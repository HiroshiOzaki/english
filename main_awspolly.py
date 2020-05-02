import os

from tempfile import gettempdir

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

class AWSPolly:

    AWS_POLLY = 'polly'
    AWS_PROFILE = 'default'
    AWS_REGION = 'us-west-2'

    AUDIO_STREAM = 'AudioStream'
    AUDIO_VOICE = 'Joanna'
    AUDIO_FILE_NAME = 'speech.mp3'

    DIRECTORY_NAME = 'resources/'
    
    def __init__(self):
        pass

    def create_path(self, sentence):
        return self.DIRECTORY_NAME + sentence + '.mp3'

    def get_sentence_mp3(self, sentence):
        try:
            session = Session(profile_name=self.AWS_PROFILE, region_name=self.AWS_REGION)
            polly = session.client(self.AWS_POLLY)
            response = polly.synthesize_speech(Text=sentence, OutputFormat="mp3", VoiceId=self.AUDIO_VOICE)

            if self.AUDIO_STREAM in response:
                with closing(response[self.AUDIO_STREAM]) as stream:
                    output = os.path.join(gettempdir(), self.AUDIO_FILE_NAME)

                    try:
                        with open(self.create_path(sentence), "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        print('AWS POLLY ERROR of [' + sentence + '].')
        except (BotoCoreError, ClientError) as error:
            print('AWS ERROR.')
