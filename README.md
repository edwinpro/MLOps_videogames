![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)

# Proyecto MLOPs: Sistema de Recomendación VideoJuegos

## Introducción

El desafío del presente proyecto implica desempeñar el rol combinado de un ingeniero MLOps, que une las funciones de un ingeniero de datos y un científico de datos, para la famosa plataforma de juegos, Steam. El objetivo es crear un Producto Mínimo Viable que incluya una API desplegada en la nube y la implementación de dos modelos de Machine Learning. Estos modelos tienen la tarea de realizar un análisis de sentimientos sobre las opiniones de los usuarios en los juegos, además de recomendar juegos basados en el nombre de un juego específico o en las preferencias de un usuario en particular.

## Contexto

En el ámbito de la industria de los videojuegos, Steam, la plataforma de distribución digital creada por Valve Corporation en 2003, ha sido un protagonista destacado con más de 120 millones de usuarios mensuales y un catálogo de más de 50,000 juegos. Sin embargo, desde 2018, la disponibilidad de datos precisos se ha visto limitada debido a cambios en la política de privacidad de Steam, lo que ha dificultado la recopilación actualizada de estadísticas. A pesar de estas restricciones, Steam sigue siendo un pilar fundamental en la distribución de juegos, proporcionando una amplia gama de títulos tanto para estudios establecidos como para desarrolladores independientes. Esta limitación en la disponibilidad de datos se convierte en un desafío para proyectos de análisis o implementación de Machine Learning, ya que la obtención de información actualizada sobre la plataforma se ha vuelto más complicada desde entonces.

## Datos

Para este proyecto se proporcionaron tres archivos JSON:

- **output_steam_games.json** Se trata de un conjunto de datos que incluye información sobre los videojuegos, como sus nombres, creadores, costos, especificaciones técnicas, etiquetas y otros detalles asociados.

- **australian_user_reviews.json** Se trata de un conjunto de datos que incluye opiniones de usuarios acerca de los videojuegos que juegan, junto con información extra, como la recomendación del juego, emoticones usados para expresar humor, y estadísticas sobre la utilidad de los comentarios para otros. Además, muestra la identificación del usuario que comenta con su enlace al perfil y la identificación del juego comentado.

- **australian_users_items.json** Este conjunto de datos alberga detalles acerca de los juegos que cada usuario ha jugado, junto con la cantidad total de tiempo que han dedicado a un juego específico.

En el documento [Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link) se encuetran los detalles de cada una de las variables de los conjuntos de datos.

## Tareas desarrolladas

### Transformaciones

Los datos fueron sometidos a un proceso ETL, abarcando tres conjuntos de datos distintos. Dos de estos conjuntos estaban estructurados de manera anidada, con columnas que contenían diccionarios o listas de estos, lo que requirió la implementación de diversas estrategias para convertir las claves de estos diccionarios en columnas separadas. Posteriormente, se llevó a cabo la imputación de valores nulos en variables esenciales para el proyecto. Asimismo, se eliminaron columnas con una alta presencia de valores nulos o con aportes insignificantes al proyecto, con el propósito de optimizar el rendimiento de la API, considerando las limitaciones de almacenamiento del despliegue. En estas transformaciones, se empleó la biblioteca Pandas.

Los detalles del ETL se puede ver en [ETL output_steam_games](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/ETL_steam_games.ipynb), [ETL australian_users_items](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/ETL_user_items.ipynb) y [ETL australian_user_reviews](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/ETL_user_reviews.ipynb).

### Feature engineering

Se nos solicitó incorporar un análisis de sentimientos a las revisiones de los usuarios en este proyecto. Para lograrlo, se introdujo una columna adicional denominada 'sentiment_analysis', sustituyendo la existente que almacenaba las revisiones, asignando una clasificación de sentimientos utilizando la siguiente escala:

- 0 si es malo,
- 1 si es neutral o esta sin review
- 2 si es positivo.

