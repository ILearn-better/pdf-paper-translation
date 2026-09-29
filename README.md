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
```

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
    --keep-tmp              # 保留单页中间 HTML/PDF（调试用）
```

输出：`out/<文件名>/<文件名>_中文.pdf`
首次翻译结果写入 `translate_cache.json`，重复运行不重复计费。

## 流水线

```
PDF ──PyMuPDF──> 每页 block(bbox, 文本, 字号) + 图片裁切
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
| 入口 | Flask 服务 + 业务回调 | `translate_pdf.py` 命令行 | 本地独立使用 |

## 已知局限

- 旋转文本（如 arXiv 侧边栏竖排字）会被过滤
- 公式仍按普通文本处理（乱码风险），表格按原位截图保留
- 双栏论文块间偶尔仍有轻微重叠，可通过 `--scale` 与字号收缩阈值调优

## 升级方向：Paddle 新版版式模型

PaddleOCR 3.x（2025）已远超本项目用的 2.6 时代：

- **PP-StructureV3**：通用文档解析，输出保留结构的 Markdown/JSON，
  版面检测模型 PP-DocLayout_plus-L 支持 20+ 类别（正文/标题/表格/公式/图/印章等）
- **PP-DocTranslation**（3.1.0 新增）：PP-StructureV3 + LLM 的端到端文档翻译产线，
  **LLM 可通过 `chat_bot_config` 指定为任意 OpenAI 兼容接口（含 DeepSeek）**，支持术语表
- **PaddleOCR-VL**（3.3.0 新增）：0.9B 视觉-语言文档解析模型，复杂元素识别 SOTA

如需更强的表格/公式还原，可用 PP-StructureV3 替换本项目的坐标提取层，
翻译层不变（继续用 DeepSeek）。
