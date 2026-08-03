from fastapi import FastAPI, HTTPException
from pathlib import Path
import pandas as pd

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "all_forecasts.csv"

print("Loading CSV from:", CSV_PATH)

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