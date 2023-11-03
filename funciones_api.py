# Importaciones
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Datos a usar desde los archivos Parquet
max_playtime_by_genre_year = pd.read_parquet('Datasets/max_playtime_by_genre_year.parquet')
max_playtime_per_genre = pd.read_parquet('Datasets/max_playtime_per_genre.parquet')
summary_playtime_per_year = pd.read_parquet('Datasets/summary_playtime_per_year.parquet')
top3_recomendados = pd.read_parquet('Datasets/top3_recomendados.parquet')
top3_no_recomendados = pd.read_parquet('Datasets/top3_no_recomendados.parquet')
conteo_sentimientos = pd.read_parquet('Datasets/conteo_sentimientos.parquet')
# Cargar datos para el sistema de recomendacion
df_modelo = pd.read_parquet('../Datasets/recomendacion.parquet')
item_vectors  = pd.read_parquet('../Datasets/item_vectors.parquet')
unique_item_ids  = pd.read_parquet('../Datasets/unique_item_ids.parquet')
user_vectors  = pd.read_parquet('../Datasets/user_vectors.parquet')


def presentacion():
    '''
    Genera una página de presentación HTML para la API Steam de consultas de videojuegos.
    
    Returns:
    str: Código HTML que muestra la página de presentación.
    '''
    return '''
    <html>
        <head>
            <title>API Videojuegos</title>
            <meta charset="UTF-8">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #333;
                    color: #fff;
                }
                h1 {
                    color: #eee;
                    text-align: center;
                }
                p {
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
                a {
                    color: #66b3ff; /* Cambiar el color del enlace */
                }
                a:hover {
                    color: #4da6ff; /* Cambiar el color al pasar el ratón sobre el enlace */
                }
                span {
                    background-color: #666; /* Cambiar el color de fondo del span */
                    padding: 2px 5px;
                }
            </style>
        </head>
        <body>
            <h1>¡Bienvenido a la API de consultas sobre videojuegos de Steam!</h1>
            <p>Explora y descubre el mundo de los videojuegos de Steam a través de nuestra plataforma de consultas</p>
            <p>INSTRUCCIONES:</p>
            <p>Para interactuar con la API haz click <a href="https://mlops-videogames.onrender.com/docs">Aquí:</a></p>
            <p> Visita mi perfil en <a href="https://www.linkedin.com/in/edwintorre/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin"></a></p>
            <p> Los detalles de desarrollo de este proyecto están disponibles en <a href="https://github.com/edwinpro/MLOps_videogames"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
        </body>
    </html>
    '''

def PlayTimeGenre(genero: str):
    # La función PlayTimeGenre tiene por parametro 'genero', filtrará los datos por el género proporcionado
    # y calculará el año con más horas jugadas para ese género.

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
    if anio not in top3_recomendados['year'].unique():
        return f"No hay datos disponibles para el año {anio}"

    # Filtrar el DataFrame top3_recomendados para el año proporcionado
    top_games_year = top3_recomendados[top3_recomendados['year'] == anio]

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

def UsersNotRecommend(anio):
    # Verificar si el año proporcionado tiene datos en el DataFrame top3_no_recomendados
    if anio not in top3_no_recomendados['year'].unique():
        return f"No hay datos disponibles para el año {anio}"

    # Filtrar el DataFrame top3_no_recomendados para el año proporcionado
    top_games_year = top3_no_recomendados[top3_no_recomendados['year'] == anio]

    # Verificar si hay menos de 3 juegos para el año consultado
    if len(top_games_year) < 1:
        return "No hay suficientes juegos para mostrar el top 3 menos recomendados"

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


def sentiment_analysis(año):
    # Filtrar el DataFrame por el año dado
    df_filtrado = conteo_sentimientos[conteo_sentimientos['release_year'] == año]
    
    if df_filtrado.empty:
        return f"No hay datos disponibles para el año {año}"
    
    # Obtener la suma de cada sentimiento para el año dado
    sentimientos_totales = df_filtrado[['Negativo', 'Neutral', 'Positivo']].sum()
    
    # Convertir el resultado en un diccionario con valores enteros
    resultado = sentimientos_totales.astype(int).to_dict()
    
    return resultado

def recomendacion_juego(input_game):
    # Encontrar el vector de ítem correspondiente para el juego de entrada
    input_game_vector = item_vectors.loc[input_game].values.reshape(1, -1)
    
    # Calcular la similitud del coseno entre el vector del juego de entrada y todos los demás vectores de ítems
    similarities = cosine_similarity(input_game_vector, item_vectors.values)
    
    # Ordenar los puntajes de similitud del coseno en orden descendente
    similar_games_indices = similarities.argsort()[0][::-1]
    similar_games_indices = similar_games_indices[1:]  # Excluir el primer índice (el juego de entrada)
    
    # Seleccionar los mejores N juegos con los puntajes de similitud del coseno más altos como juegos recomendados
    recommended_game_ids = item_vectors.index[similar_games_indices][:5]
    
    # Obtener los nombres de los juegos recomendados, considerando solo un registro por 'item_id'
    recommended_games = unique_item_ids[unique_item_ids['item_id'].isin(recommended_game_ids)]['item_name'].tolist()
    
    return recommended_games

def recomendacion_usuario(input_user: str):
    input_user = str(input_user)

    vector_usuario = user_vectors.loc[input_user].values.reshape(1, -1)
    similarities = cosine_similarity(vector_usuario, user_vectors.values)

    similar_users_indices = similarities.argsort()[0][::-1]
    top_similar_users = user_vectors.index[similar_users_indices][:5]

    recommended_games = []
    for user in top_similar_users:
        games = df_modelo.loc[df_modelo['user_id'] == user, 'item_id'].tolist()
        recommended_games.extend(games)

    recommended_games = list(set(recommended_games))
    recommended_games.sort(key=lambda x: user_vectors.loc[top_similar_users, x].mean(), reverse=True)
    recommended_games = recommended_games[:5]

    #juegos_recomendados_nombres = [id_name_map[item_id] for item_id in recommended_games]
    juegos_recomendados_nombres = unique_item_ids[unique_item_ids['item_id'].isin(recommended_games)]['item_name'].tolist()
    
    return juegos_recomendados_nombres