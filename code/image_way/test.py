"""
思路：
读取->截图->提取->粘贴->输出pdf
从基础功能开始写
"""
import sys
sys.path.append("../")
import head
import cv2
from paddleocr import PaddleOCR

def block2array(page_imge_array, page_num, block):
    """
    带入array和页数以及block，得到block矩阵，box，page
    param:
    page_imge_array:单页pdf图片
    block:block信息
    return:
        block对应的图片矩阵
        box坐标
        page页数
    """
    x1, y1, x2, y2 = [int(i) for i in block["bbox"]]
    # print("block[\"bbox\"]:",block["bbox"])
    # cv2.rectangle不接受浮点数
    cv2.rectangle(page_imge_array, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 这里的 (0, 255, 0) 是矩形框的颜色，2 是边框粗细
    # 显示图像
    cv2.imshow("Image with Rectangle", page_imge_array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return page_imge_array, block["bbox"], page_num


def block2array_shortcut(page_imge_array, page_num, block):
    """
    功能：在单页图片上通过block的坐标找到对应box截图并识别其中内容，返回信息字典
    流程：带入array和页数以及block，得到block矩阵，box，page
    param:
    page_imge_array:单页pdf图片
    block:block信息
    return:
        block对应的图片矩阵
        box坐标
        page页数
    """
    x1, y1, x2, y2 = [int(i) for i in block["bbox"]]
    # cv2.rectangle不接受浮点数
    x1, y1, x2, y2 = [i * 3 for i in (x1, y1, x2, y2)]
    page_image0 = page_imge_array
    img = page_image0[y1:y2, x1:x2, :]
    # cv2.rectangle(page_image0, (round(x1),round(x2)), (round(y1),round(y2)), (255, 0, 0), 2)  # 这里的 (0, 255, 0) 是矩形框的颜色，2 是边框粗细
    head.plt.imshow(img)
    head.plt.show()

    ocr = PaddleOCR()
    table = ocr.ocr(img)
    if table == [[]]:
        output = {
            "array": [[]],
            "bbox": block["bbox"],
            "page": page_num,
            "fontsize": 0
        }
        print("没文字的")
        return output
    else:
        text_message = table[0][0][1]
        text_1 = text_message[0]
        print("text_1:", text_1)
        fontzie = round(text_message[1])
        # 定义字体、字号和颜色
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale =3
        color = (0, 0, 0)  # 这里的 (0, 255, 0) 是文本的颜色，(B, G, R)
        # 使用cv2.putText将文本绘制在图像上
        cv2.putText(img, text_1, (0, 90), font, font_scale, color, thickness=3, bottomLeftOrigin=False)
        # 使用cv2.getTextSize获取文本的大小
        (text_width, text_height), baseline = cv2.getTextSize(text_1, font, font_scale, thickness=3)
        # 输出文本的宽度和高度
        print("文本宽度:", text_width)
        print("文本高度:", text_height)
        print("baseline:",baseline)
        # 绘制文本的左上角坐标
        x, y = (0, 90)
        # 绘制文本矩形框
        cv2.rectangle(img, (x, y), (x + text_width, y - text_height), color, 1)
        # 绘制基线
        # cv2.line(img, (x, y + baseline), (x + text_width, y + baseline), color, 1)
        print("img:", img.shape)
        head.plt.imshow(img)
        head.plt.show()


        output = {
            "array": img,
            "bbox": block["bbox"],
            "page": page_num,
            "fontsize": fontzie

        }
        page_imge_array[y1:y2, x1:x2] = img
        # 显示图像



        return output


def pdf_page_to_image(path, page_num=0, sampling_rate=3):
    doc = head.fitz.open(path)
    page = doc[page_num]
    # 获取页面大小
    page_width, page_height = page.rect.width, page.rect.height

    matrix = head.fitz.Matrix(sampling_rate, sampling_rate)  # 等距缩放
    # 使用指定的采样率将页面转换为pixmap
    pix = page.get_pixmap(matrix=matrix)
    # 将pixmap转换为PIL图像
    pix_array = pixmap_to_PIL_image(pix)
    pix_1 = head.np.array(pix_array)
    return pix_1, page_width, page_height


def pixmap_to_PIL_image(pixmap):
    # 获取图像数据
    image_data = pixmap.samples
    # 创建PIL Image对象
    pil_image = head.Image.frombytes("RGB", [pixmap.width, pixmap.height], image_data)
    return pil_image


#
# def text_and_draw(page_block_list,page_num):
#     """
#     功能：画出一页上的全部框
#     参数：page_block_list 单页上的全部block
#     page_num：页数
#     返回值：直接展示画好的图
#     """
#     doc = head.fitz.open(head.path)
#     for i in page_block_list:
#         if i["page"] == page_num:
#             page = doc[i]
#             rect = head.fitz.Rect(i["bbox"])
#             page.draw_rect(rect)
#     doc.save("检测单页划分情况.pdf")
#
# def get_page_block(page_num,page):
#     """
#     功能:拿单页的全部block
#     参数说明:
#     page_num:页数
#     page:页面对象
#     """
#     text_dict = page.get_text("dict")  # 获取文本信息字典
#     return


page_num = 5
all_page_span = head.get_all_page_span(head.path)
page_image, _, _ = pdf_page_to_image(head.path,page_num)

for i in all_page_span:
    if i["page"] == page_num:
        block2array_shortcut(page_image, page_num, i)

        # cutout_dict = block2array_shortcut(page_image, page_num, i)
        # x1, y1, x2, y2 = [int(i) for i in cutout_dict["bbox"]]
        # print(cutout_dict)
        # if not cutout_dict["array"]:
        #     page_image[y1:y2, x1:x2] = cutout_dict["array"]
        #     head.plt.imshow(page_image)
        #     head.plt.show()

