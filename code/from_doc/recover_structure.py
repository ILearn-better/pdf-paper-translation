"""
文本结构恢复：
思路:各种元素融合成大list，用page进行判别

"""
import os

import fitz

from get_picture import extract_images_to_save_into_png
import head as headPath
from translate_and_shift_to_json import translate_and_shift_to_json3
from translate import translate
from tools_function import get_block_text


def recover_structure_English():
    """
    提取英文内容，检测英文分段成果
        恢复段落在pdf中位置结构
        恢复图片在pdf中位置结构
    """

    paragraph = translate_and_shift_to_json3()  # 拿分好的段落数据
    # print(paragraph)
    # 展开paragraph
    blocks = []
    for i in paragraph:
        if len(i) >= 1:
            for j in i:
                blocks.append(j)
        else:
            # print(len(i))
            # print(i)
            # if len(i)!=0:
            #     blocks.append(i)
            continue
    pic_dict_list = extract_images_to_save_into_png(headPath.path, 1)
    blocks = blocks + pic_dict_list

    doc = fitz.open(headPath.path)
    s_p = os.path.join(os.getcwd(), "media", "output", "英文样式还原.html")
    with open(s_p, 'w', encoding="utf-8") as file:
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<head>")
        file.write("</head>")

        for i in range(doc.page_count):
            page_size = doc[i].rect
            file.write(
                "<div id=\"{}\" style=\" position: relative;width: {}px;height: {}px;margin: 0px; border:1px solid #000\">".format(
                    str(i), page_size[2] * 2, page_size[3] * 2))
            for block in blocks:
                # print(block)
                # print(len(block))
                if block["page"] == i:
                    x0, y0, x1, y1 = block["bbox"]
                    rate = 2.0

                    if block["type"] == "image":
                        show_path = os.path.join(os.getcwd(), "media", "other_out_media", "pic",
                                                      os.path.basename(block["save_path"]))

                        file.write(
                            "<img id=\"{}\" alt=\"pic\" src=\"{}\" style=\"position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;\"/>".format(
                                str(i), show_path, y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))


                    else:
                        file.write(
                            "<div style=\"font-size:10px;position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;word-wrap:break-word;\">".format(
                                y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))
                        textt = get_block_text(block)
                        file.write("<p style=\"font-size:10px\">")
                        file.write(textt)
                        file.write("</p>")

                        file.write("</div>")
                else:
                    continue
            file.write("</div>")

        file.write("</html>")


# recover_structure_English()
def recover_structure_Chinese():
    """
    提取英文内容，翻译为中文内容，再恢复分段成果:
        恢复段落在pdf中位置结构
        恢复图片在pdf中位置结构
    """
    if type(translate()) == False: return False
    paragraph = translate()  # 拿分好的段落数据
    # print(paragraph)
    # 展开paragraph
    blocks = []
    for i in paragraph:
        if len(i) >= 1:
            for j in i:
                blocks.append(j)
        else:
            # print(len(i))
            # print(i)
            # if len(i)!=0:
            #     blocks.append(i)
            continue
    pic_dict_list = extract_images_to_save_into_png(headPath.path, 1)
    blocks = blocks + pic_dict_list

    doc = fitz.open(headPath.path)

    s_p = os.path.join(os.getcwd(), "media", "output", "翻译好的.html")

    with open(s_p, 'w', encoding="utf-8") as file:
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<head>")
        file.write("</head>")

        for i in range(doc.page_count):
            page_size = doc[i].rect
            file.write(
                "<div id=\"{}\" style=\" position: relative;width: {}px;height: {}px;margin: 0px; border:1px solid #000\">".format(
                    str(i), page_size[2] * 2, page_size[3] * 2))
            for block in blocks:
                # print(block)
                # print(len(block))
                if block["page"] == i:
                    x0, y0, x1, y1 = block["bbox"]
                    rate = 2.0
                    if block["type"] == "image":

                        show_path = os.path.join("./output/paper/paper1/pic",
                                                      os.path.basename(block["save_path"]))
                        file.write(
                            "<img id=\"{}\" alt=\"pic\" src=\"{}\" style=\"position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;\"/>".format(
                                str(i), show_path, y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))


                    else:
                        file.write(
                            "<div style=\"font-size:10px;position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;word-wrap:break-word;\">".format(
                                y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))
                        textt = block["text"]
                        file.write("<p style=\"font-size:10px\">")
                        file.write(textt)
                        file.write("</p>")

                        file.write("</div>")
                else:
                    continue
            file.write("</div>")

        file.write("</html>")

# recover_structure_Chinese()
# 字体是十号
if __name__=="__main__":
    recover_structure_Chinese()
