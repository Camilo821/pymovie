from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import requests
import os
IMDB_LINK_FIND = 'https://www.imdb.com/find?q='
IMDB_LINK = 'https://www.imdb.com'
class Movie:
    name:str
    #poster_link:str
    #sinopsis:str
    #reparto:list[str]
    #director:str
    #producers:list[str]

    def __init__(self, name):
        self.name = name
    
    def get_movie(self):
        self.url = IMDB_LINK_FIND + self.name
        self.__page = requests.get(self.url)
        self.__bs = BeautifulSoup(self.__page.content, 'html.parser')
        self.__msg = self.__bs.find('td', class_='result_text').find_all('a')
        for i in self.__msg:
            self.movie_name = i.text
            self.movie_imdb_link = IMDB_LINK + i['href']

    def get_info(self):
        self.__page = requests.get(self.movie_imdb_link)
        self.__bs = BeautifulSoup(self.__page.content, 'html.parser')
        self.en_sinopsis = self.__bs.find_all('span', class_='sc-16ede01-2 gXUyNh')
        self.__traductor = GoogleTranslator(source='en', target='es')
        self.es_sinopsis = str([self.__traductor.translate(i.text) for i in self.en_sinopsis]).replace('[', '').replace(']', '').replace("'", '')
        self.__rate_html = self.__bs.find_all('span', class_='sc-7ab21ed2-1 jGRxWM', limit=1)
        self.rate = float(str([i.text for i in self.__rate_html]).replace('[', '').replace(']', '').replace("'", ''))
        self.__director = self.__bs.find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        self.director = str([i.text for i in self.__director]).replace('[', '').replace(']', '').replace("'", '')


