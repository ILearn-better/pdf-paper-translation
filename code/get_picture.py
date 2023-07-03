import fitz
import head
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
extract_images(head.path)
"""
问题：有些图片不能很好检测到
"""