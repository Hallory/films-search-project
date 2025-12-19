from fastapi import FastAPI

app = FastAPI(title="Film Search API")

@app.get("/health")
def health():
    return {"status": "ok"}
