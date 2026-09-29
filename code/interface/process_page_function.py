import os
import subprocess
import tempfile
from urllib.request import pathname2url

import fitz
from PIL import Image
import numpy as np
from collections import Counter

def get_one_page_span(page, page_num):
    """
    参数:page是单个fitz类对象，且为一页,page_num是page所属的页码
    返回值:返回当前页出现的span
    """
    span_ = []
    text_dict = page.get_text("dict")  # 获取文本信息字典
    for block in text_dict["blocks"]:  # 遍历每个文本块
        if block["type"] == 0:  # 如果是文字类型
            for line in block["lines"]:  # 遍历每一行
                for span in line["spans"]:  # 遍历每个span
                    span["page"] = page_num
                    span_.append(span)
    return span_


def pdf_page_to_image(path="", page_num=0, sampling_rate=3):
    """
    功能:将pdf转为图片
    :param path:
    :param page_num:
    :param sampling_rate:
    :return:
    """
    doc = fitz.open(path)
    page = doc[page_num]
    # 获取页面大小
    page_width, page_height = page.rect.width, page.rect.height
    # # 计算新的尺寸
    # new_width = int(page_width * sampling_rate)
    # new_height = int(page_height * sampling_rate)
    # 创建包含缩放因子的转换矩阵
    matrix = fitz.Matrix(sampling_rate, sampling_rate)
    # 使用指定的采样率将页面转换为pixmap
    pix = page.get_pixmap(matrix=matrix)
    # 将pixmap转换为PIL图像
    pix_array = pixmap_to_PIL_image(pix)
    pix_1 = np.array(pix_array)
    return pix_1, page_width, page_height


def pixmap_to_PIL_image(pixmap):
    # 获取图像数据
    image_data = pixmap.samples
    # 创建PIL Image对象
    pil_image = Image.frombytes("RGB", [pixmap.width, pixmap.height], image_data)
    return pil_image



def _find_browser():
    """
    查找本机可用于 HTML -> PDF 的无头浏览器（Chromium 内核）。
    优先 Edge（Windows 自带），其次 Chrome。
    """
    candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None


def html_to_pdf(html_file, output_pdf_path, width, height, timeout=180):
    """
    用 Chromium 内核无头模式把 HTML 渲染成 PDF。
    通过 @page 规则锁定页面尺寸，保证与原始 PDF 页面 1:1 对应。

    参数:
        html_file: 输入 html 路径
        output_pdf_path: 输出 pdf 路径
        width, height: 目标页面尺寸（px，等于原 PDF 页面的 point 值）
    """
    browser = _find_browser()
    if not browser:
        raise RuntimeError(
            "未找到 Edge/Chrome，无法把 HTML 渲染为 PDF。请安装 Microsoft Edge 或 Google Chrome。"
        )

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # 锁定页面尺寸并清零默认边距
    inject = (
        "<style>"
        "@page {{ size: {w}px {h}px; margin: 0; }}"
        "html, body {{ margin: 0; padding: 0; background: #fff; }}"
        "</style>"
    ).format(w=int(round(width)), h=int(round(height)))
    if "</head>" in html:
        html = html.replace("</head>", inject + "</head>", 1)
    else:
        html = inject + html

    render_html = os.path.splitext(html_file)[0] + ".render.html"
    with open(render_html, "w", encoding="utf-8") as f:
        f.write(html)

    output_pdf_path = os.path.abspath(output_pdf_path)
    out_dir = os.path.dirname(output_pdf_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    if os.path.exists(output_pdf_path):
        os.remove(output_pdf_path)

    profile_dir = tempfile.mkdtemp(prefix="html2pdf_")
    # pathname2url 只做转义，不带 file: 协议头，必须补上，否则浏览器会当成无效地址
    page_url = pathname2url(os.path.abspath(render_html))
    if not page_url.lower().startswith("file:"):
        page_url = "file:" + page_url
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        "--user-data-dir=" + profile_dir,
        "--print-to-pdf=" + output_pdf_path,
        page_url,
    ]
    proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    if not os.path.isfile(output_pdf_path):
        raise RuntimeError(
            "HTML 转 PDF 失败。浏览器返回码:{}\n{}\n{}".format(
                proc.returncode,
                proc.stdout.decode("utf-8", "ignore")[-1500:],
                proc.stderr.decode("utf-8", "ignore")[-1500:],
            )
        )
    return output_pdf_path


def pdfkit_html_to_PDF(html_file, output_pdf_path, width, height):
    """
    [已改造] 函数名沿用，内部实现由 pdfkit + wkhtmltopdf 换成 Edge/Chrome 无头渲染。
    原实现依赖 Linux 路径 /usr/bin/wkhtmltopdf，在 Windows 上不可用。
    """
    return html_to_pdf(html_file, output_pdf_path, width, height)

def statistic_of_max_block_span(block_with_lines):
    """
    :param block: 带有lines的block
    :return:
    """
    span_list = []
    for line in block_with_lines["lines"]:
        for span in line["spans"]:
            span_list.append(span["size"])
    return max(span_list)

def get_page_main_spansize(page):
    """
    功能:拿到单页中的频率最大span size
    :return:
    """
    spansize_list = []
    text_dict = page.get_text("dict")  # 获取文本信息字典

    print(text_dict.keys())
    for block in text_dict["blocks"]:
        if block["type"] == 0:  # 如果是文字类型
            spansize_list.append(statistic_of_max_block_span(block))
            if "text" in block.keys():
                spansize_list.append(block["size"])
    font_size_choice = sorted(dict(Counter(spansize_list)).items(), key=lambda x: x[1])[-1][0]
    return font_size_choice
def get_block_text(block):
    """
    功能:
    带入正文block，返回内容文本
    :return:字符串
    """
    if "lines" in block.keys():
        p = " "
        # print(block)
        for line in block["lines"]:
            for span in line["spans"]:
                p = p+span["text"]
                # p = p+span["text"]+"  "
            # p+="\n"
        return p
    if "text" in block.keys():
        if "size" in block.keys():
            return block["text"],block["size"]
        else:
            return block["text"]