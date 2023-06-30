import head
import fitz
import os
def get_paper_path(path=r"./media"):
    """
    功能：
        获取指定目录下paper地址
    参数：
        path:paper父目录
    返回值：
        参数paper绝对路径list
    """
    path_resolution = []
    for i in os.listdir(path):
        path_resolution.append(os.path.join(os.getcwd(),"media",i))
    return path_resolution
# print(get_paper_path())