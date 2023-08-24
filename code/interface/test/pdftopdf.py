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

from get_table_and_function import structure_res
from logger import logger
from PIL import Image

from translate_interface import interface_to_dict


def keep_last_line_break(str1):
    """
    功能:保留最后一个换行符
    检测最后一个字符是不是换行符号，是的话才保留，不是的话用空格替换
    :return:
    """
    # text = "This is\na multiline\ntext with\nline breaks.\n"
    parts = str1.rsplit('\n', 1)  # 从右侧开始分割，只分割一次
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

if __name__ =="__main__":
    # path = r"/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/selected_pdf_page_6.pdf"
    path=r"/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/selected_pdf_function.pdf"
    page_num =0

    doc = fitz.open(path)
    page= doc[page_num]

    # 得到结构信息
    page_text_message,other_block_message,_ = structure_res(path,page_num,0)#模型一开始就得初始化，不然很慢
    print("地址:{},文本块数量:{}".format(__file__,len(page_text_message)))

    image,page_width, page_height=pdf_page_to_image(path,page_num,1)
    new_pdf = fitz.open()
    new_pdf_page = new_pdf.new_page(width= page_width,height=page_height)


    logger.info("地址:{},文本块数量:{}".format(__file__,len(page_text_message)))
    for block in page_text_message:
        rate=6
        x0,y0,x1,y1 =[round(i) for i in block["bbox"]]
        coordinate = (x0-rate,y0-rate,x1+rate,y1+rate)
        text = page.get_textbox(coordinate)
        translated_text = interface_to_dict(text)["data"]
        print("翻译结果:{}".format(translated_text))
        print("===="*8)
        #扔给翻译


        rect = fitz.Rect((x0,y0,x1,y1))
        # new_pdf_page.draw_rect(rect)
        # print("rect:",rect)
        strr = translated_text
        # strr = keep_last_line_break(text)

        # font = fitz.Font("cjk")
        # print("font.name:",font.name)
        # page.insert_font(fontname="F0", fontbuffer=font.buffer)

        new_pdf_page.insert_textbox(coordinate,translated_text,
                                    fontsize=8,lineheight = 1,fontname="china-ss")
        # new_pdf_page.insert_text(coordinate, text,
        #                            fontsize=8,lineheight = 1)

    for index,other_block in enumerate(other_block_message):
        rate=6
        x0,y0,x1,y1 =[round(i) for i in other_block["bbox"]]
        coordinate = (x0-rate,y0-rate,x1+rate,y1+rate)
        save_name = os.path.join("image",str(index)+"_.png")
        cv2.imwrite(save_name,image[y0:y1,x0:x1])
        print("===="*8)
        #扔给翻译


        rect = fitz.Rect((x0,y0,x1,y1))
        # new_pdf_page.draw_rect(rect)
        # print("rect:",rect)

        new_pdf_page.insert_image(rect,alpha=0,filename =save_name)
    new_pdf.save("sd.pdf")
