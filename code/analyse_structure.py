import head
"""
对单页pdf进行结构提取
流程:
    读取pdf，选择一页保存为图片
    对图片进行pdddleocr进行结构提取
"""
def save_page():
    doc =head.fitz.open(head.path)
    dp = doc[16].get_pixmap()
    dp.save(r"media/picture/png_16.png")
# save_page()
def process_page():
    """
    思路:
    1.图片读取2.结构提取
    :return:
    """
    import os
    import cv2
    from paddleocr import PPStructure,draw_structure_result,save_structure_res
    table_engine = PPStructure(show_log=True)

    save_folder=r'output/output_Picture'
    img_path = r'media/picture/png_16.png'
    img = cv2.imread(img_path)
    result = table_engine(img)
    save_structure_res(result,save_folder,os.path.basename(img_path).split('.')[0])
# process_page()
