import head
from find_main_text import find_main_text_font_size
"""
简单的pdf转markdown：
将所有span逐个放置到markdown
"""
#恢复本文和字号
"""

"""
import fitz

def pdf_to_markdown(pdf_path, markdown_path):
    doc = fitz.open(pdf_path)
    main_text_size=find_main_text_font_size(head.path)
    with open(markdown_path, 'w', encoding='utf-8') as md_file:
        for i in range(doc.page_count):
            page=doc[i]
            # print(dir(page))
            text_dict = page.get_text("dict")
            for block in text_dict["blocks"]:
                if block["type"]==0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            # print(span)
                            if span["size"]>main_text_size:
                                md_file.write(span["text"])
                            if span["size"]==main_text_size:
                                md_file.write(span["text"])
                    md_file.write("\n")

    doc.close()

# 提供 PDF 文件路径和输出 Markdown 文件路径
pdf_path = head.path
markdown_path = "output.md"

# 调用函数将 PDF 转换为 Markdown
pdf_to_markdown(pdf_path, markdown_path)
