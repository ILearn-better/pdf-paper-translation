import head as headPath
import fitz
import os
"""
将一些常用的函数放此处
"""
#########################################################################
"""
代码心得:
    对于同参的函数:
        可视为独立的功能函数
    对于参数递进的函数:
        需要一个主函数统一整体功能
"""
#########################################################################

def get_paper_path(path=r"./media"):
    """
    功能：
        获取指定目录下paper地址
    参数：
        path:paper父目录
    返回值：
        参数paper绝对路径list
    """
    path_resolution = []
    for i in os.listdir(path):
        path_resolution.append(os.path.join(os.getcwd(),"media",i))
    return path_resolution



def get_one_page_span(page,page_num):
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
                    span["page"]=page_num
                    span_.append(span)

    return span_

def get_all_page_span(path):
    """
    功能：
        获取全文span，返回全文span
    参数：
        path
    返回值：
        全文span
    """
    doc = fitz.open(path)
    record_everypage_spanlist = []
    for i in range(doc.page_count):
        span_list = []
        text_dict = doc[i].get_text("dict")  # 获取文本信息字典
        for block in text_dict["blocks"]:  # 遍历每个文本块
            if block["type"] == 0:  # 如果是文字类型
                for line in block["lines"]:  # 遍历每一行
                    for span in line["spans"]:  # 遍历每个span
                        span["page"]=i
                        span_list.append(span)
        record_everypage_spanlist = record_everypage_spanlist + list(span_list)
    return record_everypage_spanlist

# print(len(get_all_page_span(headPath.path)))

def draw_pdf1(span_list,file_name):
    """
    功能:实现一维span list的bbox在pdf中的绘制
    参数:
        可视化正文提取情况,一维list
    返回值:
        无
    """
    doc = fitz.open(headPath.path)
    for j in span_list:
        page = doc[j["page"]]
        rect = fitz.Rect(j["bbox"])
        page.draw_rect(rect)
    doc.save(file_name+".pdf")

def draw_pdf2(span_list,file_name):
    """
        可视化正文提取情况,二维list
    """
    doc = fitz.open(headPath.path)
    for i in span_list:
        for j in i:
            print(j)
            page = doc[j["page"]]
            rect = fitz.Rect(j["bbox"])
            page.draw_rect(rect)
    doc.save(file_name+".pdf")

def get_block(path):
    """
    功能:拿到全文block
    参数:
        path:pdf路径
    返回值:
        全文block字典list
    """
    doc = fitz.open(path)
    all_page_block =[]
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")  # 获取文本信息字典
        for block in text_dict["blocks"]:  # 遍历每个文本块
            block["page"]=i
            # print(block)
            all_page_block.append(block)
    return all_page_block


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
def get_block_main_font_size():
    """
    返回一个block中的最大频率的font size
    """

    return
if __name__ == "__main__":
    pass