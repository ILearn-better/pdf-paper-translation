############################################################################################################
import sys
sys.path.append("../")
#print(os.getcwd())
import head
from translate_and_shift_to_json import write_paragraph_into_txt
from flask import Flask, render_template, request,jsonify,send_file,make_response
from werkzeug.utils import secure_filename
from recover_structure import recover_structure_English,recover_structure_Chinese


app = Flask(__name__)
path = ""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pdf2html_dont_translate', methods=['GET', 'POST'])
def pdf2html_dont_translate():
    """
    传入pdf,输出html（未翻译的）
    """
    if request.method == 'POST':
        f = request.files['file']
        save_p = head.os.path.join(head.os.getcwd(),"media","input",secure_filename(f.filename))
        if head.os.path.basename(save_p)=="":
            """检测有无上传文件"""
            return make_response(404)
        else:
            f.save(save_p)
            head.path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/input")))
            recover_structure_English()
            result_file_path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)
            # return str(filename)

    else:
        return render_template("index.html")


@app.route('/pdf2html_translated', methods=['GET', 'POST'])
def pdf2html_translated():
    """
    传入pdf,输出html（翻译的,并还原好）
    """
    if request.method == 'POST':
        f = request.files['file']
        save_p = head.os.path.join(head.os.getcwd(),"media","input",secure_filename(f.filename))
        if head.os.path.basename(save_p)=="":
            """检测有无上传文件"""
            return make_response(404)
        else:
            f.save(save_p)
            head.path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/input")))
            recover_structure_Chinese()
            result_file_path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)
            # return str(filename)

    else:
        return render_template("index.html")


@app.route('/pdf_paragraph_to_txt', methods=['GET', 'POST'])
def pdf_paragraph_to_txt():
    """
    流程:读取文件->处理文件->处理完成后保存txt->发送文件地址
    :return:
    """
    if request.method == 'POST':
        f = request.files['file']
        save_p = head.os.path.join(head.os.getcwd(),"media","input",secure_filename(f.filename))
        if head.os.path.basename(save_p)=="":
            """检测有无上传文件"""
            return make_response(404)
        else:
            f.save(save_p)
            # data = {
            #     'status': 1,
            #     'message': 'This is an example API response',
            #     'data': {
            #         'example_key': 'example_value',
            #         'save_p':save_p
            #     }
            # }
            head.path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/input")))
            write_paragraph_into_txt()
            result_file_path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)

    else:
        return render_template("index.html")

#     需要添加逻辑：用户关闭页面就要把文件全部清除

@app.route('/pdf_paragraph_to_translationTxT', methods=['GET', 'POST'])
def pdf_paragraph_to_translationTxT():
    """
    流程:读取文件->处理文件->处理完成后保存txt->发送文件地址
    :return:
    """
    from translate import translate0
    if request.method == 'POST':
        f = request.files['file']
        save_p = head.os.path.join(head.os.getcwd(),"media","input",secure_filename(f.filename))
        if head.os.path.basename(save_p)=="":
            """检测有无上传文件"""
            return make_response(404)
        else:
            f.save(save_p)
            head.path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/input")))
            translate0()
            result_file_path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)

    else:
        return render_template("index.html")


@app.route('/pdf2md', methods=['GET', 'POST'])
def pdf2md():
    """
    传入pdf,输出markdown
    """
    from generate_markdown import pdf_to_markdown

    if request.method == 'POST':
        f = request.files['file']
        save_p = head.os.path.join(head.os.getcwd(),"media","input",secure_filename(f.filename))
        if head.os.path.basename(save_p)=="":
            """检测有无上传文件"""
            return make_response(404)
        else:
            f.save(save_p)
            head.path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/input")))
            save_1 = head.os.path.join(head.os.getcwd(),"media","output","output.md")
            pdf_to_markdown(head.path,save_1)
            result_file_path = head.os.path.join(head.os.getcwd(), get_latest_file(head.os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)

    else:
        return render_template("index.html")

def get_latest_file(path):
    """
    获取指定目录中最新的文件
    :param path: 目录路径
    :return: 最新文件的路径
    """
    # 获取目录中所有文件的列表
    files = [head.os.path.join(path, f) for f in head.os.listdir(path) if head.os.path.isfile(head.os.path.join(path, f))]
    # 按修改时间排序
    files.sort(key=lambda x: head.os.path.getmtime(x), reverse=True)
    # 返回最新的文件
    return files[0] if files else None


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5008)
# https://www.daehee.com/werkzeug-console-pin-exploit/
