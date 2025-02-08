from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import requests
import os
import re
TMDB_LINK_FIND = 'https://www.themoviedb.org/search?query='
TMDB_LINK = 'https://www.themoviedb.org'
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
        self.url = TMDB_LINK_FIND + self.name
        self.__page = requests.get(self.url)
        self.__bs = BeautifulSoup(self.__page.content, 'html.parser')
        self.__msg = self.__bs.find('div', class_='results').find_all('div', class_="title")
        self.__msg = [x.find('a') for x in self.__msg]
        self.movies = self.__msg
        # for i in range(0, len(self.__msg)):
        #     print(f"{i}. {self.__msg[i].text}")
            # self.movie_name = i.text
            # self.movie_imdb_link = TMDB_LINK + i['href']
        # self.__selection = int(input("Ingrese el numero de la película que desea: "))
        # self.movie_name = self.__msg[self.__selection].text
        # self.movie_imdb_link = TMDB_LINK + self.__msg[self.__selection]['href']
    def get_info(self, movie_link):
        self.__page = requests.get(movie_link)
        self.__bs = BeautifulSoup(self.__page.content, 'html.parser')
        self.en_sinopsis = self.__bs.find_all('div', class_='overview')
        self.__traductor = GoogleTranslator(source='en', target='es')
        self.es_sinopsis = str([self.__traductor.translate(i.text) for i in self.en_sinopsis]).replace('[', '').replace(']', '').replace("'", '')
        self.rate = self.__bs.find('div', class_='user_score_chart')['data-percent']
        # self.rate = str([i.text for i in self.__rate_html]).replace('[', '').replace(']', '').replace("'", '')
        self.__director = self.__bs.find('li', class_="profile").find_all('a')
        self.director = str([i.text for i in self.__director]).replace('[', '').replace(']', '').replace("'", '')
        self._cast = self.__bs.find('ol', class_="scroller").find_all('p')
        self._cast.pop(-1)
        self.actor = []
        self.role = []
        for i in range(0, len(self._cast)):
            if i%2==0:
                self.actor.append(self._cast[i].text)
            else:
                self.role.append(self._cast[i].text)
        self.image_link = self.__bs.find('img', class_="poster")
        self.image_link = self.image_link['src']
        self.certification = self.__bs.find('span', class_="certification").content
        self.release = self.__bs.find('span', class_="release")
        if self.release:
            self.release = self.release.get_text().replace(' (US)', '')
            self.release = re.sub(r'\([^)]*\)', '', self.release)
            self.type = 'pelicula'
        else:
            self.release = self.__bs.find('span', class_="release_date").get_text().replace('(', '').replace(')', '')
            self.type = 'serie'
        self.genres = self.__bs.find('span', class_="genres").find_all('a')
        self.genres = [self.__traductor.translate(x.get_text()).lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for x in self.genres]
        self.runtime = self.__bs.find('span', class_="runtime")
        # for i in range(0, len(self.actor)):
        #     print(f"{self.actor[i]} - {self.papel[i]}")

