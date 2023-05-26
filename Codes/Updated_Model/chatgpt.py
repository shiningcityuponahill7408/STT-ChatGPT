import openai
openai.api_key = "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"

class ChatGPT_part():
  def __init__(self, transcript):
    self.transcript = transcript
  
  def ChatGPT(self):
    model = "gpt-3.5-turbo"

    # 메시지 설정하기
    messages = [
            {'role' : 'system', 'content':'전체적인 대화의 맥락을 바탕으로 대화의 문제를 찾아주는 역할입니다.'},
            {'role' : 'system', 'content':'찾은 문제에 대한 이유를 바탕으로 이를 교정해줍니다. 이때 가장 우선시 되는 것은 갈등의 해결입니다.'},
            {'role' : 'system', 'content':'문맥상 어색한 부분이나, 세대별로 다른 이해를 발생할 수 있는 언어에 대한 내용을 찾아 교정합니다.'},
            {'role' : 'system', 'content':'교정의 이유는 대화 전체에서 맥락을 파악해 문제가 되는 이유로 상세히 나타냅니다.'},
            {'role' : 'system', 'content':'교정된 문장은 구어체 형식으로 대화에 맥락에 맞게 교정합니다.'},
            {'role' : 'system', 'content':'반드시 다음 내용만 출력해야 한다. 반드시 하나의 배열로 출력하고 각 원소는 파이썬 배열 형태로 [문장 순서, 이유, 교정된 문장]이다'},
            {"role": "user", "content": '대화내용\n '+ self.transcript}
    ]
    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    print("----")
    print(answer)
    print("----")

    return answer