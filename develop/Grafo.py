import networkx as nx
import matplotlib.pyplot as plt


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

        print(f"{nombre_pelicula}: {index_pelicula} -> {nombre_personaje}: {index_personaje} = {self.matriz_adyacencia[index_pelicula][index_personaje]}")
        print(f"{nombre_personaje}: {index_personaje} -> {nombre_pelicula}: {index_pelicula} = {self.matriz_adyacencia[index_personaje][index_pelicula]}")
