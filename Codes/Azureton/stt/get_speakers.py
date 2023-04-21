'''
add 2 seconds silence to the existing conversation.wav
this makes a better diarization
'''

from huggingface_hub import login
login("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")

from pydub import AudioSegment
from pyannote.audio import Pipeline

# authorization key should not be exposed
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token="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")


def get_num_speakers(original_audio):
    '''
    given an audio file,
    return the number of speakers in an audio file: original_audio
    '''

    t1 = 0 * 1000 # Works in milliseconds
    t2 = 10 * 60 * 1000 # t1:t2 is total 10mins

    newAudio = AudioSegment.from_wav(original_audio)
    a = newAudio[t1:t2]
    a.export("conversation_new.wav", format="wav") 

    audio = AudioSegment.from_wav("conversation_new.wav")
    spacermilli = 2000
    spacer = AudioSegment.silent(duration=spacermilli)
    audio = spacer.append(audio, crossfade=0)

    audio.export('audio.wav', format='wav')

    # 4. apply pretrained pipeline
    diarization = pipeline("audio.wav")

    how_many = set()
    # 5. print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        how_many.add(int(speaker[-2:]))

    # the length of how_many is the total number of speakers in an audio file
    #print(len(how_many))

    return len(how_many)