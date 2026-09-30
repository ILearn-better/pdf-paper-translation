# PDF 论文翻译工具

将英文 PDF 论文 / 研报按**原版式**翻译成中文并输出 PDF。

> 原版（2023）基于 PyMuPDF 坐标提取 + 内网 ChatGLM 翻译 + wkhtmltopdf 渲染。
> 本版已完成三处关键改造，使其可在 Windows 本地独立跑通（详见下文"改造说明"）。

## 效果

输入英文论文（如 Attention Is All You Need），输出保留原始版式的中文 PDF：
标题、多栏作者区、摘要、正文、脚注均按原坐标还原。

## 环境准备

```bash
# 1. 创建虚拟环境（Python 3.12，PaddleOCR 生态兼容性最好）
python -m venv C:\Users\zhoulikun\.workbuddy\binaries\python\envs\pdf-paper-translation

# 2. 安装依赖
C:\Users\zhoulikun\.workbuddy\binaries\python\envs\pdf-paper-translation\Scripts\python.exe ^
    -m pip install pymupdf opencv-python pillow numpy requests openai flask

# 3. 扫描件版式识别（不处理扫描件可跳过）
#    ⚠ paddlepaddle 与 paddleocr 都**不在**清华源里（报 "from versions: none"）：
#      paddlepaddle 走 Paddle 官方源，paddleocr 走 PyPI 官方源，别加 -i 镜像
C:\Users\zhoulikun\.workbuddy\binaries\python\envs\pdf-paper-translation\Scripts\python.exe ^
    -m pip install paddlepaddle==3.4.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
C:\Users\zhoulikun\.workbuddy\binaries\python\envs\pdf-paper-translation\Scripts\python.exe ^
    -m pip install paddleocr==3.7.0
```

模型缓存在 `~/.paddlex/official_models`（约 2GB），首次运行自动下载，之后各环境共用。

还需本机装有 **Microsoft Edge** 或 **Chrome**（用于 HTML → PDF 渲染，程序自动查找）。

## 配置 DeepSeek API Key

在项目根目录创建 `.env`（已被 .gitignore 排除，不会入库）：

```
DEEPSEEK_API_KEY=sk-xxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

也可直接设置同名系统环境变量，优先级高于 `.env`。

## 使用

```bash
cd code/interface

# 翻译整本
python translate_pdf.py "media/input/Attention_is_all_you_need.pdf"

# 常用参数
python translate_pdf.py 论文.pdf ^
    -o out/自定义目录 ^     # 输出目录（默认 out/<文件名>/）
    --pages 1-5 ^           # 只翻译指定页（1 基页码，支持 1,4,7 混合写法）
    --workers 8 ^           # 翻译并发数
    --scale 2.0 ^           # 图片裁切倍率
    --ocr auto ^            # 扫描件版式识别：auto（默认）/ always / never
    --ocr-profile fast ^    # 识别档位：default 精度优先 / fast 快 3~5 倍
    --keep-tmp              # 保留单页中间 HTML/PDF（调试用）
```

输出：`out/<文件名>/<文件名>_中文.pdf`
首次翻译结果写入 `translate_cache.json`，重复运行不重复计费。

## 扫描件支持（版式识别层）

原版依赖 PyMuPDF 的 `get_text_blocks()` 取元素——**只有带文本层的电子版 PDF 才成立**。
纯扫描件（整页就是一张图）抽出来是 0 个文本块，整条链路拿不到任何元素，会输出空白页。

`ocr_frontend.py` 补上了缺的这一层，接在元素抽取的位置（`--ocr auto`，默认开）：

| 页面类型 | 元素来源 | 说明 |
| --- | --- | --- |
| 有文本层 | `translate_pdf.collect_page` | 原逻辑，bbox 与字号直接取自 PDF |
| 无文本层（扫描页） | `ocr_frontend.collect_page_ocr` | PP-DocLayout_plus-L 版面检测 + PP-OCRv5 文字识别 |

两条路产出的元素结构完全一致（`{type, bbox, text, font_size}`），
坐标统一换算成 PDF 点（pt），**后面的翻译与 bbox 绝对定位渲染层零改动**。

版面区域的处理策略：

- **文字类区域** → 取 OCR 文字，参与翻译
- **图 / 表 / 公式 / 印章 / 图表区域** → 从页面位图原位裁切回贴，**不翻译**（数学卷的公式和几何图靠这条保住原样，不会被 OCR 成乱码）

实现要点（踩过的坑）：

- `FLAGS_use_onednn=0` 必须在 `import paddle` **之前**设置。PaddlePaddle 3.4.0 在
  Windows/CPU 上「PIR 新执行器 + oneDNN」有已知缺陷，开了会在版面检测模型（RT-DETR）
  上直接抛 `NotImplementedError: ConvertPirAttribute2RuntimeAttribute not support`；
  pipeline 参数里的 `enable_mkldnn=False` 是第二道保险。
- 公式识别与表格识别**主动关掉**（`use_formula_recognition=False` 等）：
  一是省掉 7 个模型的加载与推理，二是这些区域本来就按图片保留，识别了也用不上。
- OCR 放在**每页一个子进程**里跑（`ocr_frontend` 以 `--png/--out` 参数自调）：
  实测长进程连续推理多页偶发 Segmentation fault（Paddle 3.4.0 / Windows CPU），
  独立进程单页非常稳；崩了只损失一页并自动重试，代价是每页多 ~12s 模型加载。
- 文字块按 **OCR 行**拆分而不是整块还原：`block_content` 有时会把题干和
  A/B/C/D 选项合并成一行，按行还原才能保住试卷的分行结构。
- **设备自动探测**：装了 GPU 版 Paddle（`paddlepaddle-gpu`）就自动走 GPU，
  否则退回 CPU；环境变量 `PADDLE_DEVICE=cpu/gpu` 可强制指定。
  GPU（RTX 4050 6GB）单页 OCR 约 150s → 数秒级。CPU 版的 oneDNN 缺陷
  只影响 CPU，GPU 上无此问题（flags 留着无害）。
  Windows GPU 安装：官方 cu118 源装 `paddlepaddle-gpu==3.3.1`（驱动需 ≥452.39，
  cu126 需 ≥550.54），CUDA 运行库（nvidia-*-cu11 共 ~1.7GB）会一并作为 pip 依赖拉取。

## 流水线

```
PDF ──PyMuPDF──> 探测该页有无文本层
     │
     ├─ 有文本层 ──> 每页 block(bbox, 文本, 字号) + 图片裁切
     │
     └─ 无文本层（扫描件）──> PP-DocLayout + PP-OCRv5（ocr_frontend.py）
                              └─> 文字区域转元素 / 图·表·公式区域原位裁图
     │
     ├─ 收集全部文本块 ──DeepSeek 并发翻译──> 中文文本
     │
     └─ 按 bbox 绝对定位生成 HTML ──Edge/Chrome 无头渲染──> 单页 PDF
                │
                └── PyMuPDF 合并 ──> 中文 PDF
