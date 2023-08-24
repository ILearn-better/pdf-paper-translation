import fitz
from PIL import Image
import numpy as np
import pdfkit
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



def pdfkit_html_to_PDF(html_file, output_pdf_path,width,height):
    """
    pdfkit方法
    """
    # 配置Wkhtmltopdf的路径
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    # HTML文件的路径
    options = {
        'quiet': '',
        # 'dpi': 75,
        'javascript-delay': '2000',  # 延时2s，echarts画图需要时间
        # 'minimum-font-size': '24',  # 字体大小
        # 'footer-right': 'xx有限公司',  # 页脚
        # 'footer-font-size': 10,  # 页脚字体大小
        # 'footer-spacing': 20,  # 页脚距离正文距离
        # 'footer-line': '',  # 页脚显示与正文分割线
        # 'margin-bottom': 25,  # 正文与底部距离
        'encoding': 'UTF-8',
        "enable-local-file-access": None,
        'image-quality': 500,  # 当使用 jpeg 算法压缩图片时使用这个参数指定的质量(默认为 94)  解决分式位置上移问题，原因不清楚，猜测：公式被转成类似图片
        # 'no-pdf-compression': '',
        'page-width': str(width)+"px",  # 设置页面宽度为8.5英寸
        'page-height':str(height)+"px"  # 设置页面高度为11英寸
    }

    # 使用pdfkit将HTML转换为PDF，并传入配置
    pdfkit.from_file(html_file, output_pdf_path, options=options, configuration=config)
    """
    pdfkit问题解决方案:
    https://blog.csdn.net/weixin_54644396/article/details/113055065
    参数说明:
    https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
    下载:
    https://wkhtmltopdf.org/downloads.html
    """

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