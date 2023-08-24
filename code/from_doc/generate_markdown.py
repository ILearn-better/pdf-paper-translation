import head as headPath
from find_main_text import find_main_text_font_size
"""
简单的pdf转markdown：
将所有span逐个放置到markdown
"""
#恢复本文和字号
"""

"""
import fitz

def pdf_to_markdown(pdf_path, markdown_path):
    doc = fitz.open(pdf_path)
    main_text_size=find_main_text_font_size(headPath.path)
    with open(markdown_path, 'w', encoding='utf-8') as md_file:
        for i in range(doc.page_count):
            page=doc[i]
            # print(dir(page))
            text_dict = page.get_text("dict")
            for block in text_dict["blocks"]:
                if block["type"]==0:
                    for line in block["lines"]:
                        for span in line["spans"]:#对于一些block就是span的可能会有重复
                            # print(span)
                            if span["size"]>main_text_size:
                                md_file.write("<span  style=\"font-size: {}px;\">".format(span["size"])+span["text"]+"</span>"+"\n")
                            if span["size"]==main_text_size:
                                md_file.write("<span  style=\"font-size: {}px;\">".format(span["size"])+span["text"]+"</span>")
                md_file.write("\n")
        """
        对比找问题：
        1.目录结构未保留
        2.字体显示有问题
        3.换行与文本连贯性
        """
    doc.close()

def pdf_mainText_to_markdown(pdf_path, markdown_path):
    """
    功能:
        正文转markdown
    参数:
        pdf_path:pdf路径
        markdown_path:markdown路径
    返回值:
    """
    from find_paragraph import get_main_text_block
    main_text_block = get_main_text_block()
    with open(markdown_path, 'w', encoding='utf-8') as md_file:
        for block in main_text_block:
            print(block["page"])
            if block["type"]==0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        md_file.write("<span  style=\"font-size: {}px;\">".format(span["size"])+span["text"]+"</span>")
                md_file.write("\n"+"\n")
# 提供 PDF 文件路径和输出 Markdown 文件路径

def path_list():
    import os
    path_ = r"/output/Resume_md\简历\失败简历\失败简历"
    p_list = []
    for i in os.listdir(path_):
        p_list.append(os.path.join(path_,i))
    return p_list

if __name__=="__main__":
    pass
# pdf_path = headPath.path
# markdown_path = "output.md"
# pdf_to_markdown(pdf_path, markdown_path)
# pdf_path = path_list()
# for i in pdf_path:
# # 调用函数将 PDF 转换为 Markdown
#     name = i.split("\\")[-1]
#     # print(name)
#     r_markdown_path = r"C:\Users\EDY\Desktop\project\pdf2md\code\Resume_md\简历\span效果\\"+name+"output.md"
#     pdf_to_markdown(i, r_markdown_path)


