"""
单页实验:
1.
做原本的span恢复+翻译+中文结构恢复（html）
2.
做布局重排
"""
import os
import re
from collections import Counter

import fitz

from process_page_function import pdf_page_to_image, pdfkit_html_to_PDF, get_page_main_spansize,get_one_page_span,get_block_text
from logger import logger
# from ChatGPT_API import GPT_API#此处的IP映射会影响对翻译API的调用
from translate_interface import interface_to_dict,GPTinterface_to_dict
import cv2

"""
拿全文span
画全文span截图信息（检测）
拿单页进行复原
"""


###################################################################


###################################################################
# 功能函数定义
def draw_page_span(page_image, page_block, save_path: str):
    """
    功能:绘制span box的信息
    参数:
        page:page对象
        page_span:page对应的block信息
    :param page_span:
    :return:
    """
    print(type(page_image))
    for i in page_block:
        x0, y0 = [int(i) for i in i["bbox"][:2]]
        x1, y1 = [int(i) for i in i["bbox"][2:4]]
        # print("x0,y0,x1,y1:", x0, y0, x1, y1)
        cv2.rectangle(page_image, (x0, y0), (x1, y1), (255, 0, 0), 1)
    # save_path = os.path.join("media", "output", pic_num+"_"+"drwa_bo_into_page.png")
    save_path = os.path.join(save_path, "drwa_bo_into_page.png")
    cv2.imwrite(save_path, page_image)
    return page_image


def recover_without_translation(page_block, page_width, page_height, htmlorpng_folder, name="s"):
    """
    功能:恢复页面结构
    参数说明:
    :param page_block:page的block信息
    :param page_width:page宽
    :param page_height:page高
    :param name:文件命名
    :return:
    """
    html_path = os.path.join(htmlorpng_folder, name + "recover.html")
    # if os.path.exists(txt_path): return txt_path
    rate = 1.0

    with open(html_path, "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<head>")
        file.write("</head>")
        file.write(
            "<div id=\"{}\" style=\" position: relative;width: {}px;height: {}px;margin: 0px; border:1px solid #000\">".format(
                str(1) + "-page第一层", page_width * rate, page_height * rate))
        for block in page_block:
            # print(block)
            x0, y0, x1, y1 = block["bbox"]
            if block["type"] == "image":
                # if "image" in block.keys():
                #     show_path = os.path.join(os.getcwd(), "media", "output",
                #                                   os.path.basename(block["save_path"]))  # 检测block有没有save_path字段
                show_path = block["text"]
                file.write(
                    "<img id=\"{}\" alt=\"pic\" src=\"{}\" style=\"position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;\"/>".format(
                        str(2) + "-page第二层", show_path, y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))
            else:

                file.write(
                    "<div style=\"position: absolute;top: {}px;left: {}px;width:{}px;height:{}px;word-wrap:break-word;\">".format(
                        y0 * rate, x0 * rate, (x1 - x0) * rate, (y1 - y0) * rate))
                out = get_block_text(block)
                print("拿到blcok的文本并输出out:", out)
                if len(out) == 2:
                    textt, fontsize = out
                    file.write("<p style=\"font-size:{}px\">".format(fontsize))
                    print("len(out) == 2时的输出:",textt)
                    file.write(textt)
                    file.write("</p>")
                    file.write("</div>")
                else:
                    textt = out
                    print("len(out) != 2时的输出:",textt)
                    file.write("<p style=\"font-size:{}\">".format(block["size"]))
                    file.write(textt)
                    file.write("</p>")
                    file.write("</div>")
    return html_path


def Temporary_character_substitution(s):
    """
    功能：英文转中文（暂时）
    :param s:
    :return:
    """
    l = len(s.split(" "))
    ch = "中" * l
    return ch


######
# 判断字符串是中文还是英文
def is_chinese(s):
    for char in s:
        # 中文字符的 Unicode 范围为：[\u4e00-\u9fff]
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


######

