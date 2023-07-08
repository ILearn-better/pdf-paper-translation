import os
import fitz
from collections import Counter
from find_main_text import statistics_of_font_size,find_main_text_font_size,find_main_text
from find_TOC import find_fontsize_bigger_than_main_fontsize,Choose_TOC_span,start_from_first_biggest_number,filter_TOC_span,recovery_order_via_dict
from find_paragraph import find_border_of_page,get_block,get_main_text_block,get_line,find_border_of_line
from get_picture import extract_images,extract_images_to_save_into_png
from get_other_font import find_other_font
from tools_function import get_paper_path,get_one_page_span,get_all_page_span,draw_pdf1,draw_pdf2,get_block
import json
import re
import pdfplumber
from openpyxl import Workbook
from PIL import Image
import cv2
import numpy as np
# global path
# path =r"./media/Attention is all you need.pdf"
path =r"C:\Users\EDY\Desktop\project\pdf2md\code\media\AI could create a .pdf"
# path =r"./media/TEST.pdf"
# path =r"C:\Users\EDY\Desktop\project\pdf2md\code\media\Calibrating distribution models from PELVE.pdf"
"""
可以写一个功能函数:
    自动收集所有文件当中函数，并添加到头head中，便于其他文件引用
"""
Json_save_path = r"C:\Users\EDY\Desktop\project\pdf2md\code\output\pdf_to_json.json"



