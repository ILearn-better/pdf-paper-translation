############################################################################################################
# import sys
# sys.path.append("../")
from flask import Flask, request, jsonify, send_file
import threading
from logger import logger
import requests
import os
import global_param
from print_function import print_and_logger
from urllib.parse import urlparse
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


# ================================================================================================================
# 2023.08.07
@app.route('/pdf_translate2pdf', methods=['POST'])
def pdf_translate2pdf():
    """
    获取上传文件的路径，并翻译
    :return:
    """
    if request.method == 'POST':
        if not request.is_json:
            return "Request must be in JSON format", 400

    data_dict = request.json
    print("当前过程:\"获取传输文件字典\",地址:{},打印用户文件传输字典:{}".format(__file__, data_dict))
    logger.info("当前过程:\"获取传输文件字典\",地址:{},打印字典打印用户文件传输字典:{}".format(__file__, data_dict))
    #############################################################
    # 检测接受参数是否存在
    content = request.json.get("fileName")
    file_id = request.json.get("FileId")
    file_path = request.json.get("filePath")
    userid = request.json.get("userId")
    source = request.json.get("source")

    if not file_id or not file_path or not content or not userid or not source:
        return jsonify({
            "status": 0,
            "message": "未接受到参数"
        })
    #############################################################
    # 创建用户文件夹->创建类别文件夹
    # user_folder_path = os.path.join("media", str(data_dict["userId"]))
    # htmlorpng_folder = os.path.join(user_folder_path, "HTMLorPNG_folder")
    # inputpdf_folder = os.path.join(user_folder_path, "inputPDF_folder")
    # outputpdf_folder = os.path.join(user_folder_path, "outputPDF_folder")
    # if os.path.exists(os.path.join("media", str(data_dict["userId"]))):
    #     user_folder_path = os.path.join("media", str(data_dict["userId"]))
    #     print("地址:{},用户文件夹路径:{},{}".format(__file__, user_folder_path, "该用户静态文件夹已经存在"))
    # else:
    #     for i in [user_folder_path,htmlorpng_folder, inputpdf_folder, outputpdf_folder]:
    #         os.mkdir(i)
    #         print("地址:{},用户文件夹路径:{},{}".format(__file__, i, "该文件夹已新建成功！"))
    #############################################################
    # 创建类别文件夹->各类别下创建用户文件夹
    htmlorpng_folder = os.path.join("media", "HTMLorPNG_folder")
    inputpdf_folder = os.path.join("media", "inputPDF_folder")
    outputpdf_folder = os.path.join("media", "outputPDF_folder")


    for i in [htmlorpng_folder, inputpdf_folder, outputpdf_folder]:
        if os.path.exists(i):
            print("当前过程:\"生成中间文件夹\",地址:{},message:{}".format(__file__, i + "存在"))
            logger.info("当前过程:\"生成中间文件传入\",地址:{},message:{}".format(__file__, i + "存在"))
        else:
            os.mkdir(i)
            print("当前过程:\"生成中间文件夹\",地址:{},message:{}".format(__file__, i + "文件夹已创建成功"))
            logger.info("当前过程:\"生成中间文件夹\",地址:{},message:{}".format(__file__, i + "存在"))

    userfolder_n = source+"_"+str(data_dict["userId"])
    user_inputpdf_folder = os.path.join(inputpdf_folder, userfolder_n)
    user_htmlorpng_folder = os.path.join(htmlorpng_folder, userfolder_n)
    user_outputpdf_folder = os.path.join(outputpdf_folder, userfolder_n)

    for j in [user_inputpdf_folder, user_htmlorpng_folder, user_outputpdf_folder]:
        if os.path.exists(j):
            print("当前过程:\"生成用户文件夹\",地址:{},message:{}".format(__file__, j + "存在"))
            logger.info("当前过程:\"生成用户文件夹\",地址:{},message:{}".format(__file__, j + "存在"))

        else:
            os.mkdir(j)
            print("当前过程:\"生成用户文件夹\",地址:{},message:{}".format(__file__, j + "文件夹已创建成功"))
            logger.info("当前过程:\"生成用户文件夹\",地址:{},message:{}".format(__file__, j + "文件夹已创建成功"))

    #############################################################
    user_folder_path_dict = {
        "userhtmlorpng": user_htmlorpng_folder,
        "userinputpdf": user_inputpdf_folder,
        "useroutput": user_outputpdf_folder
    }
    #############################################################

    # pdf_save_path = download_pdf_file(data_dict, inputpdf_folder)#通过0 1 调整本地还是服务器
    pdf_save_path = download_pdf_file(data_dict, inputpdf_folder)  # 通过0 1 调整本地还是服务器
    print("当前过程:\"生成用户文件夹\",地址{},获取的上传文件保存路径:{}".format(__file__, pdf_save_path))
    logger.info("当前过程:\"生成用户文件夹\",地址{},获取的上传文件保存路径:{}".format(__file__, pdf_save_path))
    threading.Thread(target=translate_function, args=(pdf_save_path, data_dict, user_folder_path_dict)).start()
    return jsonify({
        "status": 1,
        "message": "success"
    })


