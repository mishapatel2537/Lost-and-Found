from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Lost and Found API running"}