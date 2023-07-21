from fastapi import FastAPI, Cookie, HTTPException
from pydantic import BaseModel

from app.model.model import predict, convert

app = FastAPI()


class StockIn(BaseModel):
    ticker: str


class StockOut(StockIn):
    forecast: dict


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict", response_model=StockOut, status_code=200)
def get_prediction(payload: StockIn):
    ticker = payload.ticker

    prediction_list = predict(ticker)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"ticker": ticker, "forecast": convert(prediction_list)}
    return response_object