#  当作视图函数测试
# @app.route('/pdf_translate2pdf', methods=['POST'])
def translate_function(pdf_save_path, data_dict, user_folder_path_dict):
    """
    提供翻译功能
    :return:
    """
    if os.path.isfile(pdf_save_path):
        print("路径{}下文件存在。".format(pdf_save_path))
    else:
        print("目标路径下没有文件")
        logger.info("目标路径下没有文件")
        return "目标路径下没有文件"
        # 检测有无文件，没有则返回无，有则向下执行
    try:
        from one_page_experience import main
        print_and_logger("开始文件处理", __file__, "")
        output_pdf_path = main(pdf_save_path, data_dict, user_folder_path_dict)
        print(__file__, "翻译完成，conbined_pdf.pdf文件已经生成！！！！！！")
        logger.info("地址:{},翻译完成，conbined_pdf.pdf文件已经生成！！！！！！".format(__file__))
        status = 1
    except Exception as e:
        output_pdf_path = ""
        status = 2
        print("发生异常", str(e))
    #########################################################
    fileId = data_dict["FileId"]
    HOST = global_param.BIZ_HOST
    url = HOST + "/pdftrans/callback"

    SERVER_HOST = global_param.SERVERS_HOST
    # filename = os.path.basename(output_pdf_path)
    json_data = {
        "id": fileId,
        "fileUrl": os.path.join(SERVER_HOST, output_pdf_path),  # 要改改
        "status": status,
        "source":data_dict["source"]
    }

    response = requests.post(url, data=json_data)
    if response.status_code == 200:
        logger.info("地址:{},成功响应：{}".format(__file__, response.json()))
        print(__file__, response.json())
    else:
        logger.info("地址:{},响应失败：{}".format(__file__, response, response.url))
        print(__file__, "回调响应：响应失败！", response)
    return response
    #########################################################


@app.route('/media/<filefolder>/<id>/<filename>')
def local_filedownload(filefolder, id, filename):
    """
    下载文件
    :return:文件流
    """
    media_dir = os.path.join(os.getcwd(), "media")
    full_path = os.path.join(media_dir, filefolder, id, filename)
    if not os.path.exists(full_path):
        return "File not Found", 404
    return send_file(full_path, as_attachment=True)

def is_absolute(url):
    return bool(urlparse(url).netloc)
def download_pdf_file(data_dict, inputpdf_folder):
    """Download PDF from given URL to local directory.
    :param data_dict: 接收字典
    :param inputpdf_folder：文件接收后的保存路径
    :param urlorpath:bool 0 or 1 控制带入本地文件路径（test）还是服务器文件下载路径（部署），默认是响应下载
    :return: True if PDF file was successfully downloaded, otherwise False.
    """
    if is_absolute(data_dict["filePath"]):
        url = data_dict["filePath"]
        # Request URL and get response object
        response = requests.get(url, stream=True)
        print(__file__, "文件下载地址请求已接收")
        logger.info('地址:{},请求状态:{}'.format(__file__, response))

        # isolate PDF filename from URL
        pdf_file_name = os.path.basename(url)
        assert pdf_file_name, "没拿到路径"
        if response.status_code == 200:
            # Save in current working directory
            userfolder_forinput = os.path.join(inputpdf_folder, str(data_dict["userId"]))
            if os.path.exists(userfolder_forinput):
                print("地址:{},message:{}".format(__file__, userfolder_forinput + "已存在"))
                logger.info('文件路径:{},文件写入路径：{},message:{}'.format(__file__, userfolder_forinput, "已存在"))
            else:
                os.mkdir(userfolder_forinput)
                print("地址:{},message:{}".format(__file__, userfolder_forinput + "已创建"))
                logger.info('文件路径:{},文件写入路径：{},message:{}'.format(__file__, userfolder_forinput, "已创建"))

            filepath = os.path.join(userfolder_forinput, pdf_file_name)
            logger.info('地址:{},文件写入路径：{}'.format(__file__, filepath))
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(response.content)
                print(f'{pdf_file_name} was successfully saved!')
            return filepath
        else:
            print(f'Uh oh! Could not download {pdf_file_name},')
            print(f'HTTP response status code: {response.status_code}')
            return None
    if os.path.isabs(data_dict["filePath"]):
        local_file_path = data_dict["filePath"]
        print("地址:{},message:{}".format(__file__, "目前处在本地调试模式"))
        logger.info("地址:{},message:{}".format(__file__, "目前处在本地调试模式"))
        return local_file_path
    else:
        print("地址:{},message:{}".format(__file__, "请输入绝对路径或者相对路径"))
        logger.info("地址:{},message:{}".format(__file__, "请输入绝对路径或者相对路径"))



if __name__ == '__main__':
    # translate_function("/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/Introduction.pdf", {"file_id": 0},
    #                    "Introduction.pdf")
    app.run(debug=False, host="0.0.0.0", port=5008)
# https://www.daehee.com/werkzeug-console-pin-exploit/
