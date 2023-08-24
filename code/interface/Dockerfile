FROM registry.in/python-cv:1.0


# 设置工作目录
WORKDIR /home/interface
COPY . .
# 暴露容器内的端口5008
EXPOSE 5008

# 安装vim
RUN apt-get install -y wkhtmltopdf

# 安装requirements.txt中指定的依赖包
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python","InterFace.py"]
