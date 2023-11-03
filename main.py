from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import funciones_api as fa

import importlib
importlib.reload(fa)

# Se instancia la aplicación
app = FastAPI()

# Funciones
@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])
def home():

    '''
    Página de inicio que muestra una presentación.

    Returns:
    HTMLResponse: Respuesta HTML que muestra la presentación.
    '''
    return fa.presentacion()

@app.get(path = '/playtimegenre',
          description = """ <font color="blue">
                        Año con más horas jugadas<br>
                        Devuelve año con mas horas jugadas para dicho género.
                        </font>
                        """,
         tags=["Consultas"])
def PlayTimeGenre(genero: str = Query(..., 
                                description="Genero de videojuego", 
                                examples="Action")):
        
    return fa.PlayTimeGenre(genero)

@app.get(path = '/userforgenre',
          description = """ <font color="blue">
                        Usuario con más horas jugadas<br>
                        Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
                        </font>
                        """,
         tags=["Consultas"])
def UserForGenre(genero: str = Query(..., 
                                description="Genero de videojuego", 
                                examples="Indie")):
    return fa.UserForGenre(genero)

@app.get(path = '/usersrecommend',
          description = """ <font color="blue">
                        MAS recomendados<br>
                        Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
                        </font>
                        """,
         tags=["Consultas"])
def UsersRecommend(anio: int = Query(..., 
                                description="Año a consultar.", 
                                examples="2015")):
    return fa.UsersRecommend(anio)


@app.get(path = '/usersnotrecommend',
          description = """ <font color="blue">
                        MENOS recomendados<br>
                        Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
                        </font>
                        """,
         tags=["Consultas"])
def UsersNotRecommend(anio: int = Query(..., 
                                description="Año a consultar.", 
                                examples="2015")):
    return fa.UsersNotRecommend(anio)

@app.get(path = '/sentimentanalysis',
          description = """ <font color="blue">
                        Reseñas de usuarios<br>
                        Devuelve una lista con la cantidad de reseñas de usuarios que se encuentren categorizados.
                        </font>
                        """,
         tags=["Consultas"])
def sentiment_analysis(anio: int = Query(..., 
                                description="Año para obtener conteo de reseñas", 
                                examples="2015")):
    return fa.sentiment_analysis(anio)


@app.get(path = '/recomendacionjuego',
          description = """ <font color="blue">
                        Recomendación item-item<br>
                        Ingresando el id de juego, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
                        </font>
                        """,
         tags=["Recomendaciones"])
def recomendacion_juego(input_game: int = Query(..., 
                                description="ID de juego", 
                                examples="209650")):
    return fa.recomendacion_juego(input_game)