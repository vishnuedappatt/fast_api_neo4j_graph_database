from fastapi import FastAPI
from pydantic import BaseModel

from graph import create_node, init_graph

app = FastAPI(prefix="/api/")


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Data(BaseModel):
    name: str
    username: str
    password: str


@app.post("/user/", tags=["users"])
def add_user(data: Data):

    node = create_node(label="Person", propreties=data)
    g = init_graph()
    g.create(node)
