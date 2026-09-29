# -*- coding: utf-8 -*-
"""
DeepSeek 翻译适配层
==================
原项目的翻译走内网 ChatGLM 服务（192.168.1.196:5000/api/v1/translate），该服务已失效。
本模块用 DeepSeek 的 OpenAI 兼容接口替换它，并保持原调用契约不变：

    interface_to_dict(text)  ->  {"data": "<译文>"}

支持:
    - API Key 从环境变量 DEEPSEEK_API_KEY 或项目根目录 .env 读取（不硬编码）
    - 批量并发翻译 + 本地缓存（避免重复计费 / 便于失败重试）
    - 失败自动重试
"""
import hashlib
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translate_cache.json")

_cache = {}
_cache_lock = threading.Lock()

SYSTEM_PROMPT = (
    "你是学术论文翻译助手。用户会给你一段从英文论文/研报中提取的文本，请翻译成中文。"
    "要求：\n"
    "1. 只输出译文本身，不要输出任何解释、前后缀、引号或 Markdown 代码块标记。\n"
    "2. 保持专业术语准确，使用学术论文的书面语风格。\n"
    "3. 数字、单位、公式、LaTeX、变量名、引用标记（如 [1]、(Smith et al., 2020)）、URL、"
    "代码、图表编号（如 Figure 1、Table 2）保持原样不翻译。\n"
    "4. 如果输入本身已经是中文，原样返回。\n"
    "5. 如果输入是无意义的符号或空白，原样返回。"
)


def _read_env_file():
    """从项目根目录 .env 读取配置（不覆盖已有的系统环境变量）"""
    env_path = os.path.join(_PROJECT_ROOT, ".env")
    if not os.path.isfile(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception as e:
        print("[deepseek] 读取 .env 失败: {}".format(e))


_read_env_file()


def get_api_key():
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "未找到 DEEPSEEK_API_KEY。请设置环境变量，或在项目根目录 .env 中写入 "
            "DEEPSEEK_API_KEY=sk-xxxx"
        )
    return key


def get_base_url():
    return os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").strip()


def get_model():
    return os.environ.get("DEEPSEEK_MODEL", "deepseek-chat").strip()


# --------------------------------------------------------------------------- #
# 缓存
# --------------------------------------------------------------------------- #
def _load_cache():
    global _cache
    if os.path.isfile(_CACHE_PATH):
        try:
            with open(_CACHE_PATH, "r", encoding="utf-8") as f:
                _cache = json.load(f)
        except Exception:
            _cache = {}


def _save_cache():
    try:
        with open(_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(_cache, f, ensure_ascii=False, indent=0)
    except Exception as e:
        print("[deepseek] 缓存写入失败: {}".format(e))


def _key(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


_load_cache()


# --------------------------------------------------------------------------- #
# 核心调用
# --------------------------------------------------------------------------- #
_client = None
_client_lock = threading.Lock()


def _get_client():
    global _client
    if _client is None:
        with _client_lock:
            if _client is None:
                from openai import OpenAI
                _client = OpenAI(api_key=get_api_key(), base_url=get_base_url())
    return _client


def translate_text(text, retries=3, temperature=0.3):
    """翻译单段文本。失败抛异常。"""
    text = (text or "").strip()
    if not text:
        return ""

    k = _key(text)
    with _cache_lock:
        if k in _cache:
            return _cache[k]

    last_err = None
    for attempt in range(retries):
        try:
            resp = _get_client().chat.completions.create(
                model=get_model(),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                temperature=temperature,
                stream=False,
            )
            out = (resp.choices[0].message.content or "").strip()
            if out:
                with _cache_lock:
                    _cache[k] = out
                return out
            last_err = RuntimeError("接口返回空内容")
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise RuntimeError("DeepSeek 翻译失败: {}".format(last_err))


def translate_batch(texts, workers=8, progress=True):
    """
    并发翻译多段文本，返回与输入等长的列表（顺序一致）。
    单段失败不会中断整体，失败位置返回空字符串并在控制台提示。
    """
    results = [""] * len(texts)
    todo = [(i, t) for i, t in enumerate(texts) if (t or "").strip()]
    if not todo:
        return results

    done = [0]
    total = len(todo)

    def _work(item):
        idx, txt = item
        try:
            results[idx] = translate_text(txt)
        except Exception as e:  # noqa: BLE001
            print("[deepseek] 第 {} 段翻译失败: {}".format(idx, e))
            results[idx] = ""
        finally:
            with _cache_lock:
                done[0] += 1
                if progress and (done[0] % 10 == 0 or done[0] == total):
                    print("[deepseek] 翻译进度 {}/{}".format(done[0], total), flush=True)

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        list(ex.map(_work, todo))

    _save_cache()
    return results


# --------------------------------------------------------------------------- #
# 兼容原项目契约
# --------------------------------------------------------------------------- #
def interface_to_dict(content):
    """与原 translate_interface.interface_to_dict 完全相同的返回结构。"""
    try:
        return {"data": translate_text(content)}
    except Exception as e:  # noqa: BLE001
        print("[deepseek] 翻译失败: {}".format(e))
        return False
