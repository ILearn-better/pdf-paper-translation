import head
import fitz
from collections import Counter
from find_main_text import find_main_text_font_size,statistics_of_font_size
def find_font_size_number_more_than_twice(path,main_text_font_size):
    """
    功能:统计font size出现次数>2的span
    思路:先获得全文span的font size再用Counter统计
    参数:
    返回值:
    """
    doc = fitz.open(path)
    record_most_account = []
    for i in range(doc.page_count):
        font_size,_,_ = statistics_of_font_size(doc[i])
        record_most_account = record_most_account+list(font_size)
    print("全文span总量:",len(record_most_account))
    order_list = sorted(dict(Counter(record_most_account)).items(),key=lambda x:x[0],reverse=1)
#     print(order_list)
    new_order_list=[]
    for i,j in dict(order_list).items():
        if i>main_text_font_size and j>=2:
            new_order_list.append((i,j))
    return dict(new_order_list),record_most_account
def start_from_first_biggest_number(lst):
    """
    功能:
        选择一个list中的最大值，返回对应索引
    参数:
        自带顺序的lst
    返回值:
        一个整数，表示lst中最大值的索引，如果lst为空或有多个最大值，返回-1
    """
    # 如果lst为空，返回-1
    if not lst:
        return -1
    # 初始化最大值和索引为第一个元素和0
    max_val = lst[0]
    max_idx = 0
    # 初始化一个标志，表示是否有多个最大值
    multiple = False
    # 遍历lst中除了第一个元素之外的其他元素
    for i in range(1, len(lst)):
        # 获取当前元素的值
        val = lst[i]
        # 如果当前元素的值大于最大值，更新最大值和索引，并将标志设为False
        if val > max_val:
            max_val = val
            max_idx = i
            multiple = False
        # 如果当前元素的值等于最大值，将标志设为True，表示有多个最大值
        elif val == max_val:
            multiple = True
    # 如果有多个最大值，返回-1，否则返回最大值的索引
    if multiple:
        return -1
    else:
        return max_idx

def find_TOC(path):
    """
    功能:
        没有TOC情况下找目录
        1.所有 font size > 正文的 font size，并且出现次数 >= 2 的认为是目录(先统计目前哪些span的font size出现次数超过2次)
        2.按照 font size 从大到小排序，是否能形成一颗完备的树
    参数:

    返回值:

    """
    doc = fitz.open(path)
    main_text_font_size = find_main_text_font_size()
    all_page_main_text=[]
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")  # 获取文本信息字典
        per_page_main_text =[]
        for block in text_dict["blocks"]:  # 遍历每个文本块
            if block["type"] == 0:  # 如果是文字类型
                for line in block["lines"]:  # 遍历每一行
                    for span in line["spans"]:  # 遍历每个span
                        #                         print(span["size"])
                        if span["size"] > main_text_font_size:
                            per_page_main_text.append(span)

        all_page_main_text.append(per_page_main_text)
    return all_page_main_text
def recovery_order_via_dict(dict_1,font_size_list):
    """
    功能:通过字典做font size的list筛选，恢复全局顺序
    参数:字典和font size list
    返回值:
        顺序list
    """
    recovery_list = []
    for i in font_size_list:
        if i in dict_1.keys():
            recovery_list.append(i)
    return recovery_list

font_size_dict,record_most_account= find_font_size_number_more_than_twice(head.path,find_main_text_font_size(head.path))
print(font_size_dict)

R_list = recovery_order_via_dict(font_size_dict,record_most_account)
#去重判断是否满足树结构
new_list = []
for eleme in R_list:
    if eleme not in new_list:
        new_list.append(eleme)
new_list#去重后的list，每个元素可以视为表示一行


# if doc.get_toc() != []:
#     print(doc.get_toc())
# else:
