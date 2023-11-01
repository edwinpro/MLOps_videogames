# Importaciones
import pandas as pd
import json

# Datos a usar desde los archivos Parquet
max_playtime_by_genre_year = pd.read_parquet('Datasets/max_playtime_by_genre_year.parquet')
max_playtime_per_genre = pd.read_parquet('Datasets/max_playtime_per_genre.parquet')
summary_playtime_per_year = pd.read_parquet('Datasets/summary_playtime_per_year.parquet')
top3_recomendados = pd.read_parquet('Datasets/top3_recomendados.parquet')

def presentacion():
    '''
    Genera una página de presentación HTML para la API Steam de consultas de videojuegos.
    
    Returns:
    str: Código HTML que muestra la página de presentación.
    '''
    return '''
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas de videojuegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam donde se pueden hacer diferentes consultas sobre la plataforma de videojuegos.</p>
            <p>INSTRUCCIONES:</p>
            <p>Escriba <span style="background-color: lightgray;">/docs</span> a continuación de la URL actual de esta página para interactuar con la API</p>
            <p> Visita mi perfil en <a href="https://www.linkedin.com/in/ingambcarlapezzone/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin"></a></p>
            <p> El desarrollo de este proyecto esta en <a href="https://github.com/IngCarlaPezzone/PI1_MLOps_videojuegos"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
        </body>
    </html>
    '''

def PlayTimeGenre(genero: str):
    # La función PlayTimeGenre tiene por parametro 'genero', filtrará los datos por el género proporcionado
    # y calculará el año con más horas jugadas para ese género..

    # Convertir el género a minúsculas para hacer la comparación sin ser sensible a mayúsculas
    genero = genero.lower()

    # Verificar si el género está presente en el DataFrame
    if genero not in max_playtime_by_genre_year['genres'].str.lower().unique():
        return {"Error": f"El género '{genero}' no se encuentra en el conjunto de datos."}

    # Filtrar el DataFrame por el género proporcionado
    genre_data = max_playtime_by_genre_year[max_playtime_by_genre_year['genres'].str.lower() == genero]

    # Obtener el año con más horas jugadas para el género dado
    max_playtime_year = genre_data['release_year'].values[0] if not genre_data.empty else None

    # Crear el diccionario para el formato JSON
    result = {f'Año de lanzamiento con más horas jugadas para {genero.capitalize()}': str(max_playtime_year)}

    return result


def UserForGenre(genre: str):
    # Esta función tiene por parametro 'genero', debe devolver el usuario que acumula más horas jugadas 
    # para el género dado y una lista de la acumulación de horas jugadas por año.

    genre = genre.lower()  # Convertir el género a minúsculas para ser insensible a mayúsculas/minúsculas

    # Filtrar por el género deseado en el dataframe max_playtime_per_genre
    genre_data = max_playtime_per_genre[max_playtime_per_genre['genres'].str.lower() == genre]

    if len(genre_data) == 0:
        return "Género no encontrado"

    # Obtener el usuario con más horas jugadas para el género dado
    max_playtime_user = genre_data.loc[genre_data['playtime_forever'].idxmax()]['user_id']

    # Filtrar por el género deseado en el dataframe summary_playtime_per_year
    genre_year_data = summary_playtime_per_year[summary_playtime_per_year['user_id'].isin(genre_data['user_id'])]

    # Agrupar y sumar las horas jugadas por año, excluyendo los años con 0 horas jugadas
    yearly_hours = genre_year_data.groupby('release_year')['playtime_total_hours'].sum().reset_index()
    yearly_hours = yearly_hours[yearly_hours['playtime_total_hours'] > 1]

    # Crear un diccionario con el formato solicitado
    hours_by_year = [
        {'Año': int(year), 'Horas': int(hours)}
        for year, hours in zip(yearly_hours['release_year'], yearly_hours['playtime_total_hours'])
    ]

    # Formato de salida en JSON
    output = {
        f'Usuario con más horas jugadas para Género {genre.capitalize()}': max_playtime_user,
        'Horas jugadas': hours_by_year
    }

    return output

def UsersRecommend(anio):
    # Verificar si el año proporcionado tiene datos en el DataFrame top3_recomendados
    if anio not in top3_recomendados['release_year'].unique():
        return f"No hay datos disponibles para el año {anio}"

    # Filtrar el DataFrame top3_recomendados para el año proporcionado
    top_games_year = top3_recomendados[top3_recomendados['release_year'] == anio]

    # Verificar si hay menos de 3 juegos para el año consultado
    if len(top_games_year) < 1:
        return "No hay suficientes juegos para mostrar el top 3"

    # Reiniciar el índice del DataFrame filtrado por año
    top_games_year = top_games_year.reset_index(drop=True)

    # Obtener el top 3 de juegos más recomendados para el año dado
    top_3_games = top_games_year.head(3)

    # Crear una lista con el formato especificado
    top_3_list = []
    for index, row in top_3_games.iterrows():
        game_rank = index + 1  # Usar el índice + 1 como número de puesto
        game_dict = {"Puesto " + str(game_rank): row['title']}
        top_3_list.append(game_dict)

    return top_3_list    


