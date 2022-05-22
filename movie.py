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
        self.page = requests.get(self.url)
        self.bs = BeautifulSoup(self.page.content, 'html.parser')
        self.msg = self.bs.find('td', class_='result_text').find_all('a')
        for i in self.msg:
            self.movie_name = i.text
            self.movie_imdb_link = IMDB_LINK + i['href']

    def get_info(self):
        self.url = self.movie_imdb_link
        self.page = requests.get(self.url)
        self.bs = BeautifulSoup(self.page.content, 'html.parser')
        self.en_sinopsis = self.bs.find_all('span', class_='sc-16ede01-2 gXUyNh')
        traductor = GoogleTranslator(source='en', target='es')
        self.es_sinopsis = str([traductor.translate(i.text) for i in self.en_sinopsis]).replace('[', '').replace(']', '').replace("'", '')

