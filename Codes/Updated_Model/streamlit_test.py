import streamlit as st
import time

# set the layout wide
st.set_page_config(layout = "wide")

# visual components
st.title("Hi! We recommend a better conversation for you!")

# get an audio file; wav and mp3 are allowed to be uploaded
audiofile = st.file_uploader("Upload an audio file! You can upload .wav", type = ["wav"] )

# or get a YouTube link
url = st.text_input("Or copy and paste a YouTube link!")

def CombineText(texts):
    resultText = []
    tempText = ""

    speakerNumber = texts[0][0]
    startTime = time.strftime("%M:%S", time.gmtime(0))

    index = 0

    for i, text in enumerate(texts):
        if(text[0] == speakerNumber):
            tempText += text[1] + "\n"

        else:
            resultText.append([index, speakerNumber, startTime, tempText])

            index += 1
            startTime = time.strftime("%M:%S", time.gmtime(text[2]))
            tempText = text[1] + "\n"
            speakerNumber = text[0]

    return resultText

def makeOriginalText(texts):

    result = ""

    for index, speakerNumber, startTime, text in texts:
        st.write(f"**{speaker_img[speakerNumber]}Speaker {speakerNumber}** (*{startTime}*)")
        st.write(text)
        st.write("")

    return result

def makeGPTText(texts):

    result = ""

    for index, speakerNumber, startTime, text in texts:
        result += f"[Speaker {speakerNumber}]\n"
        result += text
        result += "\n"
        
    return result

text = [[1, ' 평소에 눈도 안 맞춰지지 않냐?', 0.0], [1, ' 뭔 일이야?', 2.32], [0, ' 당신 헤어스타일 바꿨나?', 3.62], [1, ' 웬일이래?', 6.0200000000000005], [1, ' 옛날에 내가 머리를 빡빡 밀어도 못 알아보던 사람이?', 7.62], [0, ' 무슨 말을 그렇게 극단적으로 해?', 10.88], [0, ' 내가 아무리 무신경에도 그렇지, 당신이 머리를 빡빡 밀었는데', 12.58], [0, ' 그것도 못 알아봤을까 봐.', 16.06], [1, ' 말이 그렇다는 거야, 말이.', 17.56], 
        [1, ' 아무튼 사랑스럽지만 알아버려서 고맙네요.', 19.66], [0, ' 당신 피부과 시술도 받았어?', 24.0], [0, ' 요새 운동도 하고 외모에 신경 많이 쓰네.', 26.0], [1, ' 나 피부는 원래 좋았거든.', 30.0], [0, ' 와 오늘 왜 이렇게 예뻐요?', 34.0], [0, ' 얼굴 너무 좋아 보이시는데?', 35.9], [0, ' 서인호는 그냥 최생이 가지라고 줘버려요.', 38.1], [0, ' 줘버려요.', 40.4], [1, ' 조금만 더 있다가요.', 41.4], [1, ' 둘이 섹시한 건 너무너무 웃기잖아요.', 42.9]]

speaker_img = ["🔴","🔵","🟡","🟢","🟣"]

result = CombineText(text)
gptText = makeGPTText(result)
print(gptText)

with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("음성 기록")
        makeOriginalText(result)

    with col2:
        st.header("Here is a better conversation you may try!")
        st.text("bbb")


