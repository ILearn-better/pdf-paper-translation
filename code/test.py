import fitz
import head
from find_main_text import statistics_of_font_size,find_main_text_font_size,find_main_text
main_text_font_size = find_main_text_font_size(head.path)
main_text_span= find_main_text(head.path,main_text_font_size)

def test():
    doc = fitz.open(head.path)
    record_most_account = []
    for i in range(doc.page_count):
        statistics_of_font_size(doc[i])
test()


def test_1(span_list):
    """
    可视化正文提取情况
    """
    doc = fitz.open(head.path)
    for i in span_list:
        for j in i:
            print(j)
            page = doc[j["page"]]
            rect = fitz.Rect(j["bbox"])
            page.draw_rect(rect)
    doc.save("检测全文span分割情况_基于TEST.pdf.pdf")
test_1(main_text_span)