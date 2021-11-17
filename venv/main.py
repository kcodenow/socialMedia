from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None

my_posts = [
            {"title": "title of post1", "content": "content of post1", "id": 1},
            {"title": "title of post2", "content": "content of post2", "id": 2}
            ]
            
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome!!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    return {"post_detail": post}

@app.post("/posts")
def create_posts(post: Post, status_code=status.HTTP_201_CREATED):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    ind = find_post_index(id)
    
    if(ind == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID={id} does not exist")
    my_posts.pop(ind)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
    ind = find_post_index(id)
    
    if(ind == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID={id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[ind] = post_dict
    return {"data": post_dict}