Con el propósito de validar un concepto, el proyecto emplea TextBlob, una librería de procesamiento de lenguaje natural en Python, para llevar a cabo un análisis de sentimientos básico. El enfoque radica en asignar valores numéricos a comentarios de usuarios sobre un juego específico, indicando si el sentimiento expresado es negativo, neutral o positivo.

La metodología se basa en evaluar el texto, determinar su polaridad mediante TextBlob y clasificar la revisión como negativa, neutral o positiva según esa polaridad. El modelo predefinido utiliza umbrales de -0.2 y 0.2 para clasificar como negativos por debajo de -0.2, positivos por encima de 0.2 y neutrales en el rango intermedio.

Por otro lado, para optimizar la velocidad de las consultas en la API y considerando las limitaciones de almacenamiento en la nube para la implementación de la API, se crearon dataframes auxiliares para cada función requerida. Estos dataframes se guardaron en formato _parquet_, permitiendo una compresión y codificación eficaz de los datos.

Todos los detalles del desarrollo se pueden ver en la Jupyter Notebook [Feature_Engineering](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/Feature_Engineering.ipynb).

### Análisis exploratorio de los datos (EDA)

Los tres conjuntos de datos tras el proceso ETL fueron analizados para identificar las variables aplicables en la creación del modelo de recomendación. Este análisis se efectuó empleando la librería Pandas para la manipulación de los datos, junto con Matplotlib y Seaborn para su visualización.

Específicamente para el modelo de recomendación, se optó por generar un marco de datos particular que incluye el ID de los usuarios que realizaron reseñas, los nombres de los juegos comentados y una columna de calificación creada a partir del análisis de sentimientos y las recomendaciones de juegos.

El desarrollo de este análisis se encuentra en la Jupyter Notebook [EDA](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/EDA.ipynb)

### Modelo de aprendizaje automático

Se desarrollaron dos enfoques de recomendación para sugerir 5 juegos, ya sea al ingresar el ID de un juego o el ID de un usuario.

En el primer método, se emplea un modelo que se basa en las similitudes entre los juegos, generando recomendaciones basadas en la similitud de cada juego con los demás. En el segundo enfoque, se utiliza un modelo que considera las preferencias de usuarios similares para recomendar juegos al usuario activo.

Estos modelos se construyeron utilizando algoritmos de memoria para abordar el filtrado colaborativo, analizando toda la base de datos en busca de usuarios con preferencias similares al usuario objetivo, utilizando sus gustos para predecir las preferencias del usuario activo.

Para calcular la similitud entre juegos (item_similarity) y entre usuarios (user_similarity), se aplicó el método de similitud del coseno. Esta técnica es común en sistemas de recomendación y análisis de datos, ya que evalúa cuán parecidos son dos conjuntos de datos o elementos basándose en el ángulo entre los vectores que los representan en un espacio multidimensional.

El desarrollo para la creación de los dos modelos se presenta en la Jupyter Notebook [Modelo](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/Modelo.ipynb).

### Desarrollo de API

Para el desarrolo de la API se decidió utilizar el framework FastAPI, creando las siguientes funciones:

- **PlayTimeGenre**: Esta función recibe como parametro 'genero', filtrará los datos por el género proporcionado y calculará el año con más horas jugadas para ese género.

- **UserForGenre**: Esta función recibe como parametro 'genero', devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

- **UsersRecommend**: Esta función recibe como parametro 'año', devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

- **UsersNotRecommend**: Esta función recibe como parametro 'año', devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.

- **sentiment_analysis**: Esta función recibe como parametro 'año', según el año de lanzamiento, devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

- **recomendacion_juego**: Esta función recibe como parámetro el Id de un juego y devuelve una lista con 5 juegos recomendados similares al ingresado.

- **recomendacion_usuario**: Esta función recibe como parámetro el Id de un usuario y devuelve una lista con 5 juegos recomendados para dicho usuario teniendo en cuenta las similitudes entre los usuarios.

> _NOTA: ambas funciones, recomendacion_juego y recomendacion_usuario se agregaron a la API, pero sólo recomendacion_juego se pudo deployar en Render dado que el conjunto de datos que requiere para hacer la predicción excedía la capacidad de almacenamiento disponible. Por lo tanto, para utilizarla se puede ejecutar la API en local._

