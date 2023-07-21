import fitz
import head
from PIL import Image
import os
def extract_images(pdf_path):
    pdf = fitz.open(pdf_path)
    for page_index in range(pdf.page_count):
        page = pdf[page_index]
        # print(dir(page))
        #get_image_bbox:获取给定图像上的边界框', 'get_image_info', 'get_image_rects', 'get_images'
        # image_list = page.get_images()
        # print("Page.get_image_info:",page.get_image_info())
        image_ = page.get_image_info()
        # print("Image_list:",image_list)
        if image_:
            print(f"[INFO] Found a total of {len(image_)} images in page {page_index}")
            for coordinate in page.get_image_info():
                print(coordinate)
                rect = fitz.Rect(coordinate["bbox"])
                page.draw_rect(rect)

        else:
            print("[INFO] No images found on page", page_index)
    pdf.save("提取图片"+".pdf")
# extract_images(head.path)
"""
问题：有些图片不能很好检测到
"""

def extract_images_to_save_into_png(pdf_path,save_pic):
    """
    功能:
        在pdf上截图，并保存为png，并返回对应字典
    参数:
        pdf_path:head.path
        save_pic:是否保存图片,1是保存，0是不保存
    返回值:
        字典：png保存位置，box信息，所处页码

    """
    pdf = fitz.open(pdf_path)
    picture_list = []
    for page_index in range(pdf.page_count):
        page = pdf[page_index]
        image_ = page.get_image_info()
        if image_:
            print(f"[INFO] Found a total of {len(image_)} images in page {page_index}")
            for index,coordinate in enumerate(page.get_image_info()):
                pixmap = page.get_pixmap()
                # 将 Pixmap 对象转换为 Image 对象
                # print(pixmap.samples)
                img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
                cropped_pix = img.crop(coordinate["bbox"])



                save_name=f"In page {page_index} imagen {index}"
                save_path=os.path.join(os.getcwd(),"media","other_out_media","pic",save_name+'.png')#注意修改
                if save_pic:
                    try:
                        cropped_pix.save(save_path)
                    except:
                        # print(cropped_pix.shape)
                        continue
                        # print("+++" * 7)
                        # print(cropped_pix)
                        # arr_ = head.np.array(cropped_pix)
                        # print(arr_.shape)
                        # head.plt.imshow(arr_)
                        # head.plt.show()

                save_pic_dict={
                    "save_path":save_path,
                    "bbox":coordinate["bbox"],
                    "page":page_index,
                    "type":"image"
                }
                picture_list.append(save_pic_dict)

        else:
            # print("[INFO] No images found on page", page_index)
            pass
    return picture_list
# picture_list = extract_images_to_save_into_png(head.path,1)
# print(picture_list)
# print(len(picture_list))
"""
比较一下保存的图片和len值即可验证是否正确
"""