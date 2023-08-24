"""
核心:找不是正文，不是目录，不是图片

坐标是唯一的

思路1：
    找所有字体小于正文的span和目录，而且坐标不与图片坐标重合的span
思路2:
    找与正文，目录，图片的coordinate都不相同的span

"""
import head as headPath
def find_other_font():
    """
    功能:
        找与正文，目录，图片的coordinate都不相同的span
    参数:
    返回值:
        目标span的字典
    """
    from find_main_text import find_main_text,find_main_text_font_size
    from find_TOC import Choose_TOC_span
    from get_picture import extract_images_to_save_into_png
    from tools_function import get_all_page_span

    #拿正文coordinate文本
    main_text_span_list=find_main_text(headPath.path,find_main_text_font_size(headPath.path))
    main_text_span_coordinate_list =[j["bbox"] for i in main_text_span_list for j in i]
    # print(main_text_span_coordinate_list[0])

    #拿目录coordinate文本
    TOC_span_list,_=Choose_TOC_span(headPath.path)
    TOC_span_coordinate_list =[i["bbox"] for i in TOC_span_list]
    # print(TOC_span_coordinate_list)

    #拿图片coordinate
    pic_dict=extract_images_to_save_into_png(headPath.path,0)
    pic_dict_bbx_list = [i["coordinate"] for i in pic_dict]
    print(pic_dict_bbx_list)

    full_page_span=get_all_page_span(headPath.path)
    other_font = []
    for i in full_page_span:
        # print(i["bbox"])
        # print(i)
        if i["bbox"] in main_text_span_coordinate_list or i["bbox"] in TOC_span_coordinate_list or i["bbox"] in pic_dict_bbx_list:
            continue
        else:
            other_font.append(i)
    return other_font
# find_other_font()
if __name__ == "__main__":
    pass