from fastapi import FastAPI
import os
import platform

app = FastAPI(
    title="DataSAI API",
    description="API déployée sur Google Cloud Run",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API DataSAI", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/predict/{value}")
def predict(value: float):
    result = value * 2.5 + 10
    return {
        "input": value,
        "prediction": round(result, 2),
        "model": "DataSAI v1.0"
    }
    
@app.get("/info")
def system_info():
    # Affiche les infos du système où tourne le container
    return {
        "python_version": platform.python_version(),
        "os": platform.system(),
    }