import codecs

import networkx as nx
import matplotlib.pyplot as plt
import unidecode as unidecode


class Grafo:

    def __init__(self, dim):
        self.dim = dim
        self.matriz_adyacencia = [[[0]] * dim for _ in range(dim)]
        self.listaNombres = [None for _ in range(dim)]
        self.visitados = []
        self.Camino = []

    def imprimir_matriz(self):
        print(self.listaNombres)
        for fila in self.matriz_adyacencia:
            print(fila)


    def visualizar_grafo_libreria(self):
        G = nx.DiGraph()  # Utilizar un grafo dirigido

        # Agregar nodos al grafo
        for nombre in self.listaNombres:
            G.add_node(nombre)

        # Agregar aristas al grafo con pesos diferentes en cada dirección
        for i in range(self.dim):
            for j in range(self.dim):
                peso1 = self.matriz_adyacencia[i][j][0]
                peso2 = self.matriz_adyacencia[j][i][0]
                if peso1 != 0:
                    G.add_edge(self.listaNombres[i], self.listaNombres[j], weight1=peso1)
                if peso2 != 0:
                    G.add_edge(self.listaNombres[j], self.listaNombres[i], weight2=peso2)

        # Dibujar el grafo
        pos = nx.spring_layout(G)  # Asignar posiciones a los nodos
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        #nx.draw_networkx_labels(G, pos)

        # Dibujar las etiquetas de los pesos
        labels1 = nx.get_edge_attributes(G, 'weight1')
        labels2 = nx.get_edge_attributes(G, 'weight2')
        labels = {**labels1, **labels2}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Mostrar el grafo
        plt.axis('off')
        plt.show()

    def agregar_nodo(self, nombre_pelicula, nombre_personaje, relacion_pelicula_personaje, relacion_personaje_pelicula):
        """Metodo para crear un nodo en el grafo y relacionarlos, o en su defecto
        si el lo que se recibe en nuevo_nombre ya existe se relaciona"""
        index_pelicula = -1
        index_personaje = -1
        for i in range(len(self.listaNombres)):
            if self.listaNombres[i] == nombre_pelicula:
                index_pelicula = i
            if self.listaNombres[i] == nombre_personaje:
                # Si el nuevo_nombre está en la lista, se toma ese
                index_personaje = i
        # Si el personaje o pelicula no se encontró en la lista, entonces se amplia la matriz
        # y se agrega el nombre a la lista
        if index_pelicula == -1:
            self.listaNombres.append(nombre_pelicula)
            self.dim += 1
            index_pelicula = self.dim - 1
            copia_matriz = self.matriz_adyacencia
            #self.matriz_adyacencia = [[[0]] * self.dim for _ in range(self.dim)]
            self.matriz_adyacencia = [[[0] for _ in range(self.dim)] for _ in range(self.dim)]
            # el -1 es para que no toque la nueva fila y columna, pues no existia en la pasada, por lo que no
            # existe en la copia
            for i in range(0, self.dim - 1):
                for j in range(0, self.dim - 1):
                    self.matriz_adyacencia[i][j] = copia_matriz[i][j]
        if index_personaje == -1:
            self.listaNombres.append(nombre_personaje)
            self.dim += 1
            index_personaje = self.dim - 1
            copia_matriz = self.matriz_adyacencia
            #self.matriz_adyacencia = [[[0]] * self.dim for _ in range(self.dim)]
            self.matriz_adyacencia = [[[0] for _ in range(self.dim)] for _ in range(self.dim)]

            # el -1 es para que no toque la nueva fila y columna, pues no existia en la pasada, por lo que no
            # existe en la copia
            for i in range(0, self.dim - 1):
                for j in range(0, self.dim - 1):
                    self.matriz_adyacencia[i][j] = copia_matriz[i][j]


        # Las dos posiciones simetricas deben conectarse
        if relacion_pelicula_personaje == 0:
            pass
        else:
            if self.matriz_adyacencia[index_pelicula][index_personaje][0] == 0:

                self.matriz_adyacencia[index_pelicula][index_personaje].pop()
                self.matriz_adyacencia[index_pelicula][index_personaje].append(relacion_pelicula_personaje)
            else:
                self.matriz_adyacencia[index_pelicula][index_personaje].append(relacion_pelicula_personaje)

        if relacion_personaje_pelicula == 0:
            pass
        else:
            if self.matriz_adyacencia[index_personaje][index_pelicula][0] == 0:

                self.matriz_adyacencia[index_personaje][index_pelicula].pop()

                self.matriz_adyacencia[index_personaje][index_pelicula].append(relacion_personaje_pelicula)

            else:

                self.matriz_adyacencia[index_personaje][index_pelicula].append(relacion_personaje_pelicula)

        #print(f"{nombre_pelicula}: {index_pelicula} -> {nombre_personaje}: {index_personaje} = {self.matriz_adyacencia[index_pelicula][index_personaje]}")
        #print(f"{nombre_personaje}: {index_personaje} -> {nombre_pelicula}: {index_pelicula} = {self.matriz_adyacencia[index_personaje][index_pelicula]}")

    def buscar_coincidencias(self, NombreABuscar):
        ListaEncontrados = []
        for nombre in self.listaNombres:
            if nombre.lower().__contains__(NombreABuscar.lower()):
                ListaEncontrados.append(nombre)
        """if len(ListaEncontrados) > 0:
            for nombre in ListaEncontrados:
                print(f"{nombre}")
        else:
            print(f"No se encontraron coincidencias para {NombreABuscar}")"""

        return ListaEncontrados

    # --------------------------------------------

    def tipo_persona(self, NombreBuscar):
        try:
            indice = self.listaNombres.index(NombreBuscar)
        except ValueError:
            return "Debe ser un nombre de una persona"
        Datos = self.matriz_adyacencia[indice]
        Tipos = []
        for arreglo in Datos:
            if arreglo[0] == 0:
                pass
            else:
                for num in arreglo:
                    if num in Tipos:
                        pass
                    else:
                        Tipos.append(num)
        if len(Tipos) > 0:
            que_es = f"{NombreBuscar} Es "
            if 1 in Tipos:
                que_es += "Actor, "
            if 3 in Tipos:
                que_es += "Escritor, "
            if 4 in Tipos:
                que_es += "Director, "
            que_es = que_es[:-2]
            return que_es
        else:
            return f"{NombreBuscar} no es nada"

    # --------------------------------------------

    def conocer_relacion(self, v1, v2):
        try:
            indice1 = self.listaNombres.index(v1)
            indice2 = self.listaNombres.index(v2)
        except ValueError:
            return "Debe ser un nombre de una persona"
        Datos1 = self.matriz_adyacencia[indice1]
        Datos2 = self.matriz_adyacencia[indice2]
        lista_indices1 = []
        i = -1
        for arreglo in Datos1:
            i += 1
            if 0 in arreglo:
                pass
            else:
                lista_indices1.append(i)
        lista_indices2 = []
        i = -1
        for arreglo in Datos2:
            i += 1
            if 0 in arreglo:
                pass
            else:
                lista_indices2.append(i)

        """for index in lista_indices1:
            if index in lista_indices2:
                return "melito"
            else:
                pass
        for index in lista_indices1:
            return self.conocer_relacion(self.listaNombres[index], v2)"""

        #print(f"1: {Datos1[51]}")
        #print(f"2: {Datos2[73]}")
        print(f"1: {lista_indices1}")
        print(f"2: {lista_indices2}")


    # --------------------------------------------

    def personaje_mas_recurrente(self, relacion_personaje_pelicula):
        contador_mayor = 0
        indice_mayor = -1
        i = -1
        for fila in self.matriz_adyacencia:
            i += 1
            contador = 0
            for arreglo in fila:
                if relacion_personaje_pelicula in arreglo:
                    contador += 1
            if contador > contador_mayor:
                contador_mayor = contador
                indice_mayor = i
        definitivo = ""
        if relacion_personaje_pelicula == 1:
            definitivo = f"El actor {self.listaNombres[indice_mayor]} aparece en {contador_mayor} Películas"
        elif relacion_personaje_pelicula == 4.:
            definitivo = f"El director {self.listaNombres[indice_mayor]} dirige {contador_mayor} Películas"
        else:
            definitivo = f"Ingresa un actor o director"
        return definitivo

    def encontrar_peliculasYrelacion(self, nombre_persona):
        index = self.listaNombres.index(nombre_persona)
        fila_persona = self.matriz_adyacencia[index]
        roles = []
        cantidad_roles = 0
        diccionario = {}
        i = -1
        for arreglo in fila_persona:
            i += 1
            if 0 in arreglo:
                pass
            else:
                if 1 in arreglo:
                    # es actor
                    roles.append(1)
                    cantidad_roles += 1
                if 3 in arreglo:
                    # es escritor
                    roles.append(3)
                    cantidad_roles += 1
                if 4 in arreglo:
                    # es director
                    roles.append(4)
                    cantidad_roles += 1
                if cantidad_roles > 0:
                    diccionario[self.listaNombres[i]] = roles
                else:
                    pass
        peliculas = diccionario.keys()
        general = f"{nombre_persona} estuvo: \n"
        for pelicula in peliculas:
            texto = f"En {pelicula}, y fue: "
            info_roles = diccionario[pelicula]
            if 1 in info_roles:
                texto += "Actor, "
            if 3 in info_roles:
                texto += "Escritor, "
            if 4 in info_roles:
                texto += "Director, "
            texto = texto[:-2]
            texto += "\n"
            general += texto
        general = general[:-1]
        return general

    def encontrar_camino(self, origen, destino):
        if origen in self.listaNombres:
            if destino in self.listaNombres:
                indice_origen = None
                indice_destino = None
                for i in range(0, len(self.listaNombres)):
                    if self.listaNombres[i] == origen:
                        indice_origen = i
                    if self.listaNombres[i] == destino:
                        indice_destino = i
                lista_conexiones = []  # Nombres de los elementos a los que esta conectado el elemnto origen
                for i in range(0, len(self.listaNombres)):
                    if self.matriz_adyacencia[indice_origen][i][0] != 0:
                        lista_conexiones.append(self.listaNombres[i])
                # print(f"conexiones {origen}: {lista_conexiones}")
                if destino in lista_conexiones:
                    self.Camino.append(f" {origen} -->  {destino} ")
                    return self.Camino
                else:
                    if lista_conexiones.count == 0:
                        return " ñ "
                    else:
                        self.visitados.append(origen)
                        for nuevo_origen in lista_conexiones:
                            if nuevo_origen in self.visitados:
                                continue
                            else:
                                self.Camino.append(f" {origen} --> ")
                                cadena = self.encontrar_camino(nuevo_origen, destino)
                                # print(f"cadena : {cadena}")
                                if cadena == "ñ" or cadena is None:
                                    self.Camino.pop()
                                    continue
                                else:
                                    return cadena
            else:
                print(f"El elemento {destino} no existe en el grafo")
        else:
            print(f"El elemento {origen} no existe en el grafo")
