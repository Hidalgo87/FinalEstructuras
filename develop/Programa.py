import pickle

from develop.Grafo import Grafo
from develop.Lector import Lector


class Programa:
    def actualizarGrafo_ConTxt_EnSerializado(self):
        l = Lector()
        peliculas, diccionario = l.obtener_peliculasYdiccionario()
        g = Grafo(1)
        g.matriz_adyacencia = [[[0]]]
        nombre_pelicula = peliculas[0]
        g.listaNombres = [nombre_pelicula]
        info = diccionario[nombre_pelicula]
        directores = info[0]
        guionistas = info[1]
        actores = info[2]
        for director in directores:
            g.agregar_nodo(nombre_pelicula, director, 5, 4)
        for guionista in guionistas:
            g.agregar_nodo(nombre_pelicula, guionista, 0, 3)
        for actor in actores:
            g.agregar_nodo(nombre_pelicula, actor, 2, 1)
        i = 1
        for nombre_pelicula in peliculas[1:]:
            i += 1
            info = diccionario[nombre_pelicula]
            directores = info[0]
            guionistas = info[1]
            actores = info[2]
            print(f"{i}:{nombre_pelicula}")
            for director in directores:
                g.agregar_nodo(nombre_pelicula, director, 5, 4)
            for guionista in guionistas:
                g.agregar_nodo(nombre_pelicula, guionista, 0, 3)
            for actor in actores:
                g.agregar_nodo(nombre_pelicula, actor, 2, 1)
        g.visualizar_grafo_libreria()
        print(len(g.listaNombres))
        objeto_serializado = pickle.dumps(g)

        with open("objeto_serializado.pickle", "wb") as archivo:
            archivo.write(objeto_serializado)

    def crearGrafo_ConSerializado(self):
        with open("objeto_serializado.pickle", "rb") as archivo:
            obj = archivo.read()
            objeto_deserializado = pickle.loads(obj)

        l = Lector()
        peliculas, diccionario = l.obtener_peliculasYdiccionario()
        rafo = Grafo(0)
        rafo.dim = objeto_deserializado.dim
        rafo.listaNombres = objeto_deserializado.listaNombres
        rafo.matriz_adyacencia = objeto_deserializado.matriz_adyacencia
        rafo.Camino = objeto_deserializado.Camino
        rafo.visitados = objeto_deserializado.visitados

        lista = [pelicula for pelicula in peliculas if pelicula in rafo.listaNombres]
        print(f"Peliculas: {len(lista)}")
        return rafo
