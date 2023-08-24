# 版式检测
#####################################################
# 表格检测

#####################################################
import fitz
from logger import logger


def specify_retention_page_count(pdfPath, *args):
    """
    功能:根据所给范围，保存对应page
    功能补充：任意的page tuple，例如(5,3,2,1)也能保存
    *args:所需要保存的页数范围，可为单个int，也可为元组
    pdfPath:pdf文件路径
    :return:
    """
    args = [i - 1 for i in args]
    doc = fitz.open(pdfPath)
    if max(args) > doc.page_count - 1 or min(args) < 0:
        print("出入参数越界！")
        return False

    if len(args) >= 2:
        # doc.page_count
        print(args)
        if args[0] == 0 and args[1] == doc.page_count - 1:
            doc.save("selected_pdf.pdf")
            return 1
        elif args[0] == 0:
            doc.delete_pages(args[1] + 1, doc.page_count - 1)
            doc.save("selected_pdf.pdf")
            return 1
        elif args[1] == doc.page_count - 1:
            doc.delete_pages(0, args[0] - 1)
            doc.save("selected_pdf.pdf")
            return 1
        else:
            doc.delete_pages(0, args[0] - 1)
            doc.delete_pages(args[1], doc.page_count - 1)
            doc.save("selected_pdf.pdf")
    if len(args) == 1:
        if args[0] == -1:
            print("page save fail")
            logger.info("page save fail")
            return False
        print("开始保存所选页数......")
        logger.info("开始保存所选页数......")
        print("地址:{},参数:{}".format(__file__, args))
        print("地址:{},该pdf总页数:{}".format(__file__, doc.page_count))

        if args[0] == 0:
            doc.delete_pages(1, doc.page_count - 1)
            doc.save("selected_pdf.pdf")
            return 1
        elif args[0] == doc.page_count - 1:
            doc.delete_pages(0, doc.page_count - 2)
            doc.save("selected_pdf.pdf")
            return 1

        else:
            doc.delete_pages(0, args[0] - 1)
            print("地址:{},第一次处理后pdf剩余页数:{}".format(__file__, doc.page_count))
            doc.delete_pages(1, doc.page_count - 1)
            doc.save("selected_pdf.pdf")
            return 1
        print("所选页数保存完毕......")
        logger.info("所选页数保存完毕......")
    # doc.delete_pages(0, 1)
    # new_pdf.insert_page(0,"sd")
    # doc.save('sd.pdf')


import os

if __name__ == "__main__":
    pdf_path = r"/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/21180.pdf"
    specify_retention_page_count(pdf_path, 2)  # 边界设置还有点问题
