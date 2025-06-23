---PROYECTO FINAL DE PROGRAMACIÓN: ANALIZADOR DE DISCOGRAFÍA---

Explicación del proyecto:

El proyecto desarrolla una aplicación web capaz de almacenar y analizar datos de distintas bandas musicales.
    Guarda información de bandas (nombre, género, año de formación, país)
    Registra álbumes (título, año de lanzamiento, duración, categoría)
    Almacena canciones (título, duración, número de pista)

El programa almacena los datos en la carpeta 'data' en archivos CSV separados que contienen la información de las bandas, albumes y canciones.
La estructura es:
    bandas:
	id: Identificador único (clave primaria)
        nombre: Nombre de la banda (único)
        genero: Género musical principal
        año_formacion: Año en que se formó la banda
        pais: País de origen
    albumes:
        id: Identificador único (clave primaria)
        banda_id: ID de la banda (clave foránea)
        titulo: Título del álbum
        año: Año de lanzamiento
        duracion_total: Duración total en minutos
        categoría: Sencillo, album, mini album o album recopilatorio
    canciones:
        id: Identificador único (clave primaria)
        album_id: ID del álbum (clave foránea)
        titulo: Título de la canción
        duracion: Duración en segundos
        track_number: Número de pista en el álbum

También puede:
    Exportar todos los datos a un Excel
    Importar datos desde un archivo Excel subido

Análisis a realizar:
    Gráficos de lanzamiento de álbumes por año
    Distribución de duración de álbumes y canciones
    Proporción de géneros musicales



