from io import BufferedReader


class Lector:
    def obtener_peliculasYdiccionario(self):
        diccionario = {}
        archivo = open("develop/info.txt", "r", encoding='utf-8')
        contenido = archivo.readlines()
        archivo.close()
        peliculas = []
        for linea in contenido:
            nombre_info = linea.split("-?")
            nombre_pelicula = nombre_info[0]
            peliculas.append(nombre_pelicula)
            linea = nombre_info[1]
            directores_guionistas_actores = linea.split(";")
            directores = directores_guionistas_actores[0].split(",")
            guionistas = directores_guionistas_actores[1].split(",")
            # Hay que hacer split porque el ultimo del txt tiene "\n" y lo estamos obteniendo
            actores = directores_guionistas_actores[2][:-1].split(",")
            diccionario[nombre_pelicula] = [directores, guionistas, actores]
        return peliculas,diccionario

