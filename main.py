from movie import Movie
from movie import TMDB_LINK, TMDB_LINK_FIND
import tkinter as tk
import customtkinter as ctk
import requests
from io import BytesIO
from PIL import Image, ImageTk
ctk.set_appearance_mode("dark")
window = ctk.CTk()
window.title("Pymovie")
window.geometry("850x500")
tittle = ctk.CTkLabel(window, text="Bienvenido a Pymovie", font=("Arial", 14))
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
    movie_window.title(movies[selection].text)
    movie_window.geometry("700x300")
    rate_label = ctk.CTkLabel(movie_window, text=f"Al {movie.rate}% de las personas les gustó")
    rate_label.grid(column=0, row=1, padx=10, pady=5)
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
    movie.es_sinopsis,)
    sinopsis_label.configure(state="disabled")
    sinopsis_label.grid(column=1, row=0, padx=10, pady=5)
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



# print(movie.movie_imdb_link)
# movie.get_info()
# print(movie.es_sinopsis)
# print(f"{movie.rate}% Puntuación de los usuarios")
# print(movie.director)



window.mainloop()