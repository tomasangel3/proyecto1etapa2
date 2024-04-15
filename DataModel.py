"""
from pydantic import BaseModel

class DataModel(BaseModel):

# Estas varibles permiten que la librería pydantic haga el parseo entre el Json recibido y el modelo declarado.
    Review: str

#Esta función retorna los nombres de las columnas correspondientes con el modelo esxportado en joblib.
    def columns(self):
        return ["Review"]

"""
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

class DataModel(BaseModel):
    Review: str

@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    model = load("data\modelo.joblib")
    result = model.predict(df)
    return {"predictions": result.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
