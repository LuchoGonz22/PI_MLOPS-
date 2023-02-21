import pandas as pd #Libreria para poder leer el DataFrame
from fastapi import FastAPI #API utilizada
from fastapi.responses import PlainTextResponse #Permite a los crear respuestas HTTP
from pandasql import sqldf # Utilizar pandas para consultas SQL

tags_metadata = [
    {
        "name": "Cantidad por plataforma",
        "description": "Cantidad de películas por plataforma con filtro de PLATAFORMA",
    },
    {
        "name": "Actor que más se repite",
        "description": "Devuelve el actor que más se repite según plataforma y año",
    },
    {
        "name": "Mayor duración",
        "description": "Película con mayor duración con filtros opcionales de año, plataforma y tipo de duración",
    },
    {
        "name": "Cantidad puntaje",
        "description": "Devuelve la cantidad de películas por plataforma con un puntaje mayor a XX en determinado año\
            ",
    },
]


app = FastAPI()

df = pd.read_csv(r"C:\Users\lucho\OneDrive\Documentos\MLOpsReviews\Datasets\movies_dF.csv", low_memory=False)

@app.get("/")
def main():
    return "Mi primera API"

pysqldf = lambda q: sqldf(q, globals())


#1 => Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. 
#     (la función debe llamarse get_max_duration(year, platform, duration_type))
@app.get("/max_duration/{year}/{platform}/{duration_type}",
    response_class=PlainTextResponse,
    tags=["Mayor duración"],
)
def get_max_duration(year, platform, duration_type):
    """
    Informa cual es la **película** con mayor duración en minutos o la **serie**
    con mas temporadas, de acuerdo al tipo de duración ingresado.
    Requiere ingresar el **año** en formato AAAA, el **tipo de duración** (min / season)
    y la **plataforma** (netflix, disney, hulu, amazon), todo en minúsculas
    """
    if platform == "amazon":
        plat = "a%"
    elif platform == "netflix":
        plat = "n%"
    elif platform == "hulu":
        plat = "h%"
    elif platform == "disney":
        plat = "d%"
    else:
        return "No ha seleccionado la plataforma entre las opciones posibles"

    query = (
        """SELECT title
        FROM df
        WHERE id LIKE '"""
        + plat
        + """'
        AND release_year = '"""
        + year
        + """'
        AND duration_type = '"""
        + duration_type
        + """'
        AND duration_int = (SELECT MAX(duration_int)
        FROM df
        WHERE id LIKE '"""
        + plat
        + """'
        AND release_year = '"""
        + year
        + """'
        AND duration_type = '"""
        + duration_type
        + """')
        """
    )

    q = pysqldf(query)
    return q.to_string(index=False, header=False)



#2=> Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año
#   (la función debe llamarse get_score_count(platform, scored, year))

@app.get('/get_score_count/{platform}/{score}/{year}',
    response_class=PlainTextResponse,
    tags=["Cantidad puntaje"],
)
def get_score_count(platform, scored, year):
    """
    Cuenta cantidad de **películas** que superan el score indicado para cierto año y plataforma.
    Requiere el ingreso del **año** en formato AAAA, el **score** como un entero del 0 a 99
    y la **plataforma** (netflix, disney, hulu, amazon)
    """
    if platform == "amazon":
        plat = "a%"
    elif platform == "netflix":
        plat = "n%"
    elif platform == "hulu":
        plat = "h%"
    elif platform == "disney":
        plat = "d%"
    else:
        return "No ha seleccionado la plataforma entre las opciones posibles"

    query = (
        """SELECT COUNT(title)
        FROM df
        WHERE avg_r > """
        + scored
        + """
        AND release_year = """
        + year
        + """
        AND id LIKE '"""
        + plat
        + """'
        AND type = 'movie'"""
    )
    cantidad = pysqldf(query)
    return cantidad.to_string(index=False, header=False)

#3 => Cantidad de películas por plataforma con filtro de PLATAFORMA.
#    (La función debe llamarse get_count_platform(platform))

@app.get("/get_count_platform/{platform}",
    response_class=PlainTextResponse,
    tags=["Cantidad por plataforma"]
)
def get_count_platform(platform: str):
    """
    Devuelve la cantidad de películas en una plataforma de transmisión específica.
    Requiere ingresar la plataforma (netflix, disney, hulu, amazon) en minúsculas.
    """
    if platform == "amazon":
        plat = "a%"
    elif platform == "netflix":
        plat = "n%"
    elif platform == "hulu":
        plat = "h%"
    elif platform == "disney":
        plat = "d%"
    else:
        return "No ha seleccionado la plataforma entre las opciones posibles"

    query = (
        """SELECT COUNT(*)
        FROM df
        WHERE id LIKE '"""
        + plat
        + """'
        AND type = 'movie'"""
    )
    result = pysqldf(query)
    count = result.iloc[0, 0]
    return str(count)


#4 => Actor que más se repite según plataforma y año. 
# (La función debe llamarse get_actor(platform, year))
@app.get("/get_actor/{platform}/{year}",
    response_class=PlainTextResponse,
    tags=["Actor que más se repite"],
)
def get_actor(platform, year):
    """
    Devuelve el actor que más aparece en películas de una plataforma de transmisión en un año específico.
    Requiere ingresar la plataforma (netflix, disney, hulu, amazon) en minúsculas y el año (por ejemplo, 2022).
    """
    if platform == "amazon":
        plat = "a%"
    elif platform == "netflix":
        plat = "n%"
    elif platform == "hulu":
        plat = "h%"
    elif platform == "disney":
        plat = "d%"
    else:
        return "No ha seleccionado la plataforma entre las opciones posibles"

    query = (
        """SELECT cast, COUNT(*) as count
        FROM df
        WHERE id LIKE '"""
        + plat
        + """'
        AND type = 'movie'
        AND year = """
        + year
        + """
        GROUP BY cast
        ORDER BY count DESC
        LIMIT 1"""
    )
    result = pysqldf(query)
    return result .to_string(index=False, header=False)

    # actor = result.iloc[0, 0]
    # return actor
