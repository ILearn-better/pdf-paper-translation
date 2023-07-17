import requests
import json
def interface_to_dict(content:str)->dict:
    url = 'http://192.168.1.199:5000/api/v1/qamessages'

    param_dict ={"question_content": content,
                 "conversation_guid": "0",
                 "robots": [{"robot_id": 0, "llm_provider": "ChatGLM", "llm_model": "chatGLM-6B"}],
                 "user_uid": 1,
                 "prompt": "翻译",
                 "vector_ids": [""],
                 "load_lib": False,
                 "load_type": 1,
                 "history": {"his_len": 5, "question_list": [], "anwser_list": {}},
                 "options": {"chunk_size": 300, "embedding_model": "text2vec-large-chinese", "temperature": "0.1"}
                 }
    headers = {"Content-Type":"application/json"}

    pp= json.dumps(param_dict)
    response = requests.post(url, data=pp,headers=headers)

    if response.status_code == 200:
        # print(response.json())
        print('File uploaded successfully')
        return response.json()
    else:
        print('File upload failed')
        return False
if __name__=="__main__":
    text = "It is becoming increasingly clear that misinformation is taking its toll on public opinion on climate and sustainability issues as well."
    dd = interface_to_dict(text)
    print(dd["data"]["answers"][0]["answer_content"])
