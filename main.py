from movie import Movie
from movie import TMDB_LINK, TMDB_LINK_FIND
import tkinter as tk
import customtkinter as ctk
import requests
import pandas as pd
import numpy as np
import os
from io import BytesIO
from PIL import Image, ImageTk
ctk.set_appearance_mode("dark")
file_path = './movies.csv'
window = ctk.CTk()
window.title("Pymovie")
window.geometry("850x500")
tittle = ctk.CTkLabel(window, text="Bienvenido a Pymovie", font=("Arial", 14))
def save_movie(movie, own_rate):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=['name', 'type', 'genres', 'director', 'rate_tmdb', 'own_rate', 'release'])
    
    df = pd.concat([df, pd.DataFrame({'name': [movie.name], 'type': [movie.type], 'genres': [movie.genres], 'director': [movie.director], 'rate_tmdb': [movie.rate], 'own_rate': [own_rate], 'release': [pd.to_datetime(movie.release)]})])
    df.to_csv('movies.csv', index=False)
    print(df)
def remove_db():
    df = pd.read_csv('./movies.csv')
    df.drop(df.index, inplace=True)
    df.to_csv('movies.csv', index=False)
    print(df)
def image_from_url(url):
    response = requests.get(url, timeout=10)  # Descargar la imagen
    if response.status_code == 200:  # Si la descarga fue exitosa
        image_data = BytesIO(response.content)  # Leer la imagen en memoria
        image = Image.open(image_data)  # Abrir la imagen con Pillow
        return ImageTk.PhotoImage(image)  # Convertirla para usarla en tkinter
    else:
        print("No se pudo descargar la imagen")
        return None
#ttk.Label(window, text="Ingresa el nombre de la película que quieres buscar: ").grid(column=0, row=1, padx=10, pady=5, sticky="w")
search = ctk.CTkEntry(window, placeholder_text="Ingresa el nombre de la película", width=250)
search.grid(column=0, row=1, padx=10, pady=5)
text_label = tk.StringVar()
text_label.set("")
results = ctk.CTkLabel(window, textvariable=text_label, font=("Arial", 10))
results.grid(column=0, row=3, padx=10, pady=5)
def search_movie(selection_entry, movies, movie):
    selection = int(selection_entry.get())
    movie.get_info(TMDB_LINK + movies[selection]['href'])
    movie_window = ctk.CTkToplevel(window)
    movie_window.title(f"{movies[selection].text} ({movie.type})")
    movie_window.geometry("700x300")
    rate_label = ctk.CTkLabel(movie_window, text=f"Al {movie.rate}% de las personas les gustó")
    rate_label.grid(column=0, row=1, padx=10, pady=5)
    genres_label = ctk.CTkLabel(movie_window, text=f"Los generos de la película son {str(movie.genres).replace('[', '').replace(']', '').replace("'", '')}")
    genres_label.grid(column=0, row=2, padx=10, pady=5)
    director_label = ctk.CTkLabel(movie_window, text=f"El director es {movie.director}")
    director_label.grid(column=0, row=3, padx=10, pady=5)
    release_label = ctk.CTkLabel(movie_window, text=f"Se lanzó en el año {movie.release}")
    release_label.grid(column=0, row=4, padx=10, pady=5)
    print(movie.image_link)
    response = requests.get(movie.image_link, timeout=10)
    image_data = BytesIO(response.content)
    image = Image.open(image_data)
    image_width, image_height = image.size
    image = image.resize((int(image_width/2), int(image_height/2)))
    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(movie_window, image=image_tk)
    image_label.image = image_tk
    image_label.grid(column=0, row=0, padx=10, pady=5)
    sinopsis_label = ctk.CTkTextbox(movie_window, wrap="word", height=150, width=300)  # wrap="word" asegura que el texto no corte palabras
    sinopsis_label._textbox.insert(
    "1.0",
    movie.es_sinopsis)
    sinopsis_label.configure(state="disabled")
    sinopsis_label.grid(column=1, row=0, padx=10, pady=5)
    own_rate_entry = ctk.CTkEntry(movie_window, placeholder_text="Ingresa tu calificación del 1 al 10")
    own_rate_entry.grid(column=1, row=1, padx=10, pady=5)
    own_rate_button = ctk.CTkButton(movie_window, text="Guardar", command=lambda : save_movie(movie, own_rate=own_rate_entry.get()))
    own_rate_button.grid(column=1, row=2, padx=10, pady=5)
def search_info():
    search_text = search.get()
    movie = Movie(search_text)
    movie.get_movie()
    label_text = ""
    for i in range(0, len(movie.movies)):
        label_text = label_text + f"\n {i}. {movie.movies[i].text}"
    text_label.set(label_text)
    selection_entry = ctk.CTkEntry(window, width=250)
    selection_entry.grid(column=0, row=4, padx=10, pady=5)
    selection_button = ctk.CTkButton(window, text="Buscar", command=lambda : search_movie(selection_entry, movie.movies, movie))
    selection_button.grid(column=1, row=4, columnspan=2, pady=10)


search_button = ctk.CTkButton(window, text="Enviar", command=search_info)
search_button.grid(column=0, row=2, columnspan=2, pady=10)
reset_button = ctk.CTkButton(window, text="Reiniciar Excel", command=remove_db)
reset_button.grid(column=1, row=2, columnspan=2, pady=10)



# print(movie.movie_imdb_link)
# movie.get_info()
# print(movie.es_sinopsis)
# print(f"{movie.rate}% Puntuación de los usuarios")
# print(movie.director)



window.mainloop()