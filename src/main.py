from typing import List, Optional
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from matplotlib import pyplot as plt
from collections import Counter
import nltk
from nltk.corpus import stopwords
import Processing
import re
import io
import joblib
import seaborn as sns
import pandas as pd
import uvicorn
import DataModel as dm

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

data=[]
list_predictions = []
comun = None

@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    data.extend(df.to_dict('records'))
    return templates.TemplateResponse(
      request=request, name="subirdocumento.html", context={"data": data})

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/show/reviews", response_class=HTMLResponse)
async def get_reviews(request: Request):
   return templates.TemplateResponse(
      request=request, name="reviews.html", context={"data": data})

@app.get("/predict", response_class=HTMLResponse)
async def make_predictions(request: Request):

    nltk.download('stopwords')
    stop_words = set(stopwords.words('spanish'))
    nltk.download('punkt')
    nltk.download('vader_lexicon')

    df = pd.DataFrame(data, columns=['Review'])

    # Cargamos nuestro Pipeline de jupyter 
    model = joblib.load("../data/modelo.joblib")
    predict = model.predict(df['Review'])

    # Guardamos la prediccion realizada en una lista de diccionarios para imprimirla 
    for text, prediction in zip(df['Review'], predict):
        list_predictions.append({"text": text, "prediction": prediction})

    # Plopteamos 
    df_resultados = pd.DataFrame(list_predictions)
    generar_plots(df_resultados)

    # Palabras comunes 
    palabras_comunes(df_resultados)
    df_resultados['Conteo'] = df_resultados['Palabras'].apply(lambda x: Counter(x))
    # Para cada lista, encontramos la palabra más común y su conteo
    df_resultados['Palabra_mas_comun'] = df_resultados['Conteo'].apply(lambda x: x.most_common(1)[0] if x else None)
    grupos = df_resultados.groupby('prediction')['Palabras'].sum()
    global comun
    comun = {prediction: Counter(grupo).most_common(20) for prediction, grupo in grupos.items()}

    return templates.TemplateResponse(
      request=request, name="prediccion.html", context={"predict": list_predictions})

@app.get("/tablero", response_class=HTMLResponse)
def obtener_tablero(request: Request):
    # sacamos las palabras mas comunes para cada clasificacion
    print(comun)
    # haz una tabla  por cada llave
    
    return templates.TemplateResponse('tablero.html', {'request': request})

def generar_plots(df_resultados):
    # Plot de barras de la cantidad de reseñas por calificación
    dx = sns.countplot(x="prediction", data=df_resultados)
    fig = dx.get_figure()
    fig.savefig("../static/barplot.png")
    plt.clf()  
    # Plot de distribución de predicciones
    cx = sns.histplot(df_resultados['prediction'])
    fig = cx.get_figure()
    fig.savefig("../static/histplot.png")
    plt.clf()
    # Plot de diagrama de caja por calificación
    df_resultados['prediction'] = df_resultados['prediction'].astype(int)  # Convierte las predicciones a int para el boxplot
    df_resultados['review_length'] = df_resultados['text'].apply(len)
    bx = sns.boxplot(x="prediction", y="review_length", data=df_resultados)
    fig = bx.get_figure()
    fig.savefig("../static/boxplot.png")
    plt.clf()  
    # Plot de dispersión de la longitud de la reseña vs. calificación
    df_resultados['review_length'] = df_resultados['text'].apply(len)
    ex = sns.scatterplot(x="review_length", y="prediction", data=df_resultados)
    fig = ex.get_figure()
    fig.savefig("../static/scatterplot.png")
    plt.clf()  

def palabras_comunes(df_resultados):
    Processing.limpiar(df_resultados)

if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000)
