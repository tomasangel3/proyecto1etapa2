from typing import List, Optional
from fastapi import FastAPI
from joblib import load
import pandas as pd
import uvicorn
import DataModel as dm
from typing import List
from fastapi import FastAPI
from joblib import load
import pandas as pd
import uvicorn
import DataModel as dm

app = FastAPI()

data=[]

@app.post("/reviews")
async def create_review(reviews: List[dm.DataModel]):
   # guardar reviews en una variable
   for review in reviews:
      data.append(review.dict())
   return {"file": "successfully uploaded"}

@app.get("/show/reviews")
async def get_reviews():
   return data

@app.get("/predict")
def make_predictions():
    df = pd.DataFrame(data, columns=('Review'), index=[0])
    df.columns = ('Review')
    model = load("modelo.joblib")
    result = model.predict(df)
    return result

if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000)