```

## 相对原版的改造说明

| 环节 | 原版 | 现在 | 原因 |
| --- | --- | --- | --- |
| 翻译接口 | 内网 ChatGLM `192.168.1.196:5000` | DeepSeek（OpenAI 兼容） | 内网服务已失效 |
| 调用方式 | 逐块串行，一篇论文数百次请求 | 先收集、线程池并发、带缓存 | 全文翻译耗时从小时级降到分钟级 |
| PDF 渲染 | pdfkit + `/usr/bin/wkhtmltopdf` | Edge/Chrome 无头 `--print-to-pdf` | 原路径是 Linux 的，Windows 不可用 |
| 图片处理 | OpenCV 截图（RGB/BGR 通道反了） | PIL 裁切 | 修正色彩 |
| 版式 | 固定框，溢出互相压盖 | 按框高自动收缩字号 | 中文比英文占高 |
| 扫描件 | 无（只有文本层，扫描件输出空白页） | 增 `ocr_frontend.py`：PP-DocLayout + PP-OCRv5 前置，`--ocr auto` 按页自动启用 | 扫描的试卷/讲义没有文本层 |
| 入口 | Flask 服务 + 业务回调 | `translate_pdf.py` 命令行 | 本地独立使用 |

## 已知局限

- 旋转文本（如 arXiv 侧边栏竖排字）会被过滤
- 公式仍按普通文本处理（乱码风险），表格按原位截图保留
- 双栏论文块间偶尔仍有轻微重叠，可通过 `--scale` 与字号收缩阈值调优
- 走 OCR 的扫描页：行内公式会被当普通文字 OCR（有乱码风险）；行间公式、表格、
  几何图按**图片**原位保留，所以译文页里的公式是原图而不是排版后的公式
- OCR 的版式粒度是「版面区域块」，块内多行文字会整体重排，不如电子版逐行精确

## 升级方向：Paddle 新版版式模型

PaddleOCR 3.x（2025）已远超本项目用的 2.6 时代：

- **PP-StructureV3**：通用文档解析，输出保留结构的 Markdown/JSON，
  版面检测模型 PP-DocLayout_plus-L 支持 20+ 类别（正文/标题/表格/公式/图/印章等）
  → **已落地**：`ocr_frontend.py` 用它做扫描件的版面检测 + 文字识别
- **PP-DocTranslation**（3.1.0 新增）：PP-StructureV3 + LLM 的端到端文档翻译产线，
  **LLM 可通过 `chat_bot_config` 指定为任意 OpenAI 兼容接口（含 DeepSeek）**，支持术语表
- **PaddleOCR-VL**（3.3.0 新增）：0.9B 视觉-语言文档解析模型，复杂元素识别 SOTA

还可以再往下走的一步：把 `ocr_frontend._BASE_KWARGS` 里的
`use_formula_recognition` 打开，公式就能转成 LaTeX 参与翻译而非截图保留。
代价是 CPU 上单页可能从几十秒涨到几分钟（公式模型是重 transformer），
所以默认关着，需要时再按页开。
