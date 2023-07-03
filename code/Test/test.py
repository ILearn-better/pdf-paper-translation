import fitz
import sys
import head
from find_main_text import statistics_of_font_size,find_main_text_font_size,find_main_text
from tools_function import draw_pdf1
def test():
    """
    功能:测试statistics_of_font_size函数
    :return:
    """
    doc = fitz.open(head.path)
    record_most_account = []
    for i in range(doc.page_count):
        print(statistics_of_font_size(doc[i]))
# test()


def test_1():
    """
        可视化正文提取情况
    """
    span_list = find_main_text(head.path,find_main_text_font_size(head.path))
    doc = fitz.open(head.path)
    for i in span_list:
        for j in i:
            print(j)
            page = doc[j["page"]]
            rect = fitz.Rect(j["bbox"])
            page.draw_rect(rect)
    doc.save("检测正文span分割情况_基于TEST.pdf.pdf")

# test_1()

def test_2():
   pass
# test_2()

def test_3():
    """
    功能:绘制所有span在pdf中的位置
    参数:无
    返回值:无
    """
    from tools_function import get_all_page_span
    span_list = get_all_page_span(head.path)
    print(span_list)
    draw_pdf1(span_list,"全文span检测")

# test_3()
"""
问题:画的好小，好歪
分析:可能是用的是markdown转过来的pdf，span信息有问题
=============================================
实验:更改为word转pdf,span坐标可正常绘制内容。
"""

def test4():
    """
    找一个坐标(75.52161407470703, 69.13951110839844, 332.57098388671875, 81.09500885009766)在pdf上画框
    """
    import fitz
    doc = fitz.open(head.path)
    page = doc[0]
    rect = fitz.Rect((75.52161407470703, 69.13951110839844, 332.57098388671875, 81.09500885009766))
    page.draw_rect(rect)
    doc.save("file_name" + ".pdf")
# test4()
"""
问题:画的好小，好歪
分析:可能是用的是markdown转过来的pdf，span信息有问题
"""

def test5():
    """
    测试Choose_TOC_span函数提取性能
    :return:
    """
    from find_TOC import Choose_TOC_span
    from tools_function import draw_pdf1
    span_,_ = Choose_TOC_span(head.path)
    draw_pdf1(span_,"检测TOC提取情况_基于AI could create a 文档")
# test5()

def test6():
    """
    功能:测试line中的不同span的bbox有什么不同
    参数:
    返回值:
        分界span list
    """
    from find_paragraph import get_block
    block_list = get_block(head.path)
    # doc =fitz.open(head.path)
    for block in block_list:
        # page=doc[block["page"]]
        if block["type"] == 0:  # 如果是文字类型
            for line in block["lines"]:  # 遍历每一行

                print("line-box:", line["bbox"])
                print("=========================")
                for i in range(len(line["spans"])):
                    print("line-spans-box:",line["spans"][i]["bbox"])
                    print("--------------------")
                # rect = fitz.Rect(line["bbox"])
                # page.draw_rect(rect)
    # doc.save("line_span_distinct" + ".pdf")

# test6()
"""
=========================
line-box: (304.7243957519531, 427.0152587890625, 458.22845458984375, 436.6152648925781)
line-spans-box: (394.3164367675781, 427.0152587890625, 441.2284851074219, 436.6152648925781)
line-box: (304.7243957519531, 427.0152587890625, 458.22845458984375, 436.6152648925781)
line-spans-box: (441.23638916015625, 427.0152587890625, 458.22845458984375, 436.6152648925781)
line-box: (304.7243957519531, 427.0152587890625, 458.22845458984375, 436.6152648925781)
=========================
根据测试结果发现,coordinate会有不同,但是差距不是特别大,有相似的地方.
"""
def test7():
    """
    绘制全文block
    :return:
    """
    from tools_function import get_block
    import fitz
    blocks = get_block(head.path)
    doc = fitz.open(head.path)
    for i in blocks:
        page = doc[i["page"]]
        rect = fitz.Rect(i["bbox"])
        page.draw_rect(rect)
    doc.save("绘制全文block" + ".pdf")
# test7()

def test8():
    """
    测试用block当作正文
    :return:
    """
    from find_paragraph import get_main_text_block
    main_text_block = get_main_text_block()
    doc = fitz.open(head.path)
    for i in main_text_block:
        page = doc[i["page"]]
        rect = fitz.Rect(i["bbox"])
        page.draw_rect(rect)
    doc.save("绘制attention正文block" + ".pdf")
test8()