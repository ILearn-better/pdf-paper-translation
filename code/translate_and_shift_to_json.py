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
def translate_and_shift_to_json():
    """

    :return:
    """

    import head as h
    import json
    with open(h.Json_save_path, 'r') as f:
        data = json.load(f)
    print(data.keys())
    # print(data["main_text"]["paragraph_block"])
    save_path ="translate_markdown"
    with open(save_path+".txt",'w',encoding="utf-8") as file:
        paragraph_block = data["main_text"]["paragraph_block"]

        translate_paragraph = []
        for block in paragraph_block:
            for line in block["lines"]:
                for span in line["spans"]:
                    print(span.keys())
                    if span["text"]=="":
                        print("没内容")
                    else:
                        file.write(span["text"])
            if span["text"][-1]==".":#可以加正则表达式
                translate_paragraph =translate_paragraph+"."
                file.write("\n"*10)
            else:
                translate_paragraph =translate_paragraph+span["text"]
                continue

        """
        translate_paragraph中存的时每一段，之后要对这些段落进行翻译。
        ！在此之前要检测一下段落准不准
        """
    return translate_paragraph
translate_and_shift_to_json()