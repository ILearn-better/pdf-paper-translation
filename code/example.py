#PDFminer、PDFplumber、PyMuPDF
# 获取 span 中文字的 font size
import fitz  # PyMuPDF

path = r"./media/Financial Sector Taxation.pdf"


doc = fitz.open(path)  # 打开PDF文件

page = doc[0]  # 选择第一页

text = page.get_text("text")  # 获取文本内容

fonts = page.get_fonts()  # 获取所有字体



for font in fonts:
    print(font)
    #
    # span = text.split(font["name"])  # 将文本按字体名称分割成多个span
    #
    # for span in span:
    #
    #     font_size = font["size"]  # 获取字体大小
    #
    #     print(f"{span} has a font size of {font_size}")

