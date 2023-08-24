"""
Camelot
Tabula
PDFPlumber
PDFTables

"""
import fitz
import numpy as np
from PIL import Image
import pdfplumber
import cv2
import  matplotlib.pyplot as plt
from paddleocr import PPStructure

from logger import logger


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

class PPrestructure:
    def __init__(self):
        self.table_engine = PPStructure(show_log=True, image_orientation=True)
    def structure_res(self,pdfPath,page_num,sampling=1,test_code=0):
        image, _, _ = pdf_page_to_image(pdfPath, page_num, sampling)
        print("成功将{}页转为图片".format(page_num))
        logger.info("成功将{}页转为图片".format(page_num))

        print("第{}页版面信息获取".format(page_num))
        logger.info("第{}页版面信息获取".format(page_num))
        result = self.table_engine(image)
        page_text_message = []
        other_block_message = []
        for i in result:
            # print(i["type"])
            # if i["type"]=="table" or i["type"]=="figure" :
            if i["type"] == "text":
                # coordinate = i["bbox"]
                block_unite = {
                    "type": i["type"],
                    "bbox": i["bbox"]
                }
                page_text_message.append(block_unite)
            else:
                block_unite = {
                    "type": i["type"],
                    "bbox": i["bbox"]
                }
                other_block_message.append(block_unite)
        if test_code:
            for ii in result:
                if ii["type"] == "figure":
                    coordinate = ii["bbox"]
                    x0, y0, x1, y1 = [int(j) for j in coordinate]
                    cv2.rectangle(image, (x0, y0), (x1, y1), (255, 0, 0), -1)
                    plt.imshow(image)
                    plt.show()
            cv2.imwrite("structure_recoginzation_result.png", image)
            return page_text_message, other_block_message, image
        else:
            return page_text_message, other_block_message, image
def structure_res(pdfPath,page_num,sampling=1,test_code=0):
    image,_,_ = pdf_page_to_image(pdfPath,page_num,sampling)
    print("成功将{}页转为图片".format(page_num))
    logger.info("成功将{}页转为图片".format(page_num))

    print("第{}页版面信息获取".format(page_num))
    logger.info("第{}页版面信息获取".format(page_num))
    table_engine = PPStructure(show_log=True, image_orientation=True)
    result = table_engine(image)

    page_text_message= []
    other_block_message=[]
    for i in result:
        # print(i["type"])
        # if i["type"]=="table" or i["type"]=="figure" :
        if i["type"] =="text":
            # coordinate = i["bbox"]
            block_unite = {
                "type":i["type"],
                "bbox":i["bbox"]
            }
            page_text_message.append(block_unite)
        else:
            block_unite = {
                "type":i["type"],
                "bbox":i["bbox"]
            }
            other_block_message.append(block_unite)
    if test_code:
        for ii in result:
            if ii["type"]=="figure":
                coordinate = ii["bbox"]
                x0, y0, x1, y1 = [int(j) for j in coordinate]
                cv2.rectangle(image, (x0, y0), (x1, y1), (255, 0, 0), -1)
                plt.imshow(image)
                plt.show()
        cv2.imwrite("structure_recoginzation_result.png",image)
        return page_text_message,other_block_message,image
    else:
        return page_text_message,other_block_message,image
    #参数说明:https://blog.csdn.net/pinkuang3943/article/details/119610920
   # r"""
   #  text
   #  figure_caption
   #  table
   #  footer
   #  reference
   #  """
    # save_structure_res(result, save_folder, "testPng")
if __name__ =="__main__":
    #导入图片
    pdfPath = "/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/selected_pdf_function.pdf"
    page_num = 0
    # image,_,_ = pdf_page_to_image(pdfPath,page_num,1)
    # print(type(image))
    # structure_res(pdfPath,page_num,1,test_code=1)
    Ps = PPrestructure()
    Ps.structure_res(pdfPath,page_num,1,test_code=1)
    #################################################################
    # #pdfplumber表格识别测试
    # with pdfplumber.open("selected_pdf.pdf") as pdf:
    #     # 获取第一页
    #     first_page = pdf.pages[0]
    #     # 解析表格
    #     # tables = first_page.extract_tables()
    #     tables = first_page.find_tables()
    #     for i in tables:
    #         coordinate = i.bbox
    #         x0,y0,x1,y1 =[int(i) for i in coordinate]
    #         cv2.rectangle(image,(x0,y0),(x1,y1),(255,0,0),-1)
    #         plt.imshow(image)
    #         plt.show()
    # """
    # 问题:
    #     效果不好，识别不全，图会被当成表格
    # """
    #################################################################
