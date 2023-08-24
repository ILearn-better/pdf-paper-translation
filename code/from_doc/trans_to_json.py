"""
需要讨论
"""
class Json_output_struct():
    def __init__(self):
        self.json={
            "TOC": {},
            "main_text":
            {
                "main_text_span": {},
                "paragraph_block":{}
            },
            "other span":{},
            "picture":{}
        }
def trans_to_json():
    """
    将各部分span打包为字典存入json
    思路:
    获取目录span
    获取正文span 获取段落block
    获取其他span
    获取图片span
    :return:
    """
    import head
    import json
    TOC_span_list,_=head.Choose_TOC_span(head.path)
    #
    main_text_font_size = head.find_main_text_font_size(head.path)
    main_text_list =head.find_main_text(head.path,main_text_font_size)
    main_text_block=head.get_main_text_block()
    # other_font_list =head.find_other_font()#因为要做的是翻译,所以不需要
    # image_list = head.extract_images_to_save_into_png(head.path,0)#因为要做的是翻译,所以不需要
    Json_1 = Json_output_struct().json


    for key, value in Json_1.items():  # 遍历字典的键值对
        print(key, value)
    Json_1["TOC"] = TOC_span_list
    # Json_1["main_text"]["main_text_span"]  =main_text_list
    Json_1["main_text"]["paragraph_block"] =main_text_block
    # Json_1["other span"] =other_font_list
    # Json_1["picture"] = image_list
    print(Json_1)
    # 保存与写入
    file_name ="pdf_to_json"
    save_path = head.os.path.join(head.os.getcwd(),"output",file_name+".json")
    with open(save_path,"w",encoding="utf-8") as file:
        file.write(json.dumps(Json_1,ensure_ascii=False,indent=4))
# trans_to_json()
if __name__ == "__main__":
    pass