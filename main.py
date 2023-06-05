import pickle

from develop.Grafo import Grafo
from develop.Lector import Lector
from develop.Programa import Programa

if __name__ == '__main__':
    p = Programa()
    grafo = p.crearGrafo_ConSerializado()

    print(f"Nodos: {len(grafo.listaNombres)}")
