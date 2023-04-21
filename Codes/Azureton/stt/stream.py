import streamlit as st
import get_speakers as gs
#import transcribe

# visual components
st.title("Hi! We recommend a better conversation for you")

# get an audio file; wav and mp3 are allowed to be uploaded
audiofile = st.file_uploader("Upload an audio file! You can upload .wav or .mp3", type = ["wav", "mp3"] )

if audiofile is not None:
    # when an audio file is given, show the name of it
    st.write(f"we got \"{audiofile.name}\" file from you")

    # num_speakers = gs.get_num_speakers(audiofile)
    # if num_speakers <= 1:
    #     st.write(f"we found {num_speakers} person in your audio file!")

    # else:
    #     st.write(f"we found {num_speakers} people in your audio file!")


# or get a YouTube link
url = st.text_input("Or copy and paste a YouTube link!")

if len(url) != 0:
    st.write(f"we got the following link: {url}")