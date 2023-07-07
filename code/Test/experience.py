import head
"""
实验文本结构恢复
"""
def recovery_pdfstrure():
    """
    1.提取正文，目录恢复其在pdf中的位置
    2.加入图片

    思路：拿全文的block，span，line
    目的:熟悉html的控制
    """
    doc = head.fitz.open(head.path)
    with open("1.html","w",encoding="utf-8") as html:
        for num in range(doc.page_count):
            page = doc[num]
            page_size = page.rect
            text_dict = page.get_text("dict")
            print(text_dict)
            html.write("<div id=\"{}\" style=\"width:{}.0pt;height:{}.0pt\">".format(num, page_size[2], page_size[3]))
            for block in text_dict["blocks"]:
                print(block["bbox"])
                height = block["bbox"][3]-block["bbox"][0]
                html.write("<div id=\"{}\" style=\"top: {}pt;left:{}pt;line-height:{}pt\">".format(num, block["bbox"][1], block["bbox"][0],height))
                if block["type"] ==0:
                    for line in block["lines"]:
                        # html.write("<p style=\"top: {}pt;left:{}pt\">".format(num, line["bbox"][1], line["bbox"][0]
                        #                                                                       ))
                        # print(line.keys())
                        for span in line["spans"]:
                            #判断span类型
                            # print(span.keys())
                            print(span["text"])
                            html.write("<span style=\"font-family:{};font-size:{}pt\">".format(span["font"], span["size"]))
                            html.write(span["text"])
                            html.write("</span>")
                        # html.write("</p>")
                html.write("</div>")
            html.write("</div>")

            # break
            #只执行一个block

                # if block["type"]==0:
                #     for line in block["lines"]:

recovery_pdfstrure()
def get_table(pdf_file):
    """文本结构恢复"""
    #打开表格
    workbook = head.Workbook()
    sheet = workbook.active
    #打开pdf
    with head.pdfplumber.open(pdf_file) as pdf:
        #遍历每页pdf
        for page in pdf.pages:
            #提取表格信息
            table=page.extract_table( table_settings = {
            'vertical_strategy':"text",
            "horizontal_strategy":"text"})
            print(table)
            # 格式化表格数据
            for row in table:
                print(row)
                sheet.append(row)
    workbook.save(filename="2.xlsx")
# get_table(head.path)
def get_function_area():
    """
    拿大面积公式，并存为图片
    思考:、
    如何拿到一段话判断其是否含有公式?
    # 可否用一点简单标注？

    如何锁定一页中的公式区域?

    """

    pass

def pdf_to_html():
    """html还原pdf结构"""
    # 打开pdf文档
    doc = head.fitz.open(head.path)
    # 创建一个空的html文件
    html = open(head.os.path.join(head.os.getcwd(),"example_TEST.html"), "w")
    # 遍历pdf文档的每一页
    for page in doc:
        # 获取页面的html文本
        text = page.get_text("html")
        # if "img" in text:
        #     continue
        # if page==3:
        #     break
        # 写入html文件中
        html.write(text)
    # 关闭html文件
    html.close()
# pdf_to_html()
