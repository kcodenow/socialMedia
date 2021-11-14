from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome!!"}

@app.get("/posts")
def get_posts():
    return {"data": ["Posts1", "Post2"]}