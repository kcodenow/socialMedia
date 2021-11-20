from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
# uvicorn main:app --reload
# venv\Scripts\activate.bat

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(host='localhost', database='socialMedia',
                            user='postgres',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('\nSUCCESS - connected to DB\n')
except Exception as e:
    print(f'\nFATAL - did not connect to DB\n{e}')

@app.get("/")
def root():
    return {"message": "Welcome!!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    return {"post": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)RETURNING * """,
        (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID->{id} does not exist")
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",\
        (post.title, post.content, post.published, str(id)))
    
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID->{id} does not exist")
    return {"data": post}