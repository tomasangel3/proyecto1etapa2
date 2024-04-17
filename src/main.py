from typing import List, Optional
from fastapi import FastAPI
from joblib import load
import pandas as pd
import uvicorn
import DataModel as dm
from typing import List
from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from joblib import load
import pandas as pd
import uvicorn
import DataModel as dm

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")



data=[]

@app.post("/reviews")
async def create_review(reviews: List[dm.DataModel]):
   # guardar reviews en una variable
   for review in reviews:
      data.append(review.dict())
   return {"file": "successfully uploaded"}

@app.get("/show/reviews", response_class=HTMLResponse)
async def get_reviews(request: Request):
   return templates.TemplateResponse(
      request=request, name="reviews.html", context={"data": data}
   )

@app.get("/predict")
def make_predictions():
    df = pd.DataFrame(data, columns=['Review'])
    #for review in data :
    #    print(review)
    #    df = df.append({'Review':review}, ignore_index=True)
    #model = load("../data/modelo.joblib")
    #result = model.predict(df)
    return df

if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000)

