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
                        3. Scrollear a "Resposes" para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación que realiza el usuario y cantidad de items que tiene el mismo.
                        </font>
                        """,
         tags=["Consultas Generales"])
def PlayTimeGenre(genero: str = Query(..., 
                                description="Genero de videojuego", 
                                examples="EchoXSilence")):
        
    genre_result = fa.PlayTimeGenre(genero)
    # Convertir el resultado a formato JSON
    json_result = json.dumps(genre_result, ensure_ascii=False)
    return json_result
