"""
pdf转pdf,实验pdf类复原
测试:
文本提取
文本复原
图片复原
"""
import os
import cv2
import fitz
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from get_table_and_function import structure_res, PPrestructure
from logger import logger
from translate_interface import interface_to_dict


def keep_last_line_break(str1):
    """
    功能:保留最后一个换行符
    检测最后一个字符是不是换行符号，是的话才保留，不是的话用空格替换
    :return:
    """
    # text = "This is\na multiline\ntext with\nline breaks.\n"
    parts = str1.rsplit('\n', 1)  # 从右侧开始分割，只分割一次
    print(parts[1])
    modified_text = parts[0].replace('\n', ' ') + '\n' + parts[1]
    return modified_text


def pixmap_to_PIL_image(pixmap):
    # 获取图像数据
    image_data = pixmap.samples
    # 创建PIL Image对象
    pil_image = Image.frombytes("RGB", [pixmap.width, pixmap.height], image_data)
    return pil_image


def pdf_page_to_image(path="", page_num=0, sampling_rate=1):
    """
    功能:将pdf转为图片
    :param path:
    :param page_num:
    :param sampling_rate:
    :return:
    """
    doc = fitz.open(path)
    page = doc[page_num]
    # 获取页面大小
    page_width, page_height = page.rect.width, page.rect.height
    # # 计算新的尺寸
    # new_width = int(page_width * sampling_rate)
    # new_height = int(page_height * sampling_rate)
    # 创建包含缩放因子的转换矩阵
    matrix = fitz.Matrix(sampling_rate, sampling_rate)
    # 使用指定的采样率将页面转换为pixmap
    pix = page.get_pixmap(matrix=matrix)
    # 将pixmap转换为PIL图像
    pix_array = pixmap_to_PIL_image(pix)
    pix_1 = np.array(pix_array)
    return pix_1, page_width, page_height


if __name__ == "__main__":
    # 测试一下图片使用情况
    # path = r"/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/selected_pdf_page_6.pdf"
    path=r"/home/zhoulikun/zhou_work/pdf2md/code/interface_2/media/input/21180.pdf"
    doc = fitz.open(path)

    outputpdf_folder = os.path.join(os.getcwd(),"outputpdf")
    if os.path.exists(outputpdf_folder):
        print("存在pdf保存文件夹")
    else:
        os.mkdir(outputpdf_folder)
        print("pdf保存文件夹创建完成")

    pdf_save_path_list = []
    # for page_num in range(doc.page_count):
    for page_num in range(2):
        ############################################################
        ## 测试page
        # pix_1, page_width, page_height = pdf_page_to_image(path)
        # print(pix_1.shape,page_width,page_height)
        #############################################################

        page = doc[page_num]
        old_page_width,old_page_height = int(page.rect.width), int(page.rect.height)
        print("old_page_width:{},old_page_height:{}".format(old_page_width,old_page_height))
        # 得到结构信息
        sampling = 2
        Ps = PPrestructure()
        page_text_message, other_block_message, image = Ps.structure_res(path, page_num, sampling, 0)
        # page_text_message, other_block_message, image = structure_res(path, page_num, sampling,0)  # 模型一开始就得初始化，不然很慢
        print("地址:{},文本块数量:{}".format(__file__, len(page_text_message)))
        logger.info("地址:{},文本块数量:{}".format(__file__, len(page_text_message)))

        new_pdf = fitz.open()
        page_width,page_height = int(image.shape[1]),int(image.shape[0])
        new_pdf_page = new_pdf.new_page(0,page_width,page_height)
        print("图片shape:{},新pdf宽度:{},新pdf高度:{}".format(image.shape,new_pdf_page.rect.width, new_pdf_page.rect.height))
        print("原pdf宽高:{}".format(page.rect))
        for block in page_text_message:
            rate = 6
            x0, y0, x1, y1 = [round(i/sampling) for i in block["bbox"]]
            coordinate = (x0 - rate, y0 - rate, x1 + rate, y1 + rate)
            text = page.get_textbox(coordinate)
            # text = keep_last_line_break(text)
            print("获取到的文本:{}".format(text))
            translated_text = interface_to_dict(text)["data"]
            print("翻译结果:{}".format(translated_text))
            print("====" * 8)
            # 扔给翻译

            x0, y0, x1, y1 = [round(i) for i in block["bbox"]]
            coordinate = (x0, y0, x1, y1)
            # rect = fitz.Rect((x0, y0, x1, y1))
            # new_pdf_page.draw_rect(rect)
            # print("rect:",rect)
            # strr = text
            # strr = keep_last_line_break(text)

            # font = fitz.Font("cjk")
            # print("font.name:",font.name)
            # page.insert_font(fontname="F0", fontbuffer=font.buffer)
            ff = new_pdf_page.insert_font(fontname="F0",
                                          fontfile="/home/zhoulikun/zhou_work/pdf2md/code/interface_2/test/arial-unicode-ms.ttf",
                                          fontbuffer=None,
                                          set_simple=False)
            # 字体推荐:https://github.com/Haixing-Hu/latex-chinese-fonts
            if not isinstance(translated_text,str):
                translated_text = str(translated_text).replace("\n"," ")
            new_pdf_page.insert_textbox(coordinate, translated_text,
                                        fontsize=9*sampling, lineheight=1, fontname="F0", fill=None, overlay=True)

        for index, other_block in enumerate(other_block_message):
            rate = 6
            x0, y0, x1, y1 = [round(i) for i in other_block["bbox"]]

            coordinate = (x0 - rate, y0 - rate, x1 + rate, y1 + rate)
            save_name = os.path.join("image", str(page_num)+"_"+str(index) + "_.png")
            # image[y0:y1, x0:x1]
            # iim = cv2.resize(image[y0:y1, x0:x1],(old_page_width,old_page_height))
            print("image_shape:{}".format(image.shape))
            cv2.imwrite(save_name, image[y0:y1, x0:x1])
            print("====" * 8)

            rect = fitz.Rect((x0, y0, x1, y1))
            # new_pdf_page.draw_rect(rect)
            # print("rect:",rect)

            new_pdf_page.insert_image(rect, alpha=1, filename=save_name)

        pdf_save_path = os.path.join(outputpdf_folder,str(page_num)+"_"+"sd.pdf")
        new_pdf.save(pdf_save_path)
        pdf_save_path_list.append(pdf_save_path)
    # 做PDF拼接
    doc_conbine = fitz.open()
    for p in pdf_save_path_list:
        print("num_pdf_path:", p)
        doc_p = fitz.open(p)
        doc_conbine.insert_pdf(doc_p, 0)

    doc_conbine_savepath = os.path.join(outputpdf_folder, "result" + ".pdf")
    doc_conbine.save(doc_conbine_savepath)
