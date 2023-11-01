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

    # genre_result = fa.PlayTimeGenre('rpg')
    # # Convertir el resultado a formato JSON
    # json_result = json.dumps(genre_result, ensure_ascii=False)
    # print(json_result)
