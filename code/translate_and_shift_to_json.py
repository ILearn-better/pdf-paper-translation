"""
思路：
    用json提文本然后翻译
    >段落问题:
    block的最后一个句子是否是句号结尾，不是默认段落未结束（有些文章就是没句号的分开讨论）
        !不一定准确，因为论文结尾有时候有引用

    >思路：正文部分全部输出为一篇长文再输出
"""

"""
该文件未完成
"""
import head
def combine_strings(lst):
    result = []
    for i in range(len(lst)):
        if i == 0 and lst[i] == '小':
            continue
        if lst[i] == '大':
            result.append('大')
        else:
            result[-1] += '小'
    return result

# print(combine_strings(["大","小","小","小","小"]))
def get_block_span(block):
    """拿block中的所有span信息"""
    span_1=[]
    for line in block["lines"]:
        for span in line["spans"]:
            span_1.append(span)
    return span_1

def get_block_text(block):
    """
    功能:
    带入正文block，返回内容文本
    :return:
    """
    p = " "
    # print(block)
    for line in block["lines"]:
        for span in line["spans"]:
            p = p+span["text"]
            # p = p+span["text"]+"  "
        # p+="\n"
    return p


# import head
# data =head.get_main_text_block()
# paragraph_block =data
# block = paragraph_block[0]
# print(block)
# print(get_block_text(block))


def translate_and_shift_to_json():
    """
    :return:
    """
    import head as h
    import json
    # with open(h.Json_save_path, 'r') as f:
    #     data = json.load(f)
    import head

    data =head.get_main_text_block()
    paragraph_block =data
    result = [""]
    for block_num in range(len(paragraph_block)):
        """
        获取上一个block的所有文本，判断是否由句号结尾
        """
        previous_block_paragraph = get_block_text(paragraph_block[block_num-1])
        block=paragraph_block[block_num]
        if block["type"]==0:
            block_first_letter = block["lines"][0]["spans"][0]["text"][0]
            p = get_block_text(block)

            if block_num==0 and block_first_letter.isupper()==0:
                continue
            if block_num==0 and block_first_letter.isupper()==True:
                result[-1] += " " + p + " "
            #判断首span text的首字母是否大写 and 前一个block的末尾是否为句号结尾（这种也可能不是一段）
            #思考常见的段落结尾方式
            if block_first_letter.isupper()==True or previous_block_paragraph[-1]==" " :
            # if block_first_letter.isupper() == True or previous_block_paragraph[-1] == ".":
                result.append(p)
            else:
                result[-1] +=" "+p+" "

    #去重重复字符串

    save_path ="translate_markdown"
    with open(save_path+".txt",'w',encoding="utf-8") as file:
        for i in range(len(result)):
            file.write("第{}段:\n".format(i))
            file.write(result[i])
            file.write("\n")
    return result
# t = translate_and_shift_to_json()
# print(t)
def has_uppercase(s):
    return bool(head.re.search(r'^[A-Z]', s))

def re_judge(pattern,string_1):
    import re
    # print(re.compile(pattern))
    match = re.search(pattern, string_1)
    if match:
        # print('找到匹配项:', match.group())
        # print('匹配项的起始位置:', match.start())
        # print('匹配项的结束位置:', match.end())
        return True
    else:
        return False
def translate_and_shift_to_json2():
    """
    采用默认分段、判断合并的方法
    :return:
    """
    # with open(h.Json_save_path, 'r') as f:
    #     data = json.load(f)
    data =head.get_main_text_block()
    paragraph_block =data
    result = [""]
    for block_num in range(0,len(paragraph_block)):#一般第一页不是正文
        """
        获取上一个block的所有文本，判断是否由句号结尾
        """
        previous_block_paragraph = get_block_text(paragraph_block[block_num-1])
        block=paragraph_block[block_num]
        if block["type"]==0:
            block_first_letter = block["lines"][0]["spans"][0]["text"][:].rstrip()
            if block_num==0 and block_first_letter.isupper()==0:
                continue
            p = get_block_text(block)
            #判断首span text的首字母是否大写 and 前一个block的末尾是否为句号结尾（这种也可能不是一段）
            #换个思路：想想怎么才需要字符串合并
            rre = re_judge(r'[a-z]$',previous_block_paragraph.rstrip())#上个block文本是否小写结尾
            print(previous_block_paragraph)
            print("="*30)
            #如果上一段结尾为小写，本段开头为小写，则将上一段和本段合并
            """问题：1.有大写的人名跳出来影响分割；2.有其他span跳出来影响分割"""
            if has_uppercase(block_first_letter)==False or rre:#只要一方是小写就可合并
                # result.append(p)
                result[-1] +=" "+p
            else:
                # print(result)
                # result[-1] +=" "+p
                result.append(p)
    #去重重复字符串
    save_path ="translate_markdown"
    with open(save_path+".txt",'w',encoding="utf-8") as file:
        for i in range(len(result)):
            file.write("第{}段:\n".format(i))
            file.write(result[i])
            file.write("\n")
    return result
translate_and_shift_to_json2()



def translate_and_shift_to_json3():
    """
    打包段落的block信息
    :return:
    """
    # with open(h.Json_save_path, 'r') as f:
    #     data = json.load(f)
    data =head.get_main_text_block()
    paragraph_block =data
    result = [""]

    # text_block =[[]]
    text_block =[()]

    for block_num in range(0,len(paragraph_block)):#一般第一页不是正文
        """
        获取上一个block的所有文本，判断是否由句号结尾
        """
        # text_conbined_block_cell =[]

        previous_block_paragraph = get_block_text(paragraph_block[block_num-1])
        block=paragraph_block[block_num]
        if block["type"]==0:
            block_first_letter = block["lines"][0]["spans"][0]["text"][:].rstrip()
            if block_num==0 and block_first_letter.isupper()==0:
                continue
            p = get_block_text(block)
            #判断首span text的首字母是否大写 and 前一个block的末尾是否为句号结尾（这种也可能不是一段）
            #换个思路：想想怎么才需要字符串合并
            rre = re_judge(r'[a-z]$',previous_block_paragraph.rstrip())#上个block文本是否小写结尾
            #如果上一段结尾为小写，本段开头为小写，则将上一段和本段合并
            """问题：1.有大写的人名跳出来影响分割；2.有其他span跳出来影响分割"""
            if has_uppercase(block_first_letter)==False or rre:#只要一方是小写就可合并
                # result.append(p)
                result[-1] +=" "+p

                # text_conbined_block_cell = [result[-1],block]
                # text_block.append(text_conbined_block_cell)

                text_block[-1]+=(block,)
            else:
                # print(result)
                # result[-1] +=" "+p
                result.append(p)

                text_block.append((block,))

    return text_block
    #
    # #去重重复字符串
    # save_path ="translate_markdown"
    # with open(save_path+".txt",'w',encoding="utf-8") as file:
    #     for i in range(len(result)):
    #         file.write("第{}段:\n".format(i))
    #         file.write(result[i])
    #         file.write("\n")
    # return result
# with open("block_result.txt","w",encoding="utf-8") as file:
#     file.write(str(translate_and_shift_to_json3()))
    #文档内部有重复语句