def main(pdf_path, data_dict, user_folder_path_dict):
    """

    :param  pdf_path:下载后保存的pdf路径
    :param data_dict:接收的传输字典
    :param user_folder_path_dict:各功能文件夹路径
    :return:
    """

    htmlorpng_folder = user_folder_path_dict["userhtmlorpng"]
    # inputpdf_folder = user_folder_path_dict["userinputpdf"]
    outputpdf_folder = user_folder_path_dict["useroutput"]

    doc = fitz.open(pdf_path)
    page_n = 0  # 用于合并pdf
    pdf_name = []  # 用于合并pdf
    for i in range(doc.page_count):
    # for i in [6]:
        print("============================开始第{}页的处理======================".format(i))
        page = doc[i]
        page_block = get_one_page_span(page, i)
        page_image, page_width, page_height = pdf_page_to_image(path=pdf_path, page_num=i, sampling_rate=1)
        page_width, page_height = round(page_width), round(page_height)
        draw_page_span(page_image, page_block, htmlorpng_folder)
        ##############################################################
        # 待完善
        # fontsize_list = []
        # for i in page_block:
        #     print("font size:", i["size"])
        #     logger.info("font size:{}".format(str(i["size"])))
        #     fontsize_list.append(i["size"])
        ##############################################################
        text_region = page.get_text_blocks()
        # print("text_region:", text_region)
        # logger.info("text_region:{}".format("拿到单页元素字典"))

        ##############################################################
        def get_fontsize_list(page):
            """
            获取page中各个block的font size，没有font size的block新建key并赋值
            :param page:
            :return:
            """
            text_dict = page.get_text("dict")  # 获取文本信息字典,是一类的font size的放一起
            # print("text_dict:", text_dict.keys())
            # 给文本block设定fontsize
            text_fontsize = []
            for block in text_dict["blocks"]:
                block_max_fontsize = []
                # print(block)
                if block["type"] == 0:
                    if not "text" in block.keys():
                        for line in block["lines"]:
                            # print(line)
                            for span in line["spans"]:
                                # print("span text:{}".format(span["text"]))
                                block_max_fontsize.append(span["size"])
                        block["size"] = sorted(dict(Counter(block_max_fontsize)).items(), key=lambda x: x[1])[-1][0]

                        text_fontsize.append(block["size"])
                    if "text" in block.keys():
                        # print("block text:{}".format(block["text"]))
                        text_fontsize.append(block["size"])

                if block["type"] == 1:  # 图片的size字段为-1
                    block["size"] = -1
                    text_fontsize.append(block["size"])
            print(
                "地址:{},全页文本block数量(get_text方法):{},全页文本block数量(get_text_blocks方法):{}".format(__file__,
                                                                                                              len(
                                                                                                                  text_dict[
                                                                                                                      "blocks"]),
                                                                                                              len(text_region)))
            print("地址:{},text_fontsize的长度:{},检测text_font size 与全页的block数量是否相同:{}".format(__file__,
                                                                                                          len(text_fontsize),
                                                                                                          len(text_fontsize) == len(
                                                                                                              text_dict[
                                                                                                                  "blocks"])))
            print(
                "地址:{},全页文本span dict keys(get_text方法):{},全页文本span dict keys(get_text_blocks方法):{}".format(
                    __file__, text_dict["blocks"][0].keys(), text_region[0]))
            print("地址:{},全页文本span dict keys(type-image):{},全页文本span dict keys(type-text):{}".format(__file__,
                                                                                                              text_dict[
                                                                                                                  "blocks"][
                                                                                                                  0][
                                                                                                                  "type"],
                                                                                                              text_dict[
                                                                                                                  "blocks"][
                                                                                                                  1][
                                                                                                                  "type"]))
            return text_fontsize

        text_fontsize = get_fontsize_list(page)
        print("text_fontsize:",text_fontsize)
        ##############################################################
        page_block_translated = []
        for index, block_n in enumerate(text_region):
            if re.search(r".image.*width.*height.*bpc:", block_n[-3]):#识别图片block
                #################################################################
                # 思路1:由block_n[:4]截图（page转图片<page_image>->page_image上截图->保存到制定路径->返回路径）并保存，返回图片路径
                x0, y0, x1, y1 = [abs(int(val)) for val in block_n[:4]]
                #坐标会小于0,小于0的坐标直接取0
                picture_save_path = os.path.join(os.getcwd(), "media", "HTMLorPNG_folder", str(data_dict["userId"]),
                                                 str(index) + ".png")
                # print(page_image[y0:y1, x0:x1],"++++++++++++++++++")
                cv2.imwrite(picture_save_path, page_image[y0:y1, x0:x1])

                # if page_image[y0:y1, x0:x1]:
                #     cv2.imwrite(picture_save_path, page_image[y0:y1, x0:x1])
                # else:
                #     import numpy as np
                #     cv2.imwrite(picture_save_path,np.zeros((y1-y0,x1-x0)))
                # 思路2:利用pymupdf自带的工具覆盖和处理(实验)

                #################################################################

                page_block_translated.append({
                    "text": picture_save_path,
                    "bbox": block_n[:4],
                    "size": str(text_fontsize[index]),
                    "type": "image"
                })
                print(__file__, "图片路径box:", picture_save_path)
                logger.info("地址:{},图片在文章位置路径:第{}页，第{}个block".format(__file__, i, index))
            else:
                before_translated = block_n[-3].replace("\n", " ").rstrip()
                print("当前文本页数:{},翻译前的文本:{}".format(i,before_translated))
                translated_str = interface_to_dict(before_translated)["data"]
                #####################################################
                #切分传入前的字符
                # if len(before_translated.split(" "))>50:
                #     print("当前文本页数:{}，当前文本长度超过50个词".format(i))
                #     logger.info("当前文本页数:{}，当前文本长度超过50个词".format(i))
                #
                #     sentence_list = before_translated.split(".")  # 将翻译字符串按"."化分句子
                #     print("sentence_list:", sentence_list)
                #     print("长度sentence_list的长度：",sentence_list)
                #     l = len(sentence_list)  # 划分出的句子个数
                #
                #     s = []  # 存per个part
                #     per = 2  #
                #     for n in range(per):
                #         paraph = ""  # 合并每part句子
                #         for p in sentence_list[round(l / per) * n:round(l / per) * (n + 1)]:
                #             paraph = paraph + p
                #         s.append(paraph)
                #
                #     translated_str_p = ""  # 合并每part翻译好的文本
                #     for E_p in s:
                #         print("带入翻译的句子长度:",E_p)
                #         ts = interface_to_dict(E_p)
                #         # ts = GPTinterface_to_dict()
                #         translated_str_p = translated_str_p + ts["data"]
                #     translated_str = translated_str_p
                # #####################################################
                # else:
                #     logger.info("当前文本页数:{},翻译前的文本:{}".format(i,"before_translated后台打印，不写入日志"))
                #     # translated_str = GPTinterface_to_dict(block_n[-3].replace("\n", "").rstrip())["data"]
                #     translated_str = interface_to_dict(block_n[-3].replace("\n", "").rstrip())["data"]
                #
                #     print(translated_str)
                #     ##################################################################################
                #     # 判断字符串是否是中文,不为中文则分割，为中文则继续执行
                #     # 逻辑问题:若为但个字符也每翻译怎么办？建议用字符长度作为依据
                #     # if not is_chinese(translated_str) or len(translated_str.split[" "])>40:  # 检测不为中文则分割或则词汇大于41
                #
                #     # if not is_chinese(translated_str):  # 检测不为中文则分割
                #     #     """
                #     #     分割规则:
                #     #         将该句段分为2部分
                #     #     """
                #     #     sentence_list = translated_str.split(".")  # 将翻译字符串按"."化分句子
                #     #     print("sentence_list:",sentence_list)
                #     #     l = len(sentence_list)  # 划分出的句子个数
                #     #
                #     #     s = []  # 存per个part
                #     #     per = 2  #
                #     #     for n in range(per):
                #     #         paraph = ""  # 合并每part句子
                #     #         for p in sentence_list[round(l / per) * n:round(l / per) * (n + 1)]:
                #     #             paraph = paraph + p
                #     #         s.append(paraph)
                #     #
                #     #     translated_str_p = ""  # 合并每part翻译好的文本
                #     #     for E_p in s:
                #     #         # ts = GPTinterface_to_dict(E_p)
                #     #         ts = interface_to_dict(E_p)
                #     #
                #     #         translated_str_p = translated_str_p + ts["data"]
                #     #     translated_str = translated_str_p
                ##################################################################################
                print("当前文本页数:{}，translated_str:{}".format(i,translated_str))
                logger.info("当前文本页数:{}，translated_str:{}".format(i,translated_str))

                ###########################################
                #防止span size过大严重影响排版
                if text_fontsize[index]>100:
                    page_block_translated.append({
                        "text": "",
                        "bbox": block_n[:4],
                        "size": str(text_fontsize[index]),
                        "type": "text"
                    })
                else:
                    page_block_translated.append({
                        "text": translated_str,
                        "bbox": block_n[:4],
                        "size": str(text_fontsize[index]),
                        "type": "text"
                    })
                ###########################################

        print("D", page_block_translated)
        logger.info("page_block_translated:%s" % page_block_translated)
        ##################################################################################
        print(__file__, "准备获取单页最多的font size.....GML翻译结果....")
        logger.info("地址:{},message:{}".format(__file__, "准备获取单页最多的font size........."))
        page_most_font_size = get_page_main_spansize(page)
        print(__file__, "已经获取单页最多的font size")
        logger.info("地址:{},message:{}".format(__file__, "已经获取单页最多的font size"))
        # 对page_block_translated进行筛选，若小于page_most_font_size则不显示
        new_translated_page_block = []
        for block in page_block_translated:
            if block["size"] and int(float(block["size"])) >= page_most_font_size:
                new_translated_page_block.append(block)
        print(__file__, "已生成的new_translated_page_block")
        logger.info("地址:{},message:{}".format(__file__, "已生成的new_translated_page_block"))
        ##################################################################################
        print("准备进行格式恢复... ...")
        logger.info("地址:{},message:{}".format(__file__, "准备进行格式恢复... ..."))

        html_spath = recover_without_translation(page_block_translated, page_width, page_height, htmlorpng_folder, "Ch")
        print("翻译后的HTML输出完成，路径为:{}".format(html_spath))
        logger.info("翻译后的HTML输出完成，路径为:{}".format(html_spath))
        ##################################################################################

        # print("html_spath:", html_spath)
        name = data_dict["fileName"] + "_" + str(page_n) + "_" + os.path.basename(html_spath).split('.')[0] + '.pdf'
        outpath = os.path.join(outputpdf_folder, name)
        # print(outpath)

        pdf_name.append(name)

        # 保存PDF文件
        print("page_width,page_height:", page_width, page_height)
        logger.info("page_width:{},page_height:{}".format(str(page_width), str(page_height)))

        # pdfkit_html_to_PDF(html_spath, outpath,page_width,page_height)
        pdfkit_html_to_PDF(html_spath, outpath, page_width, page_height)

        print("翻译后的HTML to PDF转换完成,路径为:{}".format(outpath))
        logger.info("翻译后的HTML to PDF转换完成,路径为:{}".format(outpath))
        page_n = page_n + 1
        ####################################################################
        print("=================结束第{}页的处理=================".format(i))
    ########################################################################

    # 做PDF拼接
    doc_conbine = fitz.open()
    pdf_path_list = [os.path.join(outputpdf_folder, i) for i in pdf_name]
    for p in pdf_path_list:
        print("num_pdf_path:", p)
        doc_p = fitz.open(p)
        doc_conbine.insert_pdf(doc_p, 0)

    doc_conbine_savepath = os.path.join(outputpdf_folder, data_dict["fileName"] + ".pdf")
    doc_conbine.save(doc_conbine_savepath)
    #######################################################################
    return doc_conbine_savepath


