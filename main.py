from movie import Movie

def run():
    doctor_strange = Movie(input("Ingresa una película o serie"))
    doctor_strange.get_movie()
    print(doctor_strange.movie_imdb_link)
    doctor_strange.get_info()
    print(doctor_strange.es_sinopsis)



if __name__ == '__main__':
    run()
