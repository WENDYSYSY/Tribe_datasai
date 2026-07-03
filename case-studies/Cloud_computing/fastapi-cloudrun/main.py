from fastapi import FastAPI
import os

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)