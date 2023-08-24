import sys
# sys.path.append("../")
import head as headPath
from translate_and_shift_to_json import write_paragraph_into_txt
from flask import Flask, render_template, request, jsonify, send_file, make_response, Response, abort
from werkzeug.utils import secure_filename
from recover_structure import recover_structure_English, recover_structure_Chinese
from interface.logger import logger
import os
from interface import global_param

# from .interface.print_function import print_and_logger
#################################################################
# 参数设置
if global_param.MODE == "PRO":
    pdf_save_path_param = 1  # 正式环境
    print(__file__, "==========当前是正式环境==========")
    logger.info("地址:{},==========当前是正式环境==========".format(__file__))
else:
    pdf_save_path_param = 0  # 开发环境
    print(__file__, "==========当前是开发环境==========")
    logger.info("地址:{},==========当前是开发环境==========".format(__file__))

#################################################################

app = Flask(__name__)


##################################################################################
@app.route('/pdf_path', methods=['GET', 'POST'])
def pdf_path():
    """
    上传文件并保存在本地
    """
    if request.method == 'POST':
        f = request.files['file']
        save_p = os.path.join("media", "input", secure_filename(f.filename))
        if os.path.basename(save_p) == "":
            """检测有无上传文件"""
            return jsonify({
                "status": 1,
                "msg": "没传文件"
            })
        else:
            f.save(save_p)
            headPath.path = save_p
            return jsonify({
                "status": 0,
                "msg": "文件上传成功",
                "data": save_p
            })

    else:
        return jsonify({
            "status": 0,
            "msg": "没接收到post请求"
        })


def test_folder():
    """
    检测是否存在output文件夹
    """
    path = os.path.join(os.getcwd(), "media", "output")
    if not os.path.isfile(path):
        # print("not this file.test if exits this folder")
        if not os.path.exists(path):
            # print("文件夹不存在，代创建。。")
            os.mkdir(path)
            # print("文件夹创成功。")
        else:
            print("文件夹存在")


@app.route('/pdf2html_dont_translate', methods=['GET', 'POST'])
def pdf2html_dont_translate():
    """
    传入pdf,输出html（未翻译的）
    """
    if request.method == 'POST':
        f = request.files['file']
        save_p = os.path.join(os.getcwd(), "media", "input", secure_filename(f.filename))
        if os.path.basename(save_p) == "":
            """检测有无上传文件"""
            return jsonify({
                "status": 1,
                "msg": "没传文件"
            })
        else:
            f.save(save_p)
            headPath.path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/input")))
            recover_structure_English()
            result_file_path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)

    else:
        return jsonify({
            "status": 0,
            "msg": "没接收到post请求"
        })


@app.route('/pdf2html_translated', methods=['GET', 'POST'])
def pdf2html_translated():
    """
    传入pdf,输出html（翻译的,并还原好）
    """
    if request.method == 'POST':
        f = request.files['file']
        save_p = os.path.join(os.getcwd(), "media", "input", secure_filename(f.filename))
        if os.path.basename(save_p) == "":
            """检测有无上传文件"""
            return jsonify({
                "status": 1,
                "msg": "没传文件"
            })
        else:
            f.save(save_p)
            headPath.path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/input")))
            recover_structure_Chinese()
            result_file_path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)
    else:
        return jsonify({
            "status": 0,
            "msg": "没接收到post请求"
        })


@app.route('/pdf_paragraph_to_txt', methods=['GET', 'POST'])
def pdf_paragraph_to_txt():
    """
    流程:读取文件->处理文件->处理完成后保存txt->发送文件地址
    :return:
    """
    if request.method == 'POST':
        f = request.files['file']
        save_p = os.path.join(os.getcwd(), "media", "input", secure_filename(f.filename))
        if os.path.basename(save_p) == "":
            """检测有无上传文件"""
            return jsonify({
                "status": 1,
                "msg": "没传文件"
            })
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
            headPath.path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/input")))

            write_paragraph_into_txt()
            result_file_path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)

    else:
        return jsonify({
            "status": 0,
            "msg": "没接收到post请求"
        })


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
        save_p = os.path.join(os.getcwd(), "media", "input", secure_filename(f.filename))
        if os.path.basename(save_p) == "":
            """检测有无上传文件"""
            return jsonify({
                "status": 1,
                "msg": "没传文件"
            })
        else:
            f.save(save_p)
            headPath.path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/input")))
            translate0()
            result_file_path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)

    else:
        return jsonify({
            "status": 0,
            "msg": "没接收到post请求"
        })


@app.route('/pdf2md', methods=['GET', 'POST'])
def pdf2md():
    """
    传入pdf,输出markdown
    """
    from generate_markdown import pdf_to_markdown

    if request.method == 'POST':
        f = request.files['file']
        save_p = os.path.join(os.getcwd(), "media", "input", secure_filename(f.filename))
        if os.path.basename(save_p) == "":
            """检测有无上传文件"""
            return jsonify({
                "status": 1,
                "msg": "没传文件"
            })
        else:
            f.save(save_p)
            headPath.path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/input")))
            save_1 = os.path.join(os.getcwd(), "media", "output", "output.md")

            pdf_to_markdown(headPath.path, save_1)

            result_file_path = os.path.join(os.getcwd(), get_latest_file(os.path.join("media/output")))
            return send_file(result_file_path, as_attachment=True)

    else:
        return jsonify({
            "status": 0,
            "msg": "没接收到post请求"
        })


def get_latest_file(path):
    """
    获取指定目录中最新的文件
    :param path: 目录路径
    :return: 最新文件的路径
    """
    # 获取目录中所有文件的列表
    files = [os.path.join(path, f) for f in os.listdir(path) if
             os.path.isfile(os.path.join(path, f))]
    # 按修改时间排序
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    # 返回最新的文件
    return files[0] if files else None


###########################################################################################
# ================================================================================================================
if __name__ == '__main__':
    # translate_function("/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/Introduction.pdf", {"file_id": 0},
    #                    "Introduction.pdf")
    app.run(debug=False, host="0.0.0.0", port=5008)
# https://www.daehee.com/werkzeug-console-pin-exploit/
