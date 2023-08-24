FROM python:3.8.7
# 将宿主机上的/home/project目录挂载到容器中的/home目录下
#VOLUME ["/home/zlk/zlk_project/pdf_translate_tool/pdf2md/code:/home"]

# 设置镜像源为阿里云
RUN echo "deb https://mirrors.aliyun.com/debian/ buster main" > /etc/apt/sources.list \
    && echo "deb https://mirrors.aliyun.com/debian/ buster-updates main" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.aliyun.com/debian-security/ buster/updates main" >> /etc/apt/sources.list

# 设置工作目录
WORKDIR /home/interface
COPY . .
# 暴露容器内的端口5008
EXPOSE 5008

# 安装vim
RUN apt-get update && \
    apt-get install -y python-opencv

# 安装requirements.txt中指定的依赖包
RUN pip install --no-cache-dir -r requirement_modify.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python","InterFace.py"]
