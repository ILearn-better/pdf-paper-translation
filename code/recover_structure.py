"""
文本结构恢复：
思路:各种元素融合成大list，用page进行判别

"""

import head
from get_picture import extract_images_to_save_into_png
import head
from translate_and_shift_to_json import translate_and_shift_to_json3
from translate import translate
def recover_structure_English():
    """
    提取英文内容，检测英文分段成果
        恢复段落在pdf中位置结构
        恢复图片在pdf中位置结构
    """

    paragraph = translate_and_shift_to_json3()#拿分好的段落数据
    # print(paragraph)
    #展开paragraph
    blocks= []
    for i in paragraph:
        if len(i)>=1:
            for j in i:
                blocks.append(j)
        else:
            # print(len(i))
            # print(i)
            # if len(i)!=0:
            #     blocks.append(i)
            continue
    pic_dict_list = extract_images_to_save_into_png(head.path,1)
    blocks = blocks+pic_dict_list

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
                # print(block)
                # print(len(block))
                if block["page"]==i:
                    x0, y0, x1, y1 = block["bbox"]
                    rate =2.0

                    if block["type"]=="image":

                        show_path=head.os.path.join("./output/paper/paper1/pic",head.os.path.basename(block["save_path"]))
                        file.write("<img id=\"{}\" alt=\"pic\" src=\"{}\" style=\"position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;\"/>".format(str(i),show_path,y0*rate,x0*rate,(x1-x0)*rate,(y1-y0)*rate))


                    else:
                        file.write(
                            "<div style=\"font-size:10;position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;word-wrap:break-word;\">".format(
                                y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))
                        textt = head.get_block_text(block)
                        file.write("<p style=\"font-size=10\">")
                        file.write(textt)
                        file.write("</p>")

                        file.write("</div>")
                else:
                    continue
            file.write("</div>")

        file.write("</html>")
def recover_structure_Chinese():
    """
    提取英文内容，翻译为中文内容，再恢复分段成果:
        恢复段落在pdf中位置结构
        恢复图片在pdf中位置结构
    """

    paragraph = translate()#拿分好的段落数据
    # print(paragraph)
    #展开paragraph
    blocks= []
    for i in paragraph:
        if len(i)>=1:
            for j in i:
                blocks.append(j)
        else:
            # print(len(i))
            # print(i)
            # if len(i)!=0:
            #     blocks.append(i)
            continue
    pic_dict_list = extract_images_to_save_into_png(head.path,1)
    blocks = blocks+pic_dict_list

    doc = head.fitz.open(head.path)
    with open("翻译好的.html",'w',encoding="utf-8") as file:
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<head>")
        file.write("</head>")

        for i in range(doc.page_count):
            page_size = doc[i].rect
            file.write("<div id=\"{}\" style=\" position: relative;width: {}px;height: {}px;margin: 0px; border:1px solid #000\">".format(str(i),page_size[2]*2,page_size[3]*2))
            for block in blocks:
                # print(block)
                # print(len(block))
                if block["page"]==i:
                    x0, y0, x1, y1 = block["bbox"]
                    rate =2.0
                    if block["type"]=="image":

                        show_path=head.os.path.join("./output/paper/paper1/pic",head.os.path.basename(block["save_path"]))
                        file.write("<img id=\"{}\" alt=\"pic\" src=\"{}\" style=\"position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;\"/>".format(str(i),show_path,y0*rate,x0*rate,(x1-x0)*rate,(y1-y0)*rate))


                    else:
                        file.write(
                            "<div style=\"font-size:10;position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;word-wrap:break-word;\">".format(
                                y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))
                        textt = block["text"]
                        file.write("<p style=\"font-size=10\">")
                        file.write(textt)
                        file.write("</p>")

                        file.write("</div>")
                else:
                    continue
            file.write("</div>")

        file.write("</html>")

recover_structure_Chinese()
#字体是十号