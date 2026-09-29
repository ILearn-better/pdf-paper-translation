# -*- coding: utf-8 -*-
"""
PDF 论文/研报翻译 —— 命令行入口
================================
把英文 PDF 按原版式翻译成中文 PDF。

沿用原项目的核心思路（PyMuPDF 按 block 取坐标 -> 逐块翻译 -> HTML 绝对定位还原 -> 渲染回 PDF），
但做了两处必要改造：
    1) 翻译接口: 内网 ChatGLM  -> DeepSeek（见 deepseek_translate.py）
    2) PDF 生成: pdfkit+wkhtmltopdf -> Edge/Chrome 无头渲染（见 process_page_function.html_to_pdf）
并把「逐块串行调用」改为「先收集 -> 并发翻译 -> 再渲染」，避免一篇论文几百次串行请求。

用法:
    python translate_pdf.py 输入.pdf
    python translate_pdf.py 输入.pdf -o out --pages 1-3 --workers 8
"""
import argparse
import os
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import fitz  # noqa: E402
from PIL import Image  # noqa: E402

from process_page_function import html_to_pdf  # noqa: E402
from deepseek_translate import translate_batch  # noqa: E402


# --------------------------------------------------------------------------- #
# 工具
# --------------------------------------------------------------------------- #
def _fmt_seconds(s):
    if s < 60:
        return "{:.1f}s".format(s)
    return "{}m{:.0f}s".format(int(s // 60), s % 60)


def parse_pages(spec, page_count):
    """支持 '1-3'、'2'、'1,4,7'、'3-' 等写法。返回 0 基页码列表。"""
    if not spec:
        return list(range(page_count))
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, _, b = part.partition("-")
            a = int(a) if a.strip() else 1
            b = int(b) if b.strip() else page_count
            pages.extend(range(a - 1, b))
        else:
            pages.append(int(part) - 1)
    return sorted({p for p in pages if 0 <= p < page_count})


def _block_font_sizes(page):
    """返回 {四舍五入后的 bbox: 块内最大字号}，用于给 block 配字号。"""
    mapping = {}
    try:
        data = page.get_text("dict")
    except Exception:
        return mapping
    for blk in data.get("blocks", []):
        if blk.get("type") != 0:
            continue
        sizes = [sp["size"] for line in blk.get("lines", []) for sp in line.get("spans", [])]
        if not sizes:
            continue
        key = tuple(round(v, 1) for v in blk["bbox"])
        mapping[key] = max(sizes)
    return mapping


def _rotated_block_keys(page):
    """检测旋转文本块（如 arXiv 侧边栏、页边竖排字），返回其 bbox key 集合。"""
    keys = set()
    try:
        data = page.get_text("dict")
    except Exception:
        return keys
    for blk in data.get("blocks", []):
        if blk.get("type") != 0:
            continue
        for line in blk.get("lines", []):
            d = line.get("dir") or (1.0, 0.0)
            if abs(d[0]) < 0.5 and abs(d[1]) > 0.5:
                keys.add(tuple(round(v, 1) for v in blk["bbox"]))
                break
    return keys


def _main_font_size(page):
    """本页出现次数最多的字号，作为兜底字号。"""
    from collections import Counter
    sizes = []
    try:
        data = page.get_text("dict")
    except Exception:
        return 10.0
    for blk in data.get("blocks", []):
        if blk.get("type") != 0:
            continue
        for line in blk.get("lines", []):
            for sp in line.get("spans", []):
                sizes.append(round(sp["size"], 1))
    if not sizes:
        return 10.0
    return Counter(sizes).most_common(1)[0][0]


def _block_text_from_spans(page_text_blocks_item):
    """get_text_blocks() 的元组第 5 项就是块的纯文本。"""
    return (page_text_blocks_item[4] or "").replace("\n", " ").strip()


# --------------------------------------------------------------------------- #
# 单页处理
# --------------------------------------------------------------------------- #
def _merge_rects(rects, page_rect):
    """合并互相重叠的矩形（简易迭代法）"""
    merged = [fitz.Rect(r) & page_rect for r in rects]
    changed = True
    while changed:
        changed = False
        out = []
        for r in merged:
            if r.is_empty:
                continue
            hit = None
            for i, o in enumerate(out):
                if r.intersects(o):
                    hit = i
                    break
            if hit is None:
                out.append(r)
            else:
                out[hit] |= r
                changed = True
        merged = out
    return merged


def _figure_rects(page):
    """
    找一页里的图表区域 = 嵌入位图 bbox + 矢量绘图聚类。
    过滤过小(装饰线)和过大(整页背景)的区域。
    """
    page_rect = page.rect
    raw = []
    try:
        for info in page.get_image_info():
            raw.append(fitz.Rect(info["bbox"]))
    except Exception:
        pass
    try:
        raw.extend(page.cluster_drawings())
    except Exception:
        pass

    page_area = page_rect.get_area()
    rects = []
    for r in raw:
        if r.is_empty:
            continue
        if r.width < 25 or r.height < 25:          # 装饰线/下划线
            continue
        if r.get_area() > 0.9 * page_area:         # 整页背景
            continue
        rects.append(r)
    return _merge_rects(rects, page_rect)


def collect_page(page, page_index, pic_dir, scale=2.0):
    """
    抽取一页里的所有元素。
    返回 (elements, page_width, page_height)
    每个 element: {type, bbox, text, font_size}
        type=text  -> text 为英文原文
        type=image -> text 为该图裁切后的本地路径
    """
    blocks = page.get_text_blocks()  # (x0,y0,x1,y1, text, block_no, block_type)
    font_map = _block_font_sizes(page)
    rotated_keys = _rotated_block_keys(page)
    fallback_size = _main_font_size(page)

    page_rect = page.rect
    width, height = page_rect.width, page_rect.height

    # 图表区域（嵌入图 + 矢量图）：裁成图片原位回贴，图内文字不再单独翻译
    fig_rects = _figure_rects(page)
    need_crop = bool(fig_rects)
    pil_page = None
    if need_crop:
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        pil_page = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        os.makedirs(pic_dir, exist_ok=True)

    def _in_figure(bb):
        cx, cy = (bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0
        for fr in fig_rects:
            if fr.x0 <= cx <= fr.x1 and fr.y0 <= cy <= fr.y1:
                return True
        return False

    elements = []
    # 先放图，再放文字，保证文字不被图片盖住
    for fi, fr in enumerate(fig_rects):
        x0, y0 = int(round(fr.x0 * scale)), int(round(fr.y0 * scale))
        x1, y1 = int(round(fr.x1 * scale)), int(round(fr.y1 * scale))
        x0, y0 = max(0, x0), max(0, y0)
        x1 = min(pil_page.width, max(x0 + 1, x1))
        y1 = min(pil_page.height, max(y0 + 1, y1))
        crop_path = os.path.join(pic_dir, "p{}_fig{}.png".format(page_index + 1, fi))
        pil_page.crop((x0, y0, x1, y1)).save(crop_path)
        elements.append(
            {
                "type": "image",
                "bbox": [fr.x0, fr.y0, fr.x1, fr.y1],
                "text": crop_path,
                "font_size": -1,
            }
        )

    for idx, b in enumerate(blocks):
        block_type = b[6] if len(b) > 6 else 0
        bbox = [float(v) for v in b[:4]]
        key = tuple(round(v, 1) for v in b[:4])
        size = font_map.get(key, fallback_size)

        if _in_figure(bbox):
            # 图表内部的内容已随裁切图原位保留，不再重复输出
            continue

        if block_type == 1:
            # 嵌入图片未被 _figure_rects 收录时的兜底：按块截图
            if pil_page is None:
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
                pil_page = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                os.makedirs(pic_dir, exist_ok=True)
            x0, y0, x1, y1 = [int(round(v * scale)) for v in bbox]
            x0, y0 = max(0, x0), max(0, y0)
            x1 = min(pil_page.width, max(x0 + 1, x1))
            y1 = min(pil_page.height, max(y0 + 1, y1))
            crop_path = os.path.join(
                pic_dir, "p{}_{}.png".format(page_index + 1, idx)
            )
            pil_page.crop((x0, y0, x1, y1)).save(crop_path)
            elements.append(
                {"type": "image", "bbox": bbox, "text": crop_path, "font_size": size}
            )
        else:
            txt = _block_text_from_spans(b)
            if not txt:
                continue
            if key in rotated_keys:
                continue  # 旋转文本（arXiv 侧边栏等）直接丢弃
            elements.append(
                {"type": "text", "bbox": bbox, "text": txt, "font_size": size}
            )
    return elements, width, height


# 注意: style 属性用双引号包裹，这里必须用单引号，否则属性会被截断、font-size 失效
CJK_STACK = (
    "'Microsoft YaHei', 'PingFang SC', 'Hiragino Sans GB', "
    "'Source Han Sans SC', 'Noto Sans CJK SC', SimSun, sans-serif"
)


def _est_text_width(text, size):
    """粗略估算一行文本的渲染宽度（px）"""
    w = 0.0
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff" or "\u3000" <= ch <= "\u303f" or "\uff00" <= ch <= "\uffef":
            w += size          # 全角/汉字
        elif ch in " \t":
            w += size * 0.3
        else:
            w += size * 0.55   # 半角字符
    return w


def _fit_font_size(text, box_w, box_h, size, line_height=1.22, min_size=6.0):
    """
    中文塞进按英文排版的框里，纵向容易溢出。
    估算所需行数，超出框高时按比例缩小字号，避免块与块互相压盖。
    """
    import math
    box_w = max(8.0, box_w)
    lines = max(1, math.ceil(_est_text_width(text, size) / box_w))
    needed = lines * size * line_height
    if needed > box_h and needed > 0:
        size = max(min_size, size * box_h / needed)
    return size


def elements_to_html(elements, width, height, page_no):
    """按 bbox 绝对定位还原成 HTML（与原项目 recover_without_translation 同思路）。"""
    parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        "<style>body{margin:0;padding:0;}</style>",
        "</head>",
        "<body>",
        '<div id="page-{}" style="position:relative;width:{}px;height:{}px;'
        'margin:0;overflow:hidden;background:#fff;">'.format(page_no, width, height),
    ]
    for el in elements:
        x0, y0, x1, y1 = el["bbox"]
        if el["type"] == "image":
            src = _to_file_uri(el["text"])
            parts.append(
                '<img alt="fig" src="{}" style="position:absolute;top:{}px;left:{}px;'
                'width:{}px;height:{}px;"/>'.format(
                    src, y0, x0, max(1.0, x1 - x0), max(1.0, y1 - y0)
                )
            )
        else:
            box_w, box_h = max(1.0, x1 - x0), max(1.0, y1 - y0)
            size = el["font_size"] or 10.0
            size = _fit_font_size(el["text"], box_w, box_h, size)
            parts.append(
                '<div style="position:absolute;top:{}px;left:{}px;width:{}px;'
                'height:{}px;overflow:visible;word-wrap:break-word;'
                'font-family:{};font-size:{}px;line-height:1.22;color:#000;">'
                "{}</div>".format(
                    y0, x0, box_w, box_h,
                    CJK_STACK, size, _escape(el["text"]),
                )
            )
    parts += ["</div>", "</body>", "</html>"]
    return "\n".join(parts)


def _escape(s):
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def _to_file_uri(p):
    """本地路径 -> file:/// URI（图片在 Chromium 里必须用 file 协议才能加载）"""
    from urllib.request import pathname2url
    u = pathname2url(os.path.abspath(p))
    if not u.lower().startswith("file:"):
        u = "file:" + u
    return u


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def translate_pdf(pdf_path, out_dir=None, pages="", workers=8, scale=2.0, keep_tmp=False):
    pdf_path = os.path.abspath(pdf_path)
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError("找不到输入文件: {}".format(pdf_path))

    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    if out_dir is None:
        out_dir = os.path.join(HERE, "out", stem)
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    # 中间产物（图片裁切、单页 HTML/PDF）放系统临时目录，避免污染输出目录
    tmp_root = os.path.join(
        tempfile.gettempdir(), "pdf_paper_translation", stem
    )
    if os.path.isdir(tmp_root):
        shutil.rmtree(tmp_root, ignore_errors=True)
    pic_dir = os.path.join(tmp_root, "_images")
    page_dir = os.path.join(tmp_root, "_pages")
    os.makedirs(pic_dir, exist_ok=True)
    os.makedirs(page_dir, exist_ok=True)

    t_start = time.time()
    doc = fitz.open(pdf_path)
    page_list = parse_pages(pages, doc.page_count)
    print("[1/4] 打开 PDF: {} 页，本次处理 {} 页".format(doc.page_count, len(page_list)))

    # ---------- 阶段一：抽取全部元素 ----------
    per_page = []
    for i in page_list:
        page = doc[i]
        els, w, h = collect_page(page, i, pic_dir, scale=scale)
        text_n = sum(1 for e in els if e["type"] == "text")
        img_n = sum(1 for e in els if e["type"] == "image")
        per_page.append({"page_index": i, "elements": els, "width": w, "height": h})
        print(
            "      第 {} 页: 文本块 {} 个, 图片块 {} 个".format(i + 1, text_n, img_n)
        )

    # ---------- 阶段二：并发翻译 ----------
    jobs = []
    for p in per_page:
        for e in p["elements"]:
            if e["type"] == "text":
                jobs.append(e["text"])

    print("[2/4] 共 {} 个文本块待翻译，并发数 {}".format(len(jobs), workers))
    t0 = time.time()
    translated = translate_batch(jobs, workers=workers)
    print("      翻译耗时 {}".format(_fmt_seconds(time.time() - t0)))

    cursor = 0
    for p in per_page:
        for e in p["elements"]:
            if e["type"] == "text":
                e["translated"] = translated[cursor] or e["text"]
                cursor += 1

    # ---------- 阶段三：逐页还原为 HTML 并渲染 PDF ----------
    print("[3/4] 还原版式并渲染 PDF")
    page_pdfs = []
    for p in per_page:
        els = []
        for e in p["elements"]:
            if e["type"] == "text":
                els.append(dict(e, text=e.get("translated", e["text"])))
            else:
                els.append(e)
        html = elements_to_html(els, p["width"], p["height"], p["page_index"] + 1)
        html_path = os.path.join(page_dir, "page_{}.html".format(p["page_index"] + 1))
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        pdf_out = os.path.join(page_dir, "page_{}.pdf".format(p["page_index"] + 1))
        html_to_pdf(html_path, pdf_out, p["width"], p["height"])
        page_pdfs.append(pdf_out)
        print("      第 {} 页完成".format(p["page_index"] + 1))

    # ---------- 阶段四：合并 ----------
    merged = os.path.join(out_dir, stem + "_中文.pdf")
    out_doc = fitz.open()
    for f in page_pdfs:
        out_doc.insert_pdf(fitz.open(f))
    out_doc.save(merged)
    out_doc.close()

    if not keep_tmp:
        # 清理系统临时目录里的中间产物（只删自己刚创建的这个子目录）
        shutil.rmtree(tmp_root, ignore_errors=True)

    print(
        "[4/4] 完成，耗时 {}。输出: {}".format(
            _fmt_seconds(time.time() - t_start), merged
        )
    )
    return merged


def main():
    ap = argparse.ArgumentParser(
        description="把英文 PDF 论文/研报按原版式翻译成中文 PDF"
    )
    ap.add_argument("pdf", help="输入 PDF 路径")
    ap.add_argument("-o", "--out", default=None, help="输出目录")
    ap.add_argument(
        "--pages", default="", help="只处理指定页，如 1-3 / 2 / 1,4,7，默认全部"
    )
    ap.add_argument("--workers", type=int, default=8, help="翻译并发数，默认 8")
    ap.add_argument("--scale", type=float, default=2.0, help="图片裁切倍率，默认 2.0")
    ap.add_argument("--keep-tmp", action="store_true", help="保留中间产物（单页 HTML/PDF）")
    args = ap.parse_args()

    translate_pdf(
        args.pdf,
        out_dir=args.out,
        pages=args.pages,
        workers=args.workers,
        scale=args.scale,
        keep_tmp=args.keep_tmp,
    )


if __name__ == "__main__":
    main()
