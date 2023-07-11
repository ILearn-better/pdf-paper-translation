# 核心
import fitz
from collections import Counter
import fitz
import head
"""
问题：会找到image span作为正文span
"""
def statistics_of_font_size(page):
    """
    参数:page是单个fitz类对象，且为一页
    返回值:返回当前页出现的front size,及span对应的box坐标和文本
    """
    font_size = []
    font_size_bbox = []
    font_size_text = []
    text_dict = page.get_text("dict")  # 获取文本信息字典
    for block in text_dict["blocks"]:  # 遍历每个文本块
        if block["type"] == 0:  # 如果是文字类型
            for line in block["lines"]:  # 遍历每一行
                for span in line["spans"]:  # 遍历每个span
                    font_size.append(span["size"])
                    font_size_bbox.append(span["bbox"])
                    font_size_text.append(span["text"])
    #                     print(span)
    #                     print(span["text"])
    #                     print(span["size"])
    #                     print(span["bbox"])

    return font_size, font_size_bbox, font_size_text




def find_main_text_font_size(path):
    """
    功能：
        找正文font size，返回全文频率最高span size
    参数：
        path
    返回值：
        正文font size
    """
    doc = fitz.open(path)
    record_most_account = []
    for i in range(doc.page_count):
        font_size, _, _ = statistics_of_font_size(doc[i])
        record_most_account = record_most_account + list(font_size)
    # print("全文span总量:", len(record_most_account))
    font_size_choice = sorted(dict(Counter(record_most_account)).items(), key=lambda x: x[1])[-1][0]
    # print("Counter:",Counter(record_most_account))
    # 正文文本选择要设定一个阈值（经验判断可为-+2）
    # print("全文频率最高span size:", font_size_choice)
    return font_size_choice

# 找正文
def find_main_text(path, main_text_font_size):
    """
    功能:
        通过比较font_size找正文
    参数:
        main_text_font_size是全文出现频率最高的font_size
    返回值:
        span字典
        主要要其中的text,bbox,page关键字
        {"text":'',"bbox":[],page:num}
    """
    main_text_font_size = find_main_text_font_size(path)
    doc = fitz.open(path)

    all_page_main_text = []
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")  # 获取文本信息字典

        per_page_main_text = []
        for block in text_dict["blocks"]:  # 遍历每个文本块
            if block["type"] == 0:  # 如果是文字类型
                for line in block["lines"]:  # 遍历每一行
                    for span in line["spans"]:  # 遍历每个span
                        #                         print(span["size"])
                        if span["size"] == main_text_font_size:
                            span["page"] = i
                            per_page_main_text.append(span)
        all_page_main_text.append(per_page_main_text)
    return all_page_main_text

#









# main_text_font_size = find_main_text_font_size(head.path)
# find_main_text(head.path, main_text_font_size)
