import pdfkit
def pdfkit_html_to_PDF(html_file, output_pdf_path):
    """
    pdfkit方法
    """
    # 配置Wkhtmltopdf的路径
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    # HTML文件的路径
    options = {
        'quiet': '',
        'dpi': 75,
        'javascript-delay': '2000',  # 延时2s，echarts画图需要时间
        # 'minimum-font-size': '24',  # 字体大小
        # 'footer-right': 'xx有限公司',  # 页脚
        # 'footer-font-size': 10,  # 页脚字体大小
        # 'footer-spacing': 20,  # 页脚距离正文距离
        # 'footer-line': '',  # 页脚显示与正文分割线
        # 'margin-bottom': 25,  # 正文与底部距离
        'encoding': 'UTF-8',
        "enable-local-file-access": None,
        'image-quality': 500  # 当使用 jpeg 算法压缩图片时使用这个参数指定的质量(默认为 94)  解决分式位置上移问题，原因不清楚，猜测：公式被转成类似图片
        # 'no-pdf-compression': '',
    }

    # 使用pdfkit将HTML转换为PDF，并传入配置
    pdfkit.from_file(html_file, output_pdf_path, options=options, configuration=config)
    """
    pdfkit问题解决方案:
    https: // blog.csdn.net / weixin_54644396 / article / details / 113055065
    """

if __name__ == "__main__":
    # Usage example
    html_file_path = r"C:\Users\EDY\Desktop\pic_121.html"
    # 指定输出 PDF 文件的路径和文件名
    output_pdf_path = r"C:\Users\EDY\Desktop\pic121.pdf"
    # output_pdf_path = r"1output.pdf"

    # html_to_pdf(html_file_path, output_pdf_path)
    pdfkit_html_to_PDF(html_file_path, output_pdf_path)