############################################################################
# if __name__ == "__main__":
#     # main()
#     pass
############################################################################
# recover_without_translation(page_block)
if __name__ == "__main__":
    ###########################################################################################
    # 做原本的span恢复
    ## HTML方法 #################
    # translated_page_block = []
    # for i in page_block:
    #     translated = Temporary_character_substitution(i["text"])#英文转中文（暂时）
    #     i["text"] = translated
    #     translated_page_block.append(i)
    # recover_without_translation(translated_page_block, page_width, page_height)

    ## 图像方法#################
    # 找文字最大轮廓；
    # from paddleocr import PaddleOCR
    # ocr = PaddleOCR()
    # table = ocr.ocr(page_image)
    # print(table)
    # for j in table:
    #     for i in j:
    #         print(i)
    #         x0,y0=i[0][0][0],i[0][0][1]
    #         x1,y1=i[0][2][0],i[0][2][1]
    #         cv2.rectangle(page_image,(int(x0),int(y0)),(int(x1),int(y1)),(255,0,0),1)
    # plt.imshow(page_image)
    # plt.show()
    ###########################################################################################
    # 读取pdf
    # 拿page_block和page_image
    # 恢复英文结构
    # 拿相同span
    # 逐text翻译
    pdf_path = "/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/AI could create a (1).pdf"
    page_num = 8
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    page_block = get_one_page_span(page, page_num)
    # print("page_block:", page_block)
    page_image, page_width, page_height = pdf_page_to_image(path=pdf_path, page_num=page_num, sampling_rate=1)
    page_width, page_height = round(page_width), round(page_height)
    # print("page_width:{}, page_height:{}".format(page_width, page_height))
    # recover_without_translation(page_block, page_width, page_height,"En")
    ###########################################################################################
    # 绘制展示page的box的展示截图（check）
    # draw_page_span(page_image, page_block)
    # pymupdf自带方法实验 ########################################################################
    text_reg = page.get_text_blocks()


    # 给文本block设定fontsize
    def get_fontsize_list(page):
        """
        获取page中各个block的font size，没有font size的block新建key并赋值
        :param page:
        :return:
        """
        text_dict = page.get_text("dict")  # 获取文本信息字典,是一类的font size的放一起
        print("text_dict:", text_dict.keys())

        # 给文本block设定fontsize
        text_fontsize = []
        for block in text_dict["blocks"]:
            block_max_fontsize = []
            # print(block)
            if block["type"] == 0:
                if not "text" in block.keys():
                    for line in block["lines"]:
                        # print(line)
                        for span in line["spans"]:
                            print("span text:{}".format(span["text"]))
                            block_max_fontsize.append(span["size"])
                    block["size"] = max(block_max_fontsize)
                    text_fontsize.append(block["size"])
                if "text" in block.keys():
                    print("block text:{}".format(block["text"]))
                    text_fontsize.append(block["size"])

            if block["type"] == 1:  # 图片的size字段为-1
                block["size"] = -1
                text_fontsize.append(block["size"])
        print("地址:{},全页文本block数量(get_text方法):{},全页文本block数量(get_text_blocks方法):{}".format(__file__,
                                                                                                            len(
                                                                                                                text_dict[
                                                                                                                    "blocks"]),
                                                                                                            len(text_reg)))
        print("地址:{},text_fontsize的长度:{},检测text_font size 与全页的block数量是否相同:{}".format(__file__,
                                                                                                      len(text_fontsize),
                                                                                                      len(text_fontsize) == len(
                                                                                                          text_dict[
                                                                                                              "blocks"])))

        print("地址:{},全页文本span dict keys(get_text方法):{},全页文本span dict keys(get_text_blocks方法):{}".format(
            __file__, text_dict["blocks"][0].keys(), text_reg[0]))
        print("地址:{},全页文本span dict keys(type-image):{},全页文本span dict keys(type-text):{}".format(__file__,
                                                                                                          text_dict[
                                                                                                              "blocks"][
                                                                                                              0][
                                                                                                              "type"],
                                                                                                          text_dict[
                                                                                                              "blocks"][
                                                                                                              1][
                                                                                                              "type"]))
        return text_fontsize


    text_fontsize = get_fontsize_list(page)
    print("地址:{},全页文本font size:{}".format(__file__, text_fontsize))
    # ##################################################################################################
    # a = page.get_text()#拿文本
    # print("page.get_text()：",a.rstrip())
    # b = page.get_text_blocks()#拿文本块
    # print("page.get_text_blocks():",b)
    # print("===" * 90)
    # s = page.get_text_selection((90.0, 91.93089294433594), (730, 330))
    # print("===" * 90)
    # print("page.get_text_selection:", s)
    # print("===" * 90)
    # t = page.get_textbox((90.0, 91.93089294433594, 400, 400.75003051757812))#通过box拿文本
    # print("t:", t)
    # f = page.get_fonts()
    # print(f)
    # print(len(f))
