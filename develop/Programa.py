import pickle

from develop.Grafo import Grafo
from develop.Lector import Lector


class Programa:

    def __init__(self):
        self.grafo = None

    def actualizarGrafo_ConTxt_EnSerializado(self):
        l = Lector()
        peliculas, diccionario = l.obtener_peliculasYdiccionario()
        g = Grafo(1)
        g.matriz_adyacencia = [[[0]]]
        g.peliculas = peliculas
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
        print(len(g.listaNombres))
        objeto_serializado = pickle.dumps(g)

        with open("objeto_serializado.pickle", "wb") as archivo:
            archivo.write(objeto_serializado)

    def crearGrafo_ConSerializado(self) -> Grafo:
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
        rafo.peliculas = peliculas

        lista = [pelicula for pelicula in peliculas if pelicula in rafo.listaNombres]
        return rafo

    def solicitar_entero(self) -> int:
        try:
            num = int(input("Ingresa un número: "))
            return num
        except Exception:
            self.solicitar_entero()

    def mostrar_menu(self):
        print("------------------------------------- MENÚ -------------------------------------")
        print("1. Buscar una persona o película por un fragmento de su nombre")
        print("2. Conocer el tipo de una persona: actriz, director o escritor")
        print("3. Conocer la relación entre dos nodos")
        print("4. Conocer el actor que ha actuado en más películas")
        print("5. Conocer el director que más películas ha dirigido")
        print("6. Conocer todas las películas, y su rol, en las que ha trabajado una persona")

    def solicitar_persona_o_pelicula(self):
        posible_item = input("Ingrese el nombre exacto de la persona: ")
        if posible_item in self.grafo.listaNombres:
            return posible_item
        else:
            print("La persona o película ingresada no se encuentra en el grafo")
            return self.solicitar_persona_o_pelicula()

    def ejecutar_metodos(self, opcion):
        if opcion == 1:
            item = input("Ingrese un fragmento del nombre que busca: ")
            ListaEncontrados = self.grafo.buscar_coincidencias(item)
            if len(ListaEncontrados) > 0:
                for nombre in ListaEncontrados:
                    print(f"{nombre}")
            else:
                print(f"No se encontraron coincidencias")
        elif opcion == 2:
            persona = self.solicitar_persona_o_pelicula()
            texto_resultado = self.grafo.tipo_persona(persona)
            print(texto_resultado)
        elif opcion == 3:
            self.grafo.Camino = []
            self.grafo.visitados = []
            print("Ingresa el nombre del nodo origen")
            n1 = self.solicitar_persona_o_pelicula()
            print("Ingresa el nombre del nodo destino")
            n2 = self.solicitar_persona_o_pelicula()
            resultado = self.grafo.encontrar_camino(n1, n2)
            cadena = ""
            for palabra in resultado:
                cadena += palabra
            print(cadena)
        elif opcion == 4:
            response = self.grafo.personaje_mas_recurrente(1)
            print(response)
        elif opcion == 5:
            response = self.grafo.personaje_mas_recurrente(4)
            print(response)
        elif opcion == 6:
            persona = self.solicitar_persona_o_pelicula()
            response = self.grafo.encontrar_peliculasYrelacion(persona)
            print(response)
        else:
            print("Intenta otra vez")

    def Run(self):
        self.grafo = self.crearGrafo_ConSerializado()
        #print(self.grafo.encontrar_camino("Reservoir Dogs", "Leonardo DiCaprio"))
        while True:
            self.mostrar_menu()
            opcion = self.solicitar_entero()
            self.ejecutar_metodos(opcion)
