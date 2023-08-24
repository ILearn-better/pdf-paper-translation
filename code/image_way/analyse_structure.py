"""
画文本轮廓
"""
import sys

sys.path.append("../")
import head
from tools_function import get_one_page_span
from process_page_function import pdf_page_to_image
pdf_path = r"C:\Users\EDY\Desktop\project\pdf2md\code\interface\media\input\ce.pdf"
page_num = 0
doc = head.fitz.open(pdf_path)
page = doc[page_num]
page_block = get_one_page_span(page, page_num)

print("page_block:", page_block[5].keys())
print("page_block font size:", page_block[5]["size"])

page_image, page_width, page_height = pdf_page_to_image(path=pdf_path, page_num=page_num, sampling_rate=1)
head.plt.imshow(page_image)
head.plt.show()
for i in page_block:
    # print(i["bbox"])
    x0,y0=[int(j) for j in i["bbox"][:2]]
    x1,y1=[int(j) for j in i["bbox"][2:4]]
    head.cv2.rectangle(page_image,(x0-10,y0-10),(x1+10,y1+10),(255,0,0),1)
head.plt.imshow(page_image)
head.plt.show()

blurred_image = head.cv2.GaussianBlur(page_image, (3, 3), 0)
head.plt.imshow(blurred_image)
head.plt.show()

edges = head.cv2.Canny(blurred_image, 30, 100)
head.plt.imshow(edges)
head.plt.show()

# 查找轮廓
contours, _ = head.cv2.findContours(edges, head.cv2.RETR_EXTERNAL, head.cv2.CHAIN_APPROX_SIMPLE)
# 在原图上绘制轮廓
image_with_contours = blurred_image.copy()
head.cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)
head.plt.imshow(image_with_contours)
head.plt.show()
