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
    # from find_TOC import Choose_TOC_span
    # from tools_function import draw_pdf1
    import head
    span_,_ = head.Choose_TOC_span(head.path)
    head.draw_pdf1(span_,"Calibrating distribution models from PELVE")
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
# test8()

def test9():
    """
    测试:get_other_font中的find_other_font函数提取效果
    """
    from get_other_font import find_other_font
    import fitz
    other_font = find_other_font()
    doc = fitz.open(head.path)
    for i in other_font:
        print(i["page"])
        print(i["bbox"])
        page = doc[i["page"]]
        rect =fitz.Rect(i["bbox"])
        page.draw_rect(rect)
    doc.save("绘制TEST的其他font" + ".pdf")
# test9()
"""
问题:
对三个pdf文档进行提取other font
绘制other font的效果并不太好,对于复杂文本的公式,表格等提取的很乱,失去了其关联性
"""
def text10():
    """检测分栏block的读取顺序"""
    import head
    doc = head.fitz.open(head.path)
    page = doc[16]
    blocks = page.get_text("dict")["blocks"]

    name =0
    rect =fitz.Rect(blocks[7]["bbox"])#通过改索引看变化
    page.draw_rect(rect)

    doc.save("检测分栏block的读取顺序"+"_"+str(name) + ".pdf")

# text10()
"""
实验结果：block的提取是是从左到右，从上到下
"""

def text11():
    """
    测试一下为什么一些满足分段条件的段落却没分段
    :return:
    """
    import head
    from translate_and_shift_to_json import get_block_text,has_uppercase
    data =head.get_main_text_block()
    paragraph_block =data

    block_num = 0
    result = [""]
    previous_block_paragraph = get_block_text(paragraph_block[block_num-1])
    block=paragraph_block[block_num]

    if block["type"]==0:
        block_first_letter = block["lines"][0]["spans"][0]["text"][:]
        p = get_block_text(block)
        #
        #判断首span text的首字母是否大写
        #前一个block的末尾是否为句号结尾（这种也可能不是一段）
        #下一个span的首字母是否为大写
        #末尾span的span_x1与block_x1的差的绝对值大于block长度的半
        if has_uppercase(block_first_letter) and previous_block_paragraph[-1]==".":
            result.append(p)
        else:
            # print(result)
            result[-1] +="  "+p+"  "

    save_path ="translate_markdown"
    with open(save_path+".txt",'w',encoding="utf-8") as file:
        for i in range(len(result)):
            file.write("第{}段:\n".format(i))
            file.write(result[i])
            file.write("\n")
    return result
# text11()
def text12():
    """
    检测分段成果
        1.从block_result.txt中提取内容，在pdf上画图
        2.从block_result.txt中提取内容，恢复段落结构
    """
    import head
    from translate_and_shift_to_json import translate_and_shift_to_json3


    paragraph = translate_and_shift_to_json3()#拿分好的段落数据
    # print(paragraph)

    doc = head.fitz.open(head.path)
    with open(r"./show.html","w",encoding="utf-8") as html:
        for block_index in range(len(paragraph)):
            print(len(paragraph[block_index]))
            # if type(paragraph[block_index])==list:
            if len(paragraph[block_index]) >=2:
                # print(paragraph[block_index])
                for j in paragraph[block_index]:
                    print("=" * 10)
                    # print(type(j))
                    # if type(j)==str:
                    #     print(j)
                    #     print("="*10)
                    # break

                    print("paragraph大于2:",j)
                    print("=" * 10)

                    page_size = doc[j["page"]].rect
                    #
                    html.write("<div id=\"{}\" style=\"width:{}.0pt;height:{}.0pt;position:relative\">".format(j["page"], page_size[2], page_size[3]))
                    html.write("<p style=\"position:absolute;top:{}pt;left:{}pt;\">".format(j["bbox"][1], j["bbox"][0]))
                    html.write("<span>")


                    html.write(head.get_block_text(j))#可以细化

                    html.write("</span>")
                    html.write("</p>")
                    html.write("</div>")

            else:
                tt = paragraph[block_index][0]
                # print("-"*20)
                # print(tt)
                # print("-"*20)

                # print(len(tt))
                page_size = doc[tt["page"]].rect

                html.write("<div id=\"{}\" style=\"position: relative;width:{}.0pt;height:{}.0pt\">".format(tt["page"], page_size[2],
                                                                                         page_size[3]))
                html.write("<p style=\"position:absolute;top: {}pt;left:{}pt;\">".format(tt["bbox"][1], tt["bbox"][0]))
                html.write("<span>")
                print(head.get_block_text(tt))
                html.write(head.get_block_text(tt))

                html.write("</span>")
                html.write("</p>")
                html.write("</div>")

# text12()
"""
另起思路
"""
def text13():
    """
    检测分段成果
        1.从block_result.txt中提取内容，在pdf上画图
        2.从block_result.txt中提取内容，恢复段落结构
    """
    import head
    from translate_and_shift_to_json import translate_and_shift_to_json3
    paragraph = translate_and_shift_to_json3()#拿分好的段落数据
    # print(paragraph)
    #展开paragraph
    blocks= []
    for i in paragraph:
        if len(i)>1:
            for j in i:
                blocks.append(j)
        else:
            blocks.append(i[0])
    doc = head.fitz.open(head.path)

    with open("问题_覆盖.html",'w',encoding="utf-8") as file:
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<head>")
        file.write("</head>")

        for i in range(doc.page_count):
            page_size = doc[i].rect
            file.write("<div id=\"{}\" style=\" position: relative;width: {}px;height: {}px;margin: 0px; border:1px solid #000\">".format(str(i),page_size[2]*2,page_size[3]*2))
            for block in blocks:
                if block["page"]==i:
                    x0,y0,x1,y1 =block["bbox"]
                    file.write("<div style=\"font-size:10;position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;word-wrap:break-word;\">".format(y0*2,x0*2,(x1-x0)*2,(y1-y0)*2))
                    textt = head.get_block_text(block)
                    file.write("<p style=\"font-size=10\">")
                    file.write(textt)
                    file.write("</p>")

                    file.write("</div>")
                else:
                    continue
            file.write("</div>")

        file.write("</html>")

text13()
#字体是十号
# 一页一页测

