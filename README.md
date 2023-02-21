# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

## Contexto

El ciclo de vida de un proyecto de Machine Learning debe contemplar desde el tratamiento y recolección de los datos (Data Engineer) hasta el entrenamiento y mantenimiento del modelo de ML según llegan nuevos datos.

Empecé a trabajar como Data Scientist en una start-up que provee servicios de agregación de plataformas de streaming. Cree un sistema de recomendación de ML para solucionar un problema del del negocio.

Como los datos están sin transformar, se realiza un rápido trabajo de Data Engineer para tener un MVP (Minimum Viable Product).

<br/>

## **ETAPAS DEL PROCESO**

## Proceso de ETL

El proyecto consiste en realizar una ingesta de datos, posteriormente realizar un ETL, y luego disponibilizar los datos limpios para su consulta a través de una API construida en un entorno virtual.

+ Se generó el campo **`id`**: Cada id se compuso de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)

+ Los valores nulos del campo rating se reemplazaron por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

+ Las fechas se conviertieron a formato **`AAAA-mm-dd`**

+ Los campos de texto se pasaron a **minúsculas**

+ El campo ***duration*** se convirtió en dos campos: **`duration_int`** y **`duration_type`**. El primero se transformó en integer y el segundo a string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

<br/>
* **ratings** - CSV de ratings de las peliculas
* **Datasets** - Archivos necesarios para la API
* **etl.ipynb** - Proceso de ETL
* **main.py** - Codigo para la API
* **requirements.txt** - Dependencias usadas
* **EDA_process.ipynb** - Transformacion de datos para el modelo
* **ML_recomendatio.ipynb** - Sistema de recomendacion de peliculas
