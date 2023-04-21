import openai

openai.api_key = "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"

messages = []

content = '''
다음의 대화를 보고 1. 화자들이 어떤 관계인지 추측해보고 2. 화자들이 가지고 있는 갈등이 있는지 추측해봐
3. i-message 개념에 기반해서 개선된 대화로 바꿔줘
SPEAKER 1 :  그냥 여보가 말을 좀 가끔씩 아직은 노력 많이 하지만 거칠게 할 때가 있어서
SPEAKER 2 :  존댓말 쓰잖아요 그래서
SPEAKER 1 :  거칠게 존댓말 하잖아요
SPEAKER 2 :  아니
SPEAKER 2 :  음
SPEAKER 2 :  음
SPEAKER 2 :  왜
SPEAKER 1 :  뭐가 있어요?
SPEAKER 2 :  힘줄?
SPEAKER 1 :  힘줄인가?
SPEAKER 1 :  소의 힘줄이지 뭐 뼈가 있겠어요?
SPEAKER 2 :  뼈도 있지
SPEAKER 1 :  그 비아냥거리는 말투도 싫어요
SPEAKER 2 :  어떻게 살아요 내랑
'''

messages.append({"role": "user", "content": content})

completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = messages)

chat_response = completion.choices[0].message.content

#print(f"ChatGPT: {chat_response}")
print(chat_response[chat_response.index("3.") + 3: ])