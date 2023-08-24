import os
#############################################################################
# 环境变量设置
import os

DEV_MODE = 'DEV'  # 开发环境
PRO_MODE = 'PRO'  # 正式环境



MODE = os.environ.get("MODE") or DEV_MODE

if MODE == PRO_MODE:
    SERVERS_HOST = 'http://pdf.insigma.chat:8198'
    BIZ_HOST = 'http://biz:8000'
    AI_HOST = "192.168.1.196"

else:
    SERVERS_HOST = 'http://192.168.1.124:5008'
    BIZ_HOST = 'http://192.168.1.56:8000'
    # BIZ_HOST = 'http://192.168.2.230:8000'
    AI_HOST = "192.168.1.196"

AI_HOST = os.environ.get('AI_HOST') or AI_HOST
BIZ_HOST = os.environ.get('BIZ_HOST') or BIZ_HOST
SERVERS_HOST = os.environ.get('SERVERS_HOST') or SERVERS_HOST
#############################################################################
pdf_path = "/home/zhoulikun/zhou_work/pdf2md/code/interface/media/input/Introduction.pdf"
PDF_PATH =""