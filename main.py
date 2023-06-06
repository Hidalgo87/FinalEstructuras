import pickle

from develop.Grafo import Grafo
from develop.Lector import Lector
from develop.Programa import Programa

if __name__ == '__main__':
    p = Programa()
    p.Run()
    grafo = p.crearGrafo_ConSerializado()
    #a = grafo.buscar_coincidencias("leon")
    #print(a)

    #a = grafo.conocer_relacion("Sergio Leone", "Leonardo DiCaprio")
    #a = grafo.conocer_relacion("Bob Gunton", "Morgan Freeman")

    a = grafo.encontrar_camino("Sergio Leone", "Leonardo DiCaprio")
    print(a)

    #nombre, contador = grafo.personaje_mas_recurrente(4)
    #print(f"el man {nombre} tiene {contador} intervenciones")

    # print(grafo.encontrar_peliculasYrelacion("Robert De Niro"))



