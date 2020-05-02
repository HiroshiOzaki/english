import io

import ffprobe
import ffmpeg

from pydub import AudioSegment
from pydub.playback import play

# pip3 install pydub
# pip3 install ffprobe-python
# pip3 install ffmpeg-python

# https://evermeet.cx/ffmpeg/
# download ffmpeg  and add to PATH or move /usr/local/bin
# dwonload ffplay  and add to PATH or move /usr/local/bin
# dwonload ffprove and add to PATH or move /usr/local/bin

class AudioPlayer:

    def __init__(self):
        pass
    
    '''
        play audio.
        
        (notice) must install ffmpeg and ffplay and ffprove.
    '''
    def play(self, content):
        audio = AudioSegment.from_file(io.BytesIO(content), format='mp3')
        play(audio)

        
        
