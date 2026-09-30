# -*- coding: utf-8 -*-
"""
扫描件版式识别前置层
====================
translate_pdf.py 原本完全依赖 PyMuPDF 的文本块（page.get_text_blocks），
这只有「电子版 PDF」才有。纯扫描件（整页就是一张图）抽出来是 0 个文本块，
整条链路拿不到任何元素，输出就是空白页。

本模块补上缺的那一层：PaddleOCR 的版面检测 + 文字识别，
把一页扫描图变成 [(bbox, 文字, 类型)] 元素列表，
交给 translate_pdf 原有的「翻译 -> bbox 绝对定位 -> 渲染」流程，渲染层零改动。

坐标约定
--------
模型在「按 scale 倍渲染出来的页面位图」上给出像素框，这里统一除以 scale
换算回 PDF 点（pt），与 page.rect 同一坐标系，因此 elements_to_html 不用改。

版面区域处理策略
----------------
文字类区域（text / title / paragraph_title ...）-> 取 OCR 文字，参与翻译
图 / 表 / 公式 / 印章 / 图表区域                  -> 从页面位图裁切，原位回贴，不翻译
（数学卷的公式与几何图靠后面这条保住原样，不会被 OCR 成乱码）
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

# ---------------------------------------------------------------------------
# 必须在 import paddle 之前设置。
#
# FLAGS_use_onednn=0 是硬性要求：PaddlePaddle 3.3+ 在 Windows/CPU 上
# 「PIR 新执行器 + oneDNN」有已知缺陷，开了会在版面检测模型（RT-DETR）上直接抛
#   NotImplementedError: ConvertPirAttribute2RuntimeAttribute not support
# 关掉 oneDNN 走标准 CPU 内核即可（PaddlePaddle/PaddleOCR#17539、#17947）。
# use_mkldnn=False 在下面的 pipeline 参数里是第二道保险。
# ---------------------------------------------------------------------------
os.environ.setdefault("FLAGS_use_onednn", "0")
os.environ.setdefault("FLAGS_use_mkldnn", "0")
os.environ.setdefault("PADDLE_PDX_MODEL_SOURCE", "BOS")

import fitz  # noqa: E402
from PIL import Image  # noqa: E402


# 这些版面类别一律当"图"处理：原位裁切回贴，不做文字识别与翻译
NON_TEXT_LABELS = {"image", "figure", "table", "chart", "seal", "formula"}

# 速度档位：fast 换小模型，CPU 上快 3~5 倍，扫描件文字识别够用
PROFILES = {
    "default": {},
    "fast": dict(
        text_detection_model_name="PP-OCRv5_mobile_det",
        text_recognition_model_name="PP-OCRv5_mobile_rec",
    ),
}

_BASE_KWARGS = dict(
    device="cpu",
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    use_formula_recognition=False,   # 公式不做识别 -> 保留为原图，避免乱码
    use_table_recognition=False,     # 表格不做识别 -> 保留为原图
    use_chart_recognition=False,
    use_seal_recognition=False,
)

# 进程内复用产线：模型加载要 40~60 秒，多页/多文件时绝不能反复初始化
_PIPELINES = {}


def _pipeline_kwargs(profile="default"):
    if profile not in PROFILES:
        raise ValueError("未知 OCR 档位：%s（可选 %s）" % (profile, "/".join(PROFILES)))
    kw = dict(_BASE_KWARGS)
    kw.update(PROFILES[profile])
    return kw


def get_pipeline(profile="default"):
    """按档位取产线（进程内缓存）。"""
    if profile not in _PIPELINES:
        from paddleocr import PPStructureV3
        _PIPELINES[profile] = PPStructureV3(**_pipeline_kwargs(profile))
    return _PIPELINES[profile]


# ---------------------------------------------------------------------------
# 结果解析
# ---------------------------------------------------------------------------
def _result_to_dict(res, tmp_dir):
    """把产线结果落成 JSON 再读回来（跨版本最稳的方式）。"""
    os.makedirs(tmp_dir, exist_ok=True)
    try:
        res.save_to_json(save_path=tmp_dir)
    except TypeError:
        res.save_to_json(tmp_dir)
    files = sorted(glob.glob(os.path.join(tmp_dir, "*.json")))
    if not files:
        # 新版本可能返回 dict-like，直接兜底
        try:
            return json.loads(json.dumps(res, default=str))
        except Exception as e:  # noqa: BLE001
            raise RuntimeError("无法从产线结果中取得 JSON: {}".format(e))
    with open(files[-1], "r", encoding="utf-8") as f:
        return json.load(f)


def _iter_blocks(data):
    """产出 (label, content, bbox_px)。优先用 parsing_res_list，缺失时退回版面框。"""
    parsing = data.get("parsing_res_list") or []
    if parsing:
        for b in parsing:
            label = str(b.get("block_label") or "").lower()
            content = (b.get("block_content") or "").strip()
            bbox = b.get("block_bbox") or b.get("block_boxes") or b.get("bbox")
            if bbox is None or len(bbox) < 4:
                continue
            yield label, content, [float(v) for v in bbox[:4]]
        return

    det = data.get("layout_det_res") or {}
    for b in (det.get("boxes") or []):
        label = str(b.get("label") or "").lower()
        bbox = b.get("coordinate") or b.get("bbox")
        if bbox is None or len(bbox) < 4:
            continue
        yield label, "", [float(v) for v in bbox[:4]]


def _ocr_lines(data):
    """取 OCR 文本行框 [(x0,y0,x1,y1,text)]，用于估算字号。"""
    ocr = data.get("overall_ocr_res") or {}
    texts = ocr.get("rec_texts") or []
    polys = ocr.get("rec_polys") or ocr.get("dt_polys") or []
    out = []
    for i, poly in enumerate(polys):
        try:
            xs = [float(p[0]) for p in poly]
            ys = [float(p[1]) for p in poly]
        except Exception:  # noqa: BLE001
            continue
        out.append((min(xs), min(ys), max(xs), max(ys), texts[i] if i < len(texts) else ""))
    return out


def _est_font_size(bbox_px, lines, scale):
    """按框高 / 行数估算原文字号（pt）。"""
    h_pt = max(1.0, (bbox_px[3] - bbox_px[1]) / scale)
    x0, y0, x1, y1 = bbox_px
    inside = 0
    for lx0, ly0, lx1, ly1, _t in lines:
        cx, cy = (lx0 + lx1) / 2.0, (ly0 + ly1) / 2.0
        if x0 <= cx <= x1 and y0 <= cy <= y1:
            inside += 1
    n = max(1, inside) if inside else max(1, int(round(h_pt / 16.0)))
    size = h_pt / n / 1.25
    return max(6.0, min(36.0, size))


def _lines_in_bbox(lines, bbox_px):
    """取中心落在 bbox 内的 OCR 行，按阅读顺序（先上后下、再从左到右）返回。"""
    x0, y0, x1, y1 = bbox_px
    out = []
    for lx0, ly0, lx1, ly1, txt in lines:
        cx, cy = (lx0 + lx1) / 2.0, (ly0 + ly1) / 2.0
        if x0 <= cx <= x1 and y0 <= cy <= y1:
            out.append((lx0, ly0, lx1, ly1, txt))
    out.sort(key=lambda l: (round(l[1] / 10.0), l[0]))
    return out


def _line_font_size(lx0, ly0, lx1, ly1, scale):
    """单行 OCR 框高约为字号的 1.2 倍。"""
    h_pt = max(1.0, (ly1 - ly0) / scale)
    return max(6.0, min(36.0, h_pt / 1.2))


# ---------------------------------------------------------------------------
# 子进程 worker
# ---------------------------------------------------------------------------
# 实测长进程里连续跑多页 OCR 偶发 Segmentation fault（Paddle 3.4.0 / Windows CPU），
# 而独立进程单页跑非常稳。所以 OCR 统一放到子进程里做：每页一个 worker，
# 模型加载约 12s（有缓存），崩了只损失那一页，主程序还能重试。
def _run_worker(png_path, profile, out_json, log=print):
    cmd = [
        sys.executable, os.path.abspath(__file__),
        "--png", png_path, "--profile", profile, "--out", out_json,
    ]
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, env=env)
    if proc.returncode != 0 or not os.path.isfile(out_json):
        tail = (proc.stderr or b"")[-800:].decode("utf-8", "ignore")
        raise RuntimeError(
            "OCR 子进程失败（exit {}）:\n{}".format(proc.returncode, tail)
        )
    log("      版面识别耗时 %.1fs（子进程，含模型加载）" % (time.time() - t0))
    with open(out_json, "r", encoding="utf-8") as f:
        return json.load(f)


def _worker_main():
    ap = argparse.ArgumentParser(description="单页版式识别 worker")
    ap.add_argument("--png", required=True)
    ap.add_argument("--profile", default="default")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    pipeline = get_pipeline(args.profile)
    results = pipeline.predict(args.png)
    if not results:
        raise RuntimeError("版面识别没有返回结果")

    tmp_dir = tempfile.mkdtemp(prefix="ocr_worker_res_")
    try:
        data = _result_to_dict(results[0], tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 单页入口
# ---------------------------------------------------------------------------
def page_has_text(page, min_chars=8):
    """判断这一页有没有文本层（扫描页就是 False）。"""
    chars = 0
    try:
        for b in page.get_text_blocks():
            chars += len((b[4] or "").replace("\n", "").replace(" ", "").strip())
            if chars >= min_chars:
                return True
    except Exception:  # noqa: BLE001
        return False
    return False


def collect_page_ocr(page, page_index, pic_dir, scale=2.0, profile="default", log=print):
    """
    扫描页 -> 元素列表，与 translate_pdf.collect_page 的输出同构。

    :return: (elements, page_width_pt, page_height_pt)
    """
    os.makedirs(pic_dir, exist_ok=True)

    # 1) 整页渲染成位图，模型在这张图上工作
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    pil_page = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    page_png = os.path.join(pic_dir, "p{}_scan.png".format(page_index + 1))
    pil_page.save(page_png)

    # 2) 版面检测 + 文字识别（放子进程执行，隔离偶发崩溃，失败重试一次）
    out_json = os.path.join(pic_dir, "p%d_res.json" % (page_index + 1))
    data = None
    last_err = None
    for attempt in (1, 2):
        try:
            data = _run_worker(page_png, profile, out_json, log=log)
            break
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt == 1:
                log("      OCR 子进程失败，重试一次…")
    if data is None:
        raise RuntimeError("第 %d 页版式识别失败: %s" % (page_index + 1, last_err))
    lines = _ocr_lines(data)

    # 3) 组装元素
    # 文字块优先按 OCR 行拆分：block_content 有时会把题干和 A/B/C/D 选项
    # 合并成一行（丢掉换行），按块还原会把选项挤成连排；OCR 行自带坐标，
    # 一行一个元素才能保住试卷的分行结构。
    elements = []
    for bi, (label, content, bbox_px) in enumerate(_iter_blocks(data)):
        w_px = bbox_px[2] - bbox_px[0]
        h_px = bbox_px[3] - bbox_px[1]
        if w_px < 6 or h_px < 6:
            continue                                  # 噪点/装饰线

        bbox_pt = [v / scale for v in bbox_px]

        if content and label not in NON_TEXT_LABELS:
            block_lines = _lines_in_bbox(lines, bbox_px)
            if len(block_lines) >= 2:
                for lx0, ly0, lx1, ly1, ltxt in block_lines:
                    if not ltxt.strip():
                        continue
                    elements.append({
                        "type": "text",
                        "bbox": [lx0 / scale, ly0 / scale, lx1 / scale, ly1 / scale],
                        "text": ltxt.strip(),
                        "font_size": _line_font_size(lx0, ly0, lx1, ly1, scale),
                    })
                continue

            elements.append({
                "type": "text",
                "bbox": bbox_pt,
                "text": content,
                "font_size": _est_font_size(bbox_px, lines, scale),
            })
            continue

        # 图/表/公式/印章：原位裁切回贴，不翻译
        x0, y0 = int(max(0, round(bbox_px[0]))), int(max(0, round(bbox_px[1])))
        x1 = int(min(pil_page.width, max(x0 + 1, round(bbox_px[2]))))
        y1 = int(min(pil_page.height, max(y0 + 1, round(bbox_px[3]))))
        if x1 - x0 < 6 or y1 - y0 < 6:
            continue
        crop_path = os.path.join(pic_dir, "p{}_reg{}.png".format(page_index + 1, bi))
        pil_page.crop((x0, y0, x1, y1)).save(crop_path)
        elements.append({
            "type": "image",
            "bbox": bbox_pt,
            "text": crop_path,
            "font_size": -1,
        })

    return elements, page.rect.width, page.rect.height


if __name__ == "__main__":
    # 被 translate_pdf 以子进程方式调用，不要手工运行
    _worker_main()
