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

data={}

@app.post("/reviews")
async def create_review(reviews: List[dm.DataModel]):
   # guardar reviews en una variable
   for review in reviews:
      data[review.Review] = review.Review
   return {"file": "successfully uploaded"}

@app.get("/show/reviews")
async def get_reviews():
   return data

@app.post("/predict")
def make_predictions():
   data = dm.DataModel()
   df = pd.DataFrame(data, columns=data.keys(), index=[0])
   df.columns = dm.columns()
   model = load("assets/modelo.joblib")
   result = model.predict(df)
   return result

if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000)

