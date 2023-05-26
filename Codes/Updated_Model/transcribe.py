import whisper
import datetime
import librosa
import torch
import numpy as np
import pyannote.audio
# from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
# embedding_model = PretrainedSpeakerEmbedding( 
#     "speechbrain/spkrec-ecapa-voxceleb",
#     device=torch.device("cuda"))

from pyannote.audio import Audio
from pyannote.core import Segment
import wave
import contextlib
from sklearn.cluster import AgglomerativeClustering
import locale
locale.getpreferredencoding = lambda: "UTF-8"
import requests
import json
import time


class Transcribe():
    '''
    this class is for getting audio and number of speakers from stream.py
    given those, transcribe the audio
    '''
    #def __init__(self, audio, num_speakers, is_file):
    def __init__(self, audio, is_file):   
        # when given an audio file
        if is_file:
          self.audio = audio
          #self.num_speakers = num_speakers
          self.path = audio.name
          self.language = "any"
          self.model_size = 'medium'


        # when given a link
        else:
          self.path = audio
          #self.num_speakers = num_speakers
          self.language = "any"
          self.model_size = 'medium'


    # available models = ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large']
    def load_whisper_model(self):
      model = whisper.load_model(self.model_size)
      return model

    # execute the trascription
    '''
    load model and transcribe "conversation.wav"
    segments["text"] has transcription
    '''
    def execute(self):
        model = self.load_whisper_model()
        result = model.transcribe("conversation.wav") 
        segments = result["segments"]

        # Whisper가 전사한 대화내용을 맞춤법교정
        for count, x in enumerate(segments):
          response = requests.post('http://164.125.7.61/speller/results', data={'text1': x['text']})
          data = response.text.split('data = [', 1)[-1].rsplit('];', 1)[0]
          if data[0]=='<':
            continue
          data = json.loads(data)
          for err in data['errInfo']:
            var = str(err['candWord'])
            a = var.split('|')
            x['text'] = x['text'].replace(err['orgStr'],a[0])

        return segments


    def segment_wav_file(self, input_file_path, output_file_path, start_ms, end_ms):
    # Open the input WAV file
      with wave.open(input_file_path, 'rb') as input_wav:
        # Get the sample width (in bytes) and the number of channels
        sample_width = input_wav.getsampwidth()
        num_channels = input_wav.getnchannels()
        # Calculate the start and end positions (in frames)
        #start_pos = int(start_ms * input_wav.getframerate() / 1000)
        #end_pos = int(end_ms * input_wav.getframerate() / 1000)
        start_pos = int(start_ms * input_wav.getframerate() )
        end_pos = int(end_ms * input_wav.getframerate())
        # Calculate the number of frames to read
        num_frames = end_pos - start_pos
        # Set the parameters for the output WAV file
        output_wav = wave.open(output_file_path, 'wb')
        output_wav.setparams((num_channels, sample_width, input_wav.getframerate(), num_frames, input_wav.getcomptype(), input_wav.getcompname()))
        # Set the position in the input WAV file
        input_wav.setpos(start_pos)
        # Read the frames from the input WAV file and write them to the output WAV file
        output_wav.writeframes(input_wav.readframes(num_frames))
        # Close the output WAV file
        output_wav.close()

    def diarization(self):
      segments = self.execute()        

      start_end = [(x["start"], x["end"]) for c, x in enumerate(segments)]
      count = 1
      for start, end in start_end:
        self.segment_wav_file("conversation.wav", f"segmented{count}.wav", start, end)
        count += 1
      
      embedding_model = torch.hub.load('RF5/simple-speaker-embedding', 'convgru_embedder')
      # embedding_model.eval() # this shows the architecture of the embedder

      e = []
      # the list "e" has vectors of audio segments
      for count in range(len(start_end)):
        wav, _ = librosa.load(f'segmented{count + 1}.wav', sr=16000)
        wav = torch.from_numpy(wav).float()
        element = embedding_model(wav[None])
        e.append(element)
      
      # convert all vectors to numpy and flatten them
      e2 = [data.cpu().detach().numpy().flatten() for data in e]

      # use clustering
      #clustering = AgglomerativeClustering(n_clusters = self.num_speakers).fit(e2)
      # num_speakers의 정확도가 안 좋은거 같음
      # 그래서 그냥 클러스터의 개수를 명확히 하지 않고 해야할 것으로 판단함
      clustering = AgglomerativeClustering().fit(e2)

      # save the result
      #diarization_result = [ f"Speaker {clustering.labels_[count]} : { x['text'] }" for count, x in enumerate(segments)]

      # (수정) -> 대화 시간 추가
      diarization_result = [[clustering.labels_[count], x['text'], x['start']] for count, x in enumerate(segments)]
      diarization_result = self.CombineText(diarization_result)

      # return the result
      # just print "diarization_result"
      return diarization_result
    
    # 같은 사람이 말하는 대화 합치기
    def CombineText(self, texts):
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
    

    

    