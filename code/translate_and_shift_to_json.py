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

def get_block_text(block):
    """
    功能:
    带入正文block，返回内容文本
    :return:
    """
    p = ""
    for line in block["lines"]:
        for span in line["spans"]:
            p = p+span["text"]
    print(p)
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

            if block_num==0 and block_first_letter.isupper()==0:
                continue
            p = get_block_text(block)
            #判断首span text的首字母是否大写 and 前一个block的末尾是否为句号结尾（这种也可能不是一段）
            if block_first_letter.isupper()==True and previous_block_paragraph[-1]=="." :
                result.append(p)
            else:
                print(result)
                result[-1] +=" "+p

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
    return bool(head.re.search(r'[A-Z]', s))

def translate_and_shift_to_json2():
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
            block_first_letter = block["lines"][0]["spans"][0]["text"][:]
            if block_num==0 and block_first_letter.isupper()==0:
                continue
            p = get_block_text(block)
            #判断首span text的首字母是否大写 and 前一个block的末尾是否为句号结尾（这种也可能不是一段）
            if has_uppercase(block_first_letter) and previous_block_paragraph[-1]==".":
                result.append(p)
            else:
                print(result)
                result[-1] +=" "+p

    #去重重复字符串

    save_path ="translate_markdown"
    with open(save_path+".txt",'w',encoding="utf-8") as file:
        for i in range(len(result)):
            file.write("第{}段:\n".format(i))
            file.write(result[i])
            file.write("\n")
    return result
translate_and_shift_to_json2()