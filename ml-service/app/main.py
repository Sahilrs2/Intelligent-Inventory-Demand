from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd


app = FastAPI()


# CORS Configuration
# Allows React frontend (Vite) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "all_forecasts.csv"


print("Loading CSV from:", CSV_PATH)


# Load forecast data
forecasts = pd.read_csv(CSV_PATH)


@app.get("/forecast/{store_id}/{item_id}")
def get_forecast(store_id: int, item_id: int):

    subset = forecasts[
        (forecasts["store"] == store_id) &
        (forecasts["item"] == item_id)
    ]


    if subset.empty:
        raise HTTPException(
            status_code=404,
            detail="No forecast found for this store/item"
        )


    return subset[["ds", "yhat"]].rename(
        columns={
            "ds": "date",
            "yhat": "predicted_demand"
        }
    ).to_dict(orient="records")