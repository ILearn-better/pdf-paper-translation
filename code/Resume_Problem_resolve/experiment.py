import PyPDF2
def show_and_write_pdf(path):
    # try:
    # 打开一个 PDF 文件
    pdf_file = open(path, 'rb')
    # 创建一个 PDF 阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # 获取 PDF 文件的页数
    num_pages = len(pdf_reader.pages)
    # 循环遍历每一页
    name =path.split("\\")[-1]
    save_path = r"C:\Users\EDY\Desktop\project\pdf2md\code\Resume_md\Pypdf2效果_"+name
    with open(save_path+".md","w",encoding="utf-8") as file:
        for page in range(num_pages):
            # 获取当前页的对象
            pdf_page = pdf_reader.pages[page]
            # 提取当前页的文本
            text = pdf_page.extract_text()
            # 打印文本
            # print(text)
            file.write(text)

    # except:
    #     print('erro!!!!!!!!!!!')
def path_list():
    import os
    path_ = r"C:\Users\EDY\Desktop\project\pdf2md\code\Resume_md\简历\简历"
    p_list = []
    for i in os.listdir(path_):
        p_list.append(os.path.join(path_,i))
    return p_list


# pa_list = path_list()
# for i in pa_list:
#     show_and_write_pdf(i)

