import streamlit as st
#import get_speakers as gs
import transcribe as t
import chatgpt as gpt
import os
import yt_dlp
import json

# --------------------- Text Part -----------------------------------------------------------
speaker_img = ["🔴","🔵","🟡","🟢","🟣"]

def makeOriginalText(texts):
    result = ""

    for index, speakerNumber, startTime, text in texts:
        st.write(f"**{speaker_img[speakerNumber]}Speaker {speakerNumber}** (*{startTime}*)")
        st.write(text)

    return result

def makeGPTInputText(texts):
    result = ""

    for index, speakerNumber, startTime, text in texts:
        result += f"[Speaker {speakerNumber}]\n"
        result += text
        result += "\n"
        
    return result

def makeGPTOutputText(texts):
    text = '[' + texts + ']'
    result = eval(texts)

    if(len(result) == 1):
       return result[0]
    else:
       return result

def makeImproveText(texts):
       for text in texts:
        print(text)
        index = int(text[0])
        reason = text[1]
        change = ", ".join([str(x) for x in text[2:]])

        speakerNumber = result[index-1][1]
        startTime = result[index-1][2]

        st.write(f"**{speaker_img[speakerNumber]}Speaker {speakerNumber}** (*{startTime}*)")
        st.write(f"*:green[{reason}]*")
        st.write(":red[제안화법 => ]  " + change)

def makeAudio():
  audio_file = open('conversation.wav', 'rb')
  audio_bytes = audio_file.read()

  st.audio(audio_bytes, format='audio/ogg')




# ---------------------- Web Page -------------------------------------------------------------

# set the layout wide
st.set_page_config(layout = "wide")

# visual components
st.title("Hi! We recommend a better conversation for you!")

# get an audio file; wav and mp3 are allowed to be uploaded
audiofile = st.file_uploader("Upload an audio file! You can upload .wav", type = ["wav"] )

# or get a YouTube link
url = st.text_input("Or copy and paste a YouTube link!")

# when audio file is received
if audiofile is not None and len(url) == 0:

    # when an audio file is given, show the name of it
    st.write(f"we got \"{audiofile.name}\" file from you. Will be right back with a better conversation!")

    makeAudio()
    #num_speakers = gs.get_num_speakers(audiofile)

    T = t.Transcribe(audiofile,  True)
    result = T.diarization()

    G = gpt.ChatGPT_part(result)
    gpt = G.ChatGPT()
    gptInput = makeGPTInputText(result)

    G = gpt.ChatGPT_part(gptInput)
    gpt = G.ChatGPT()

    gptOutput = makeGPTOutputText(gpt)

    with st.container():
      col1, col2 = st.columns(2, gap="large")


      # output the transcript of the given audio file
      with col1:
        st.header("음성 기록")
        makeOriginalText(result)


      # get a better conversation transcribtion from ChatGPT
      with col2:
        st.header("ChatGPT가 제안하는 개선된 화법")
        st.text(makeImproveText(gptOutput))
      
      

# when a YouTube link is received
elif len(url) != 0 and audiofile is None:
  st.write(f"we got the following link: {url}. Will be right back with a better conversation!")

  # extract audio part from the given url(YouTube video)
  ydl_opts = {
    'format': 'm4a/bestaudio/best',
    "outtmpl" : 'conversation',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }]
 }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(url)
  makeAudio()
  #num_speakers = gs.get_num_speakers("conversation.wav")
  T = t.Transcribe("conversation.wav",  False)
  result = T.diarization()
  gptInput = makeGPTInputText(result)

  G = gpt.ChatGPT_part(gptInput)
  gpt = G.ChatGPT()

  gptOutput = makeGPTOutputText(gpt)



  with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
      st.header("음성 기록")
      makeOriginalText(result)
    
    with col2:
      st.header("ChatGPT가 제안하는 개선된 화법")
      try:
        st.text(makeImproveText(gptOutput))
      except:
         pass



