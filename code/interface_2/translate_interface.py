import openai
import os
import requests
import json
from global_param import AI_HOST
from logger import logger



# =====================================================================
# 调用ChatGPT并与模型交互
# message key说明：
# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Who won the world series in 2020?"},
#     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#     {"role": "user", "content": "Where was it played?"}
# ]
# =====================================================================
class GPT_API:
    # 在 https://platform.openai.com/ 上获取您的 API 密钥
    def __init__(self):
        os.environ["http_proxy"] = "http://127.0.0.1:7890"
        os.environ["https_proxy"] = "http://127.0.0.1:7890"

        openai.api_key = "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"
        # 将用户输入添加到对话历史
        prompt = "你是我的文章翻译助手，我将给你一段英文文本，请你帮我翻译为中文，要求尽可能精简和准确。" \
                 "如果只有一个单词就直接翻译该单词。" \
                 "输出不要加句号。" \
                 "请勿在翻译内容中加入自己的分析，如果不知道如何翻译，请回答\"不知道\""
        messages = [
            {"role": "system", "content": prompt},
            {"role": "assistant", "content": ''},
        ]
        self.use_api_history(prompt,messages)#有上下文功能

        # self.history_message = [{"role": "system", "content": prompt}, {"role": "assistant", "content": ''}]

    def use_api_without_history(self, user_input):
        """
        该类的外部调用函数，用于输出翻译结果
        :param user_input:要翻译的字符串文本
        :return:
        """
        print("text:{}".format(user_input))
        history = self.history_message
        history.append({"role": "system", "content": user_input})
        response = self.call_chatgpt_onece(history)
        print("translated:{}".format(response.choices[0].message.content.strip()))
        return response.choices[0].message.content.strip()

    # 调用 ChatGPT API 函数
    def use_api_history(self, user_input, message):
        history = 0
        while user_input not in ["退出", "quit", "exit"]:
            if history == 0:
                response = self.call_chatgpt_onece(message)
                print(response.choices[0].message.content.strip())
                message.extend([
                    {"role": "system", "content": user_input},
                    {"role": "assistant", "content": response.choices[0].message.content.strip()}
                ])
                # print(message)
                user_input = input("您好，请输入一个问题或指令：")
                history = history + 1
            else:
                message.append({"role": "system", "content": user_input})
                response = self.call_chatgpt_onece(message)
                print(response.choices[0].message.content.strip())
                message.append({"role": "assistant", "content": response.choices[0].message.content.strip()})
                user_input = input("您好，请输入一个问题或指令：")
                history = history + 1

        with open(os.path.join("media", "output", "save_conversation.txt"), "w", encoding="utf-8") as file:
            for i in message:
                file.write(i["role"] + ":" + i["content"])
                file.write("\n")
        return response.choices[0].message.content.strip()

    def call_chatgpt_onece(self, context):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或其他支持GPT-3.5的模型引擎
            messages=context,
            # max_tokens=150,  # 设置响应的最大长度
            temperature=0.2,  # 控制生成文本的创造性，值越大越随机，值越小越保守
            stop=None,  # 可以设置在何时停止生成文本
        )
        # return response.choices[0].message.content.strip()
        return response

def GPTinterface_to_dict(content: str) -> dict:
    url = "http://192.168.1.196:5000/api/v1/gpt_translate"
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
    print("pp:",pp)
    response = requests.post(url, data=pp, headers=headers)
    if response.status_code == 200:
        # print(response.json())
        print('File uploaded successfully')
        return response.json()
    else:
        print('GPT接口翻译未响应')
        return False

def interface_to_dict(content: str) -> dict:
    url = 'http://{}:5000/api/v1/translate'.format(AI_HOST)
    # url="http: // sam.insigma.chat: 8198 / conversation?id = 2"
    param_dict = {"question_content": content}
    headers = {"Content-Type": "application/json"}
    pp = json.dumps(param_dict)

    response = requests.post(url, data=pp, headers=headers)
    if response.status_code == 200:
        # print(response.json())
        print('GML翻译接口响应正常')
        print("GML翻译结果:",response.json())
        return response.json()
    else:
        print(__file__, "GML接口翻译未响应")
        logger.info(__file__+"  "+"GML接口翻译未响应")
        return False

#
if __name__ == "__main__":
    # tranlater = GPT_API()
    # str1 = "hello,my friend!You don't know how I love you."
    # resp = tranlater.use_api_without_history(str1)
    ########################################################
    str1 = "asdcasc asddwe2+sd()sd dssdcsac)"
    resp = GPTinterface_to_dict(str1)
    print(resp)