#     ###########################################################################################
#     # 做单栏-行间距小-纯文本的font size 区分：font size一样且间距较小的为一类
#     # structure= {
#     #     "TOC":[],
#     #     "main":[],
#     # }
#     # fontsize=[]
#     # f = page.get_fonts()
#     # for i in page_block:
#     #     if i["size"]==
#     ###########################################################################################
#     # 走完单页翻译流程（段落不合并，逐行翻译）
#     # page_block_translated = []
#     # for i in page_block:
#     #     if "text" in i.keys():
#     #         if len(i["text"]) >= 5:
#     #             translated_text = interface_to_dict(i["text"])
#     #             # print("translated_text:",translated_text)
#     #             i["text"] = translated_text["data"]
#     #             print(i["text"])
#     #             page_block_translated.append(i)
#     #         if len(i["text"]) == 0:
#     #             pass
#     #         if len(i["text"]) < 5 and len("text") > 0:
#     #             """向下合并"""
#     #             page_block_translated.append(i)
#     # # print(page_block_translated)
#     # html_spath = recover_without_translation(page_block_translated, page_width, page_height, "Ch")
#     # logger.info("翻译后的HTML输出完成，路径为:{}".format(html_spath))
#     #
#     # # print("html_spath:", html_spath)
#     # name = os.path.basename(html_spath).split('.')[0] + '.pdf'
#     # outpath = os.path.join("media", "output", name)
#     # # print(outpath)
#     #
#     # # 保存PDF文件
#     # pdfkit_html_to_PDF(html_spath, outpath)
#     # logger.info("翻译后的HTML to PDF转换完成,路径为:{}".format(outpath))
#     ###########################################################################################
#     # 完善单页翻译结果（段落合并，成块翻译）
#     """
#     思路：用get_text_blocks
#     """
#     fontsize_list = []
#     for i in page_block:
#         print("font size:", i["size"])
#         logger.info("font size:{}".format(str(i["size"])))
#         fontsize_list.append(i["size"])
#
#
#     text_region = page.get_text_blocks()
#     print("text_region:", text_region)
#     logger.info("text_region:{}".format("拿到文本字典了"))
#
#     page_block_translated = []
#     for i in text_region:
#         before_translated = i[-3].replace("\n", "").rstrip()
#         print("翻译前的文本:",before_translated)
#         logger.info("翻译前的文本:{}".format("已打印该文本"))
#
#
#         translated_str = interface_to_dict(i[-3].replace("\n","").rstrip())["data"]
#         ##################################################################################
#         #判断字符串是否是中文,不为中文则分割，为中文则继续执行
#         if not is_chinese(translated_str):#检测不为中文则分割
#             """分割规则:将该句段分为3部分"""
#             sentence_list = translated_str.split(".")#将翻译字符串按"."化分句子
#             l = len(sentence_list)#划分出的句子个数
#
#             s = []#存3个part
#             for n in range(3):
#                 paraph =""#合并每part句子
#                 for p in sentence_list[round(l / 3)*n:round(l / 3)*(n+1)]:
#                     paraph = paraph+p
#                 s.append(paraph)
#
#             translated_str_p = ""#合并每part翻译好的文本
#             for E_p in s:
#                 ts = interface_to_dict(E_p)
#                 translated_str_p = translated_str_p+ts["data"]
#             translated_str = translated_str_p
#         ##################################################################################
#         print("translated_str:",translated_str)
#         logger.info("translated_str:{}".format(translated_str))
#
#         page_block_translated.append({
#             "text": translated_str,
#             "bbox": i[:4],
#             "size": "10"
#         })
#
#     print("page_block_translated:",page_block_translated)
#     logger.info("page_block_translated:%s" % page_block_translated)
#
#     # print(page_block_translated)
#     html_spath = recover_without_translation(page_block_translated, page_width, page_height, "Ch")
#     logger.info("翻译后的HTML输出完成，路径为:{}".format(html_spath))
#
#     # print("html_spath:", html_spath)
#     name = os.path.basename(html_spath).split('.')[0] + '.pdf'
#     outpath = os.path.join("media", "output", name)
#     # print(outpath)
#
#     # 保存PDF文件
#     print("page_width,page_height:",page_width,page_height)
#     logger.info("page_width:{},page_height:{}".format(str(page_width),str(page_height)))
#
#     # pdfkit_html_to_PDF(html_spath, outpath,page_width,page_height)
#     pdfkit_html_to_PDF(html_spath, outpath,page_width,page_height)
#
#     logger.info("翻译后的HTML to PDF转换完成,路径为:{}".format(outpath))
