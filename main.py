from typing import Optional
import DataModel
import pandas as pd
from fastapi import FastAPI
from joblib import load

app = FastAPI()


@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    model = load("'/Users/tomasangel/Documents/GitHub/proyecto1etapa2/data/modelo.joblib'")
    result = model.predict(df)
    return result
