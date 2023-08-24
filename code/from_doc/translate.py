import requests
import json
import math
from .interface.global_param import AI_HOST


def interface_to_dict(content: str) -> dict:
    url = 'http://{}:5000/api/v1/translate'.format(AI_HOST)
    # url="http: // sam.insigma.chat: 8198 / conversation?id = 2"
    param_dict = {"question_content": content}
    # ,
    # "conversation_guid": "0",
    # "robots": [{"robot_id": 0, "llm_provider": "ChatGLM", "llm_model": "chatGLM-6B"}],
    # "user_uid": 1,
    # "prompt": "翻译",
    # "vector_ids": [""],
    # "load_lib": False,
    # "load_type": 1,
    # "history": {"his_len": 5, "question_list": [], "anwser_list": {}},
    # "options": {"chunk_size": 300, "embedding_model": "text2vec-large-chinese", "temperature": "0.1"}
    # }
    headers = {"Content-Type": "application/json"}

    pp = json.dumps(param_dict)
    try:
        response = requests.post(url, data=pp, headers=headers)
    except:
        print(__file__,"GML接口翻译未响应")
    if response.status_code == 200:
        # print(response.json())
        print('File uploaded successfully')
        return response.json()
    else:
        print('File upload failed')
        return False


def translate():
    """
    思路:获取段落结构，结构->翻译->重组
    功能:
        获取段落结构，翻译文本
    参数:
        paragraphs：段落文本数据结构
    返回值:
        返回同结构翻译文本
    """
    import head
    from translate_and_shift_to_json import translate_and_shift_to_json3
    # 检测是否接口有打开
    if interface_to_dict(" ") == False: return False

    text_block = translate_and_shift_to_json3()
    # print(text_block)
    text_block_Ch = []
    for tuple_dict in text_block:
        if len(tuple_dict) > 1:
            # print(len(tuple_dict))
            tx1 = ""
            str_account = []  # 英文字符长度
            for block in tuple_dict:
                txt_str = head.get_block_text(block)
                tx1 = tx1 + txt_str

                str_account.append(len(txt_str))
            # tx1_Ch = interface_to_dict(tx1)["data"]["answers"][0]["answer_content"]
            tx1_Ch = interface_to_dict(tx1)["data"]

            # 字符串分割-按字数占比
            para = ()
            s = sum(str_account)
            start_0 = math.ceil(str_account[0] / s)
            for i in range(len(tuple_dict)):
                if i == 0:
                    new_block = {"bbox": tuple_dict[0]["bbox"],
                                 "type": "text",
                                 "page": tuple_dict[0]["page"],
                                 "text": tx1_Ch[:start_0]}
                    para = para + (new_block,)
                    start = 0
                else:
                    start = start + math.ceil(str_account[i - 1] / s)
                    end = start + math.ceil(str_account[i] / s)  # 可能会有一些溢出问题
                    new_block = {"bbox": tuple_dict[0]["bbox"],
                                 "type": "text",
                                 "page": tuple_dict[0]["page"],
                                 "text": tx1_Ch[start:end]}

                    para = para + (new_block,)

            text_block_Ch.append(para)
        if len(tuple_dict) == 1:
            tx2 = head.get_block_text(tuple_dict[0])
            # print(""*10+"tx2:",tx2)
            # tx2_Ch = interface_to_dict(tx2)["data"]["answers"][0]["answer_content"]
            tx2_Ch = interface_to_dict(tx2)["data"]
            """
            检测是否含'抱歉，您提供的信息有些简短。请您提供更多的详细信息，以便我为您撰写更具吸引力的文案。'，若含有则不翻译。
            涉及"抱歉","提供更多信息","提供更多详细信息"等词汇的话不翻译。
            """
            pattern = r'^(?=.*抱歉)(?=.*提供更多信息)(?=.*提供更多详细信息)'
            if head.re.search(pattern, tx2_Ch):
                new_block = {"bbox": tuple_dict[0]["bbox"],
                             "type": "text",
                             "page": tuple_dict[0]["page"],
                             "text": tx2}
                # print(new_block)
                text_block_Ch.append((new_block,))
            else:
                new_block = {"bbox": tuple_dict[0]["bbox"],
                             "type": "text",
                             "page": tuple_dict[0]["page"],
                             "text": tx2_Ch}
                # print(new_block)
                text_block_Ch.append((new_block,))
        else:
            continue
    return text_block_Ch


def translate0():
    """
    基础翻译能力：不具备格式复原能力
    思路：对于每一个段落，先带入API->翻译->写入文档
    :return:
    """
    import head
    from translate_and_shift_to_json import translate_and_shift_to_json3
    # 检测是否接口有打开
    # if interface_to_dict(" ")==False:return False
    #

    text_block = translate_and_shift_to_json3()
    # print(text_block)
    save_p = head.os.path.join(head.os.getcwd(), "media", "output", "translation.txt")
    print(save_p)
    with open(save_p, "w", encoding="utf-8") as file:
        text_block_Ch = []
        for tuple_dict in text_block:
            if len(tuple_dict) > 1:
                # print(len(tuple_dict))
                tx1 = ""
                str_account = []  # 英文字符长度
                for block in tuple_dict:
                    txt_str = head.get_block_text(block)
                    tx1 = tx1 + txt_str

                    str_account.append(len(txt_str))
                # tx1_Ch = interface_to_dict(tx1)["data"]["answers"][0]["answer_content"]
                tx1_Ch = interface_to_dict(tx1)["data"]

                file.write(tx1_Ch + "\n")

                text_block_Ch.append(tx1_Ch)
            if len(tuple_dict) == 1:
                tx2 = head.get_block_text(tuple_dict[0])
                # print(""*10+"tx2:",tx2)
                # tx2_Ch = interface_to_dict(tx2)["data"]["answers"][0]["answer_content"]
                tx2_Ch = interface_to_dict(tx2)["data"]
                """
                检测是否含'抱歉，您提供的信息有些简短。请您提供更多的详细信息，以便我为您撰写更具吸引力的文案。'，若含有则不翻译。
                涉及"抱歉","提供更多信息","提供更多详细信息"等词汇的话不翻译。
                """
                pattern = r'^(?=.*抱歉)(?=.*提供更多信息)(?=.*提供更多详细信息)'
                if head.re.search(pattern, tx2_Ch):

                    file.write(tx2)

                    text_block_Ch.append((tx2,))

                else:

                    file.write(tx2_Ch)

                    text_block_Ch.append((tx2_Ch,))

                file.write("\n")
            else:
                continue

    return text_block_Ch


if __name__ == "__main__":
    #####################################################
    #翻译测试
    text = "It is becoming increasingly clear that misinformation is taking its toll on public opinion on climate and sustainability issues as well."
    # text="Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation . Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures. Recurrent models typically factor computation along the symbol positions of the input and output sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden states ht, as a function of the previous hidden state ht−1 and the input for positiont. This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples. Recent work has achieved significant improvements in computational efficiency through factorization tricks and conditional computation, while also improving model performance in case of the latter. The fundamental constraint of sequential computation, however, remains. Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences. In all but a few cases, however, such attention mechanisms are used in conjunction with a recurrent network. In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs."
    dd = interface_to_dict(text)
    print(dd)
    # pass
    # print(dd["data"]["answers"][0]["answer_content"])
    #####################################################
    import time
    # start = time.time()
    # end =time.time()
    # text_block_Ch = translate0()
    # print(end-start)
    # print(text_block_Ch)