El desarrollo de las funciones de consultas generales se puede ver en la Jupyter Notebook [FuncionesAPI](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/FuncionesAPI.ipynb). El desarrollo del código para las funciones del modelo de recomendación se puede ver en la Jupyter Notebook [Modelo](https://github.com/edwinpro/MLOps_videogames/blob/main/Notebooks/Modelo.ipynb)

El código para generar la API se encuentra en el archivo [main.py](https://github.com/edwinpro/MLOps_videogames/blob/main/main.py) y las funciones para su funcionamiento se encuentran en [funciones_api.py](https://github.com/edwinpro/MLOps_videogames/blob/main/funciones_api.py). En caso de querer ejecutar la API desde localHost se deben seguir los siguientes pasos:

- Clonar el proyecto haciendo `git clone https://github.com/edwinpro/MLOps_videogames.git`.
- Preparación del entorno de trabajo en Visual Studio Code:
  - Crear entorno `Python -m venv env`
  - Ingresar al entorno haciendo `venv\Scripts\activate`
  - Instalar dependencias con `pip install -r requirements.txt`
- Ejecutar el archivo main.py desde consola activando uvicorn. Para ello, hacer `uvicorn main:app --reload`
- Hacer Ctrl + clic sobre la dirección `http://XXX.X.X.X:XXXX` (se muestra en la consola).
- Una vez en el navegador, agregar `/docs` para acceder a ReDoc.
- En cada una de las funciones hacer clic en _Try it out_ y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.

### Deployment

Optamos por Render, una plataforma en la nube que unifica la creación y ejecución de aplicaciones y sitios web. Esta opción permite desplegar automáticamente desde GitHub. El proceso se llevó a cabo mediante los siguientes pasos:

- Se generó un servicio nuevo en `render.com`, conectado al presente repositorio.
- Finalmente, el servicio queda corriendo en [http://mlops-videogames.onrender.com/](http://mlops-videogames.onrender.com/).

### Video

En este [video](https://drive.google.com/file/d/1hDZFyNQf1fh4UJM16w-hA_94rX9Hi7Mz/view?usp=sharing) se explica brevemente este proyecto mostrando el funcionamiento de la API.

## Oportunidades de mejoras

El propósito inicial de este proyecto consistió en introducir un Producto Mínimo Viable. Durante esta fase, se llevaron a cabo análisis elementales, los cuales están sujetos a mejoras en futuros pasos con el fin de alcanzar un producto integral. Por ejemplo:

- **Análsis de sentimiento**: Es factible limpiar los comentarios que están en varios idiomas, con emoticones y signos de puntuación. También, es posible analizar cómo funciona el modelo al probar diferentes niveles de clasificación.

- **Modelos de recomendación**: Es factible desarrollar una clasificación que tenga en cuenta factores como el tiempo de juego de los usuarios, la utilidad de sus comentarios para otros, el coste de los juegos, y más. Además, se pueden analizar otras herramientas que creen estos modelos.

- **EDA más exhaustivo**: Es factible realizar un análisis detallado de los datos en busca de conexiones adicionales entre juegos y usuarios. Esto permitirá generar una puntuación más precisa que servirá de base para las recomendaciones.

- **ETL más exhaustivo**: Es posible realizar ajustes adicionales en ciertas variables de la API, como los precios. En algunos casos, se reemplazaron múltiples descripciones por "precio cero" debido a referencias a juegos gratuitos, sin un análisis exhaustivo. También se encontraron datos faltantes, que se reemplazaron por 0 sin verificar si correspondían a juegos gratuitos. Estos cambios pueden influir en los resultados de la API al calcular el porcentaje de juegos gratuitos.

- **Otros servicios de nube**: Explorar enfoques alternativos para implementar la API podría liberarnos de las restricciones de memoria RAM, permitiendo así aprovechar plenamente la última característica del modelo de recomendación. También podemos considerar opciones de almacenamiento independientes de Render y establecer conexiones para realizar consultas.
