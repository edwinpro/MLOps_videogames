from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import json
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
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el genero a consultar.<br>
                        3. Scrollear a "Resposes" para ver el año con más horas jugadas para ese género.
                        </font>
                        """,
         tags=["Consultas"])
def PlayTimeGenre(genero: str = Query(..., 
                                description="Genero de videojuego", 
                                examples="EchoXSilence")):
        
    resultado = fa.PlayTimeGenre(genero)
    return json.dumps(resultado, ensure_ascii=False, indent=4)


@app.get(path = '/userforgenre',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el genero a consultar.<br>
                        3. Scrollear a "Resposes" para ver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
                        </font>
                        """,
         tags=["Consultas"])
def UserForGenre(genero: str = Query(..., 
                                description="Genero de videojuego", 
                                examples="EchoXSilence")):

    resultado = fa.UserForGenre(genero)
    return json.dumps(resultado, ensure_ascii=False, indent=4)

@app.get(path = '/usersrecommend',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el año a consultar.<br>
                        3. Scrollear a "Resposes" para ver el top 3 de juegos mas recomendado por año consultado.
                        </font>
                        """,
         tags=["Consultas"])
def UsersRecommend(anio: int = Query(..., 
                                description="Año para obtener top 3 videojuego", 
                                examples="EchoXSilence")):

    resultado = fa.UsersRecommend(anio)
    return json.dumps(resultado, ensure_ascii=False, indent=4)    
