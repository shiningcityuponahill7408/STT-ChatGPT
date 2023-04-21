from get_speakers import get_num_speakers
import whisper
import datetime

import subprocess

import torch
import pyannote.audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
embedding_model = PretrainedSpeakerEmbedding( 
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cuda"))

from pyannote.audio import Audio
from pyannote.core import Segment

import wave
import contextlib

from sklearn.cluster import AgglomerativeClustering
import numpy as np



'''
여기에서는 음성파일을 받아서
get_speakers.py 로 부터는 음성파일 속에 몇명이 있는지를 받아서
대화 전사를 하는 파일
'''


def get_file():
    ''' 
    called by stream.py, this function will get an auidio file
    '''

    
    






path = "conversation.wav"

num_speakers = len(get_num_speakers("conversation.wav")) # conversation.wav is the original audio file

language = 'any' 

model_size = 'large-v2' 

model_name = model_size
if language == 'English' and model_size != 'large':
  model_name += '.en'

# I added this codes
import locale
locale.getpreferredencoding = lambda: "UTF-8"


# available models = ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large']
def load_whisper_model():
  model = whisper.load_model(model_size)
  return model


model = load_whisper_model()
result = model.transcribe(path)
segments = result["segments"]

# print the result of whisper speech-to-text
# for i, x in enumerate(segments):
#   print(x)

with contextlib.closing(wave.open(path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
duration = frames / float(rate)

audio = Audio()


def segment_embedding(segment):
  start = segment["start"]
  # Whisper overshoots the end timestamp in the last segment
  end = min(duration, segment["end"])
  clip = Segment(start, end)
  waveform, sample_rate = audio.crop(path, clip)
  return embedding_model(waveform[None])


import codecs
def time(secs):
    return datetime.timedelta(seconds=round(secs))

def get_results():

    embeddings = np.zeros(shape=(len(segments), 192))
    for i, segment in enumerate(segments):
        embeddings[i] = segment_embedding(segment)

    embeddings = np.nan_to_num(embeddings)

    clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
    labels = clustering.labels_
    for i in range(len(segments)):
        segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

    result = [ seg["speaker"] + ": " + seg["text"] for c, seg in enumerate(segments)]
    return result


#f = codecs.getwriter("utf8")( open("transcript.txt", "wb"))
# for (i, segment) in enumerate(segments):
#   if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
#     f.write("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + " ")
#   f.write(str(segment["text"][1:]) + ' ' + "\n")
# f.close()

# for (i, segment) in enumerate(segments):
#    print(segment["speaker"], ":", segment["text"])