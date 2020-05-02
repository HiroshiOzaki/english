import requests

class HttpRequest:

    URL_DICTIONARY = 'https://dictionary.cambridge.org/ja/dictionary/english/'
    URL_MEDIA = 'https://dictionary.cambridge.org/ja/media/english/uk_pron/'

    DOM_TAG_START = '<source type="audio/mpeg" src="/ja/media/english/uk_pron/'
    DOM_TAG_END = '.mp3"/>'

    def __init__(self):
        pass
    
    '''
        get URI of target from cambridge dictionary.
        source tag have URI of target as "src" attribute, parse source tag.

        for instance
        tag of 'test' is <source type="audio/mpeg" src="/ja/media/english/uk_pron/u/ukt/ukter/ukterri013.mp3"/>
        so, audio content of 'test' is https://dictionary.cambridge.org/ja/media/english/uk_pron/u/ukt/ukter/ukterri013.mp3

        target : word
    '''
    def get_uri(self, target):
        html = self.get_html_text(self.URL_DICTIONARY + target)
        
        start_index = html.find(self.DOM_TAG_START)
        end_index = html.find(self.DOM_TAG_END, start_index)

        uri = self.URL_MEDIA + html[start_index + len(self.DOM_TAG_START) : end_index] + '.mp3'

        # TODO : too bad ... shuld validate format ?
        if len(uri) < len(self.URL_MEDIA) * 2:
            return uri
        else:
            return ''

    '''
        get content of URI as byte array.

        path : URI
    '''
    def get_html_content(self, path):
        response = requests.get(path)

        return response.content

    '''
        get html of URI as string.

        path : URI
    '''
    def get_html_text(self, path):
        response = requests.get(path)

        return response.text
        
