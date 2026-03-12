from fastapi import FastAPI, HTTPException
from inference_core import predict

app = FastAPI(title="SOHMA Model API", version="0.2")

@app.get("/")
def root():
    return {"ok": True, "service": "sohma_api"}

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/predict")
def predict_endpoint(payload: dict):
    try:
        return predict(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))