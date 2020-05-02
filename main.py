import sys
import subprocess

import random

import codecs
import json

from main_jsoncontainer import JsonContainer
from main_httprequest import HttpRequest 
from main_audioplayer import AudioPlayer
from main_awspolly import AWSPolly

E = ''
S = ' '
ARROW = '>'

QUESTION_NUMBER = 150

MSG_WHITE = '\33[37m'
MSG_RED = '\033[91m'

MSG_QUESTION = 'Question'
MSG_ANSWER = 'Answer'

ENGLISH_JSON_FILE_NAME = 'resources/0000.json'

ENCODE_UTF8 = 'utf-8'

JSON_TAG_ENGLISH = 'ENGLISH'
JSON_TAG_ID = 'ID'
JSON_TAG_AUDIO = 'AUDIO'
JSON_TAG_STATE = 'STATE'
JSON_TAG_WORD = 'WORD'
JSON_TAG_MEANS = 'MEANS'
JSON_TAG_MEAN = 'MEAN'
JSON_TAG_SYNONSYM = 'SYNONSYM'
JSON_TAG_USAGES = 'USAGES'
JSON_TAG_USAGE = 'USAGE'
JSON_TAG_SENTENCES = 'SENTENCES'
JSON_TAG_SENTENCE = 'SENTENCE'
JSON_TAG_URI = 'URI'

STATE_REMEMBER = 1
AUDIO_EXIST = 1

'''
    load json file and get "ENGLISH" attribute.
'''
def load():
    with codecs.open(ENGLISH_JSON_FILE_NAME, 'r', ENCODE_UTF8) as file:
        data = json.load(file)
        return data.get(JSON_TAG_ENGLISH)

'''
    get attribute value.
    if element don't have attribute, deal with emtpy.

    element : json element
'''
def getValue(key, element):
    if key in element:
        return element[key]
    else:
        return E

'''
    from json to object.
'''
def createContainer(element):
    container = JsonContainer()
    setattr(container, 'id', getValue(JSON_TAG_ID, element))
    setattr(container, 'state', getValue(JSON_TAG_STATE, element))
    setattr(container, 'audio', getValue(JSON_TAG_AUDIO, element))
    setattr(container, 'word', getValue(JSON_TAG_WORD, element))
    setattr(container, 'means', getValue(JSON_TAG_MEANS, element))
    setattr(container, 'usages', getValue(JSON_TAG_USAGES, element))
    setattr(container, 'sentences', getValue(JSON_TAG_SENTENCES, element))
    setattr(container, 'uri', getValue(JSON_TAG_URI, element))

    return container

'''
    create index of list.
    
    max        : total question number(=length of ENGLISH.json)
    startIndex : ID of json element
    endIndex   : ID of json element
    question   : question number

    for instance,
    jsoin is [{"ID":1}, {"ID":1}, {"ID":2}, {"ID":3}, {"ID":4}, {"ID":4}, {"ID":5}]
    max is 7 and if your set startIndex is 2 and endIndex is 4 and question is 3.

    1. select  : numberList become [2, 3, 4, 5]
    2. shuffle : numberList become [5, 3, 2, 4]
    3. extract : numberList become [5, 3, 2]
'''
def createRandomNumber(max, startIndex, endIndex, question):
    numberList = list(range(0, max, 1))
    numberList = [number for number in numberList if (jsonList[number][JSON_TAG_ID] >= startIndex and jsonList[number][JSON_TAG_ID] <= endIndex)]
    
    random.shuffle(numberList)

    return numberList[0:question]

'''
    play audio.

    content : byte array of mp3
'''
def audio_content(content: bytearray):
    player = AudioPlayer()
    player.play(content)

'''
    play audio.

    content : byte array of mp3
'''
def audio_sentance_content(sentance):
    polly = AWSPolly()
    polly.get_sentence_mp3(sentance)

'''
    entry point.
'''
if __name__ == '__main__':
    jsonList = load()

    numberList = createRandomNumber(len(jsonList), 1, 200, QUESTION_NUMBER)
    #numberList = createRandomNumber(len(jsonList), 201, 400, QUESTION_NUMBER)
    
    for index, number in enumerate(numberList):
        print(MSG_WHITE)
        
        container = createContainer(jsonList[number])

        if container.state != STATE_REMEMBER:
            request = HttpRequest()

            if container.audio == AUDIO_EXIST:
                if container.uri == E:
                    uri = request.get_uri(container.word)

                    # TODO : should be single model ...
                    container.uri = uri
                    jsonList[number][JSON_TAG_URI] = uri

                if container.uri != E:
                    content = request.get_html_content(uri)

                    # if empty, repeat audio
                    value = E

                    while value == E:
                        try:
                            audio_content(content)
                        except:
                            pass  

                        value = input(ARROW)
                    
                    #with open(ENGLISH_JSON_FILE_NAME, 'w') as file:
                    #    json.dump({JSON_TAG_ENGLISH: jsonList}, file, ensure_ascii=False)
                else:
                    print('URI of [' + container.word + '] is empty.')
            
            # question
            print(MSG_WHITE)
            print(MSG_QUESTION + S + str(index) + ' : ' + str(container.id) + S + str(container.word))
            print(MSG_QUESTION + S + str(index) + ' : ' + str(container.id) + S + str(container.usages))
            
            # input
            input(ARROW)

            # answer
            print(MSG_RED)
            print(MSG_ANSWER + ' : ' + str(container.means))

        
