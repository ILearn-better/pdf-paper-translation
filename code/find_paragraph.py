import fitz
import head
from find_main_text import find_main_text_font_size,find_main_text
"""
在一些文章中，一个block就是一段，在这些文章中提取段落只需要判断block是否为正文就行
"""
def find_border_of_page(path):#没写完
    """
    思路:
    我要看一段文本是不是段落:
    1.边界
    2.文本的开始和结束
    """
    doc = fitz.open(path)
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")  # 获取文本信息字典
        for block in text_dict["blocks"]:  # 遍历每个文本块
            if block["type"] == 0:  # 如果是文字类型
                print(block)
                break
        break
#                 for line in block["lines"]:  # 遍历每一行
#                     for span in line["spans"]:  # 遍历每个span
#                         print(span["bbox"])




# 拿到分界span list（在main span list中筛选）
"""
具体而言：
    思路1：在block和正文找分界span(要写展开函数)，且该分界span只对当前block有效
    思路2:在全文找分界span
"""
def get_block(path):
    """
    功能:拿到全文block 如果可以最好是正文block
    参数:
        path:pdf路径
    返回值:
        全文block字典list
    """
    doc = fitz.open(path)
    all_page_block = []
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")  # 获取文本信息字典
        for block in text_dict["blocks"]:  # 遍历每个文本块
            if block["type"]==0:
                block["page"]=i
                # print(block)
                all_page_block.append(block)
    return all_page_block
# for i in range(len(get_block(head.path))):
#     print(get_block(head.path)[i].keys())#['number', 'type', 'bbox', 'lines', 'page']

def get_main_text_block():
    """
    功能:
        拿正文block（很难拿，因为一些block中混合各种span。例如目录，正文等）
        在一些文章中，一个block就是一段，在这些文章中提取段落只需要判断block是否为正文就行
    思路
    参数:full_page_block:所有页的block
    返回值:

    :return:
    """
    from find_main_text import find_main_text_font_size
    blocks = get_block(head.path)
    main_text_block= []
    main_text_font_size =find_main_text_font_size(head.path)
    for block in blocks:
        if block["type"]==0:
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["size"]==main_text_font_size:
                        main_text_block.append(block)
                        break
    return main_text_block

def get_line(block_):
    """
    功能:
        带入一个block,返回该block的line list
    参数:
        block_为一个block
    返回值:
        分界line list
    """
    line_list= []
    for block in block_:
        if block["type"] == 0:  # 如果是文字类型
            for line in block["lines"]:  # 遍历每一行
                line_list.append(line)
    return line_list
# print(get_line(get_block(head.path))[0].keys())#['spans', 'wmode', 'dir', 'bbox']
#################################################################
# 上面的思路比较零散,下面进行细化实现
def find_border_of_line():
    """
    功能:在block中找其中的分段line，将分段line保存为list，并返回
    参数:line:block下的line
    思路:
        如果没有next line就将其视为分段line
        如果有next line：
            分段line的x_0比next line的更小(更贴近block边界),且分段line的长度一般小于其他line(也有可能一样长，似具体格式而定)
    :return:
    """
    pass
"""
熟悉分析block和，line，span的结构信息
#block ['number', 'type', 'bbox', 'lines', 'page']
#line ['spans', 'wmode', 'dir', 'bbox']
"""
# 思考流程：想出流程-》实验-》修正-》循环