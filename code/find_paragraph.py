import fitz
import head
from find_main_text import find_main_text_font_size,find_main_text
def find_border_of_page(path):
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
def judge_paragraph_start_and_end():
    pass



def test():
    doc = fitz.open(head.path)
    for i in range(len(main_text_span)):#每一页
        for j in range(len(main_text_span[i])):#每一页的每一个span
            if j+1==len(main_text_span[i])-1:
                break
            else:
                if main_text_span[i][j]==[]:
                    continue
                else:
    #                 print(main_text_span[i][j]["bbox"])
                    if main_text_span[i][j]["bbox"][2]>main_text_span[i][j+1]["bbox"][0] and main_text_span[i][j]["bbox"][3]>main_text_span[i][j+1]["bbox"][1]:
                        print(main_text_span[i][j])
    #                     pdf_draw(main_text_span[i][j]["bbox"],path,main_text_span[i][j]["page"])
                        page = doc[main_text_span[i][j]["page"]]
                        rect = fitz.Rect(main_text_span[i][j]["bbox"])
                        page.draw_rect(rect)
    doc.save("检测全文段落span获取情况.pdf")

# 拿到分界span list（在main span list中筛选）
def get_split_span(path):
    doc = fitz.open(path)
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")  # 获取文本信息字典

        per_page_main_text = []
        for block in text_dict["blocks"]:  # 遍历每个文本块
            print(block["bbox"])


#             if block["type"] == 0:  # 如果是文字类型
#                 for line in block["lines"]:  # 遍历每一行
#                     for span in line["spans"]:  # 遍历每个span
#                         print(span["bbox"])


find_border_of_page(head.path)
# 拿到正文span list
main_text_font_size = find_main_text_font_size(head.path)
main_text_span= find_main_text(head.path,main_text_font_size)
# print(main_text_span)
# test()
get_split_span(head.path)