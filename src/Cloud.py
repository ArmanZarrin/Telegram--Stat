from typing import Union
from pathlib import Path
import json
from src.Data import DATA_DIR

from hazm import word_tokenize , Normalizer
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display
from loguru import logger


class ChatStatistics:
    """ Derive Chat Statistics from Telegram chat history in json file
    """
    def __init__(self, json_file: Union[str,Path]):
        #load Chatdata
        with open(json_file) as f:
            self.chat_data=json.load(f)
        #load stopwords
        self.normalizer=Normalizer();
        stop_words= open(DATA_DIR/'stopwords.txt').readlines()
        stop_words= list(map(str.strip, stop_words))
        self.stop_words=list(map(self.normalizer.normalize,stop_words))
        logger.info("importing stopwords");

    def cloud(self,outputpath):
        text_content='';
        for msg in self.chat_data['messages']:
            try:
                if (type(msg['text']) is str):
                    msg['text']=self.normalizer.normalize(msg['text'])
                    words=word_tokenize(msg['text'])
                    words=list(filter(lambda item: item not in self.stop_words,words))
                    text_content+= f" {' '.join(words)}"
            except:
                pass

        logger.info("text_content is ready")
        text = arabic_reshaper.reshape(text_content)
        text = get_display(text)

        # Generate a word cloud image
        wordcloud = WordCloud(
            font_path=str(DATA_DIR/'B Nazanin.ttf'),
            background_color='White' 
                            ).generate(text)

        #Export to an image
        wordcloud.to_file(outputpath/ "Your_cloud.png")
        logger.info(f"text_content is available at{outputpath}");
        #plot
        import matplotlib.pyplot as plt
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

if(__name__=="__main__"):
     chatdata = ChatStatistics(json_file=DATA_DIR / 'Tahmine.json')
     chatdata.cloud(DATA_DIR)

