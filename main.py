from movie import Movie

def run():
    movie = Movie(input("Ingresa una película o serie: "))
    movie.get_movie()
    print(movie.movie_imdb_link)
    movie.get_info()
    print(movie.es_sinopsis)
    print(f"{movie.rate}% Puntuación de los usuarios")
    print(movie.director)



if __name__ == '__main__':
    run()
