from io import BufferedReader, BufferedWriter

import requests
from bs4 import BeautifulSoup
import pandas as pd


class Movie:
    def __init__(self, nombre, url):
        self.nombre = nombre
        self.url = url


class WebScrapper:
    def __init__(self):
        self.diccionario = {}

    def obtener_movies_urls(self):
        """
        El método obtiene las URL´S  y nombre y retorna lista de objetos Movie
        :return: list[str]
        """
        url = "https://www.imdb.com/chart/top/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # este elemento tendrá 250 tr dentro con toda la info de las pelis
        lista_peliculas = soup.find('tbody', class_='lister-list')

        lista_movies = []
        # itero sobre los 250 tr
        for pelicula in lista_peliculas.find_all('tr'):
            # El nodo que contiene los atributos que me interesan
            nombre_columna = pelicula.find('td', class_='titleColumn')
            # Me trae el nodo <a>, que contiene nombre y href
            info = nombre_columna.find('a')
            # El nombre está entre > <, entonces es innertext, y puede salir con espacios innecesarios -> chao
            nombre = info.get_text(strip=True)
            # Obtener el valor que tiene el atributo href en el nodo <a>
            href = info['href']
            # objeto movie con nombre y link usable, se agrega a lista
            m = Movie(nombre, "https://www.imdb.com"+href)
            lista_movies.append(m)
        return lista_movies

    def escribir_movie_info_diccionario(self, movie):
        nombre = movie.nombre
        link = movie.url
        # No me estaba dejando hacer la peticion URL, por lo que tocó usar headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        page = requests.get(link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        """# hay un elemento <a> con ese atributote que su inner text es el name del director
        director = soup.find('a', class_='ipc-metadata-list-item__list-content-item').get_text(strip=True)


        # estaba duro scrapear esto arriba, entonces mas abajo donde estan todos los actores se pueden coger los
        # 3 primeros
        lista_actores = soup.find_all('a', attrs={'data-testid': 'title-cast-item__actor'})
        actores = [actor.get_text(strip=True) for actor in lista_actores]
        actores = actores[0:3]

        guionistas_list = soup.find_all('a', class_='ipc-metadata-list-item__list-content-item')
        guionistas = []
        for guionista in guionistas_list[1:-1]:
            # print(guionista.get_text(strip=True))
            if guionista.get_text(strip=True) in actores and len(guionistas) != 0:
                break
            else:
                guionistas.append(guionista.get_text(strip=True))"""

        ul = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt")
        elementos_li = ul.find_all('li')
        index_director = -1
        index_guionistas = -1
        index_actores = -1
        i=0
        lista_texto = []
        for li in elementos_li:
            texto = li.text
            lista_texto.append(texto)
            if texto.__contains__("Director"):
                index_director = i
            elif texto.__contains__("Writers") or texto.__contains__("Writer"):
                index_guionistas = i
            elif texto.__contains__("Stars"):
                index_actores = i
            else:
                pass
            i += 1
        directores = lista_texto[index_director+1:index_guionistas]
        guionistas = lista_texto[index_guionistas+1:index_actores]
        actores = lista_texto[index_actores+1:]



        # info = [ Directores: list, Guonistas: list, Actors: list ]
        info = [directores, guionistas, actores]
        self.diccionario[nombre] = info
        print(f"Pelicula: {nombre}")
        print(f"Director: {directores}")
        print(f"Guionistas: {guionistas}")
        print(f"Actores: {actores}")


    def escribir_en_txt(self):
        nombres = self.diccionario.keys()
        for nombre in nombres:
            info_pelicula = self.diccionario.get(nombre)
            directores = info_pelicula[0]
            guionistas = info_pelicula[1]
            actores = info_pelicula[2]
            director_str = ""
            guionista_str = ""
            actor_str = ""
            for director in directores:
                director_str = director_str + "," + director
            for guionista in guionistas:
                guionista_str = guionista_str + "," + guionista
            for actor in actores:
                actor_str = actor_str + "," + actor
            director_str = director_str[1:]
            guionista_str = guionista_str[1:]
            actor_str = actor_str[1:]

            archivo = open("info.txt", "a")
            archivo.write(f"{nombre}-?{director_str};{guionista_str};{actor_str}\n")


ws = WebScrapper()
lista_movies = ws.obtener_movies_urls()
for movie in lista_movies:
    ws.escribir_movie_info_diccionario(movie)
ws.escribir_en_txt()