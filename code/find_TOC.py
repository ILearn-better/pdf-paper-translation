import head
import fitz
from collections import Counter
from find_main_text import find_main_text_font_size,statistics_of_font_size
from tools_function import get_one_page_span
"""
问题:会找image span作为正文span
"""
#########################################################
#判断span size是否大于正文
#判断该span size出现次数是否>=2
#拿到筛选后的span
def find_fontsize_bigger_than_main_fontsize(path):
#没什么用与find_font_size_number_more_than_twice重复了
    """
    功能:拿到目标span,即满足如下条件的span:
        所有 font size > 正文的 font size
    参数:
        path
    返回值:
        返回比正文font size大的font
    思路1：
        先拿到全文span list，再在全文span list中去筛选
    思路2：
        在遍历全文span时进行筛选，保存符合条件的
    """
    doc = fitz.open(path)
    main_text_font_size = find_main_text_font_size()
    all_page_statisfy_text=[]#相当于是用位置反映页数
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")  # 获取文本信息字典
        per_page_main_text =[]
        for block in text_dict["blocks"]:  # 遍历每个文本块
            if block["type"] == 0:  # 如果是文字类型
                for line in block["lines"]:  # 遍历每一行
                    for span in line["spans"]:  # 遍历每个span
                        if span["size"] > main_text_font_size:
                            per_page_main_text.append(span)

        all_page_statisfy_text.append(per_page_main_text)
    return all_page_statisfy_text
def Choose_TOC_span(path):
    """
    功能:
        统计font size出现次数>=2的span 以及 font size > 正文font size的span
    思路:
        先获得全文span的font size再用Counter统计
    参数:
        main_text_font_size：正文font size
        path：路径
    返回值:
        返回值1：font size出现次数>2且font size比正文font size大的span
        返回值2：全部font的front size
    """
    main_text_font_size =find_main_text_font_size(path)
    doc = fitz.open(path)

    record_everypage_spanlist = []
    record_amount = []
    for i in range(doc.page_count):
        span_ = get_one_page_span(doc[i],i)#拿文本span
        per_page_spansize = [j["size"] for j in span_]#展开每页文本span
        record_amount = record_amount+per_page_spansize#合并每页文本span
        record_everypage_spanlist = record_everypage_spanlist+list(span_)
    print("全文span总量:",len(record_everypage_spanlist))
    print("全文span:",record_everypage_spanlist)
    print("全文font size:",record_amount)

    order_list = sorted(dict(Counter(record_amount)).items(),key=lambda x:x[0],reverse=1)#会失去原本的顺序性
#     print(order_list)
    #通过条件筛选出合适的font size
    new_order_list=[]#存满足条件的font size
    for i,j in dict(order_list).items():#i是font size，j是font size出现次数
        if i>main_text_font_size and j>=2:
            new_order_list.append(i)

    #利用筛选出的font size 再筛选出span
    span_ouput = []
    for i in range(len(record_everypage_spanlist)):
        if record_everypage_spanlist[i]["size"] in new_order_list:
            span_ouput.append(record_everypage_spanlist[i])
    return span_ouput,new_order_list
#########################################################
#再次筛选条件,目的是筛掉多余span(例如图像span)
#流程:去span size list中的重复元素得到new_span_list
#再通过new_span_list[start_from_first_biggest_number[lst]:]得到完整的目录font size
#通过判断span font size是否在目录font size中，从而得到对应span
def start_from_first_biggest_number(lst):
    """
    功能:
        选择一个list中的最大值，返回对应索引
    参数:
        自带顺序的lst
    返回值:
        一个整数，表示lst中最大值的索引，如果lst为空或有多个最大值，返回-1
    """
    max_index = lst.index(max(lst))
    return max_index
def filter_TOC_span(processed_list):
    """
    功能:对去重且最大值截取后的font size list进行筛选，
    参数：new_list:对去重后的list
    返回值:
        True or False
        是否为目录font size
    """
    if len(processed_list) <3 or processed_list==[]:
        return False
    else:
        return True
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

# font_size_dict,record_most_account= Choose_TOC_span(head.path)
# print(font_size_dict)
# print(record_most_account)

# R_list = recovery_order_via_dict(font_size_dict,record_most_account)
# #去重判断是否满足树结构
# new_list = []
# for eleme in R_list:
#     if eleme not in new_list:
#         new_list.append(eleme)
# print(new_list)#去重后的list，每个元素可以视为表示一行
#
# doc = fitz.open(head.path)
# if doc.get_toc() != []:
#     print(doc.get_toc())
# else:
#     """
#
#     """