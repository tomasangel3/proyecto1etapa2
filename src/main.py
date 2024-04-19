from typing import List, Optional
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from joblib import load
import io
import joblib
import pandas as pd
import uvicorn
import DataModel as dm

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

data=[]

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
def make_predictions(request: Request):
    list_predictions = []
    df = pd.DataFrame(data, columns=['Review'])
    model = joblib.load("../data/modelo.joblib")
    predict = model.predict(df['Review'])
    for text, prediction in zip(df['Review'], predict):
        list_predictions.append({"text": text, "prediction": prediction})
    df_resultados = pd.DataFrame(list_predictions)
    return templates.TemplateResponse(
      request=request, name="prediccion.html", context={"predict": list_predictions})



if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000)

