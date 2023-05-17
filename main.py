from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from datetime import datetime, timedelta
from jose import JWTError, jwt
from py2neo import Node, NodeMatcher
from pydantic import BaseModel
import os
from typing import Union, Any

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from graph import create_person_node, init_graph, matching_person_node

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# class Data(BaseModel):
#     name: str
#     username: str
#     password: str

# class User(BaseModel):
#     username:str
#     password:str

# class UserInDB(BaseModel):
#     hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# def get_user(propreties):
#     # matching=NodeMatcher(init_graph)
#     # print(matching)
#     # exist=matching.match("Person").first()
#     # match=matching_person_node.match("Person",username ="vds").first()
#     matching_node=NodeMatcher(init_graph)
#     exist=matching_node.match("Person",username="vds").all()
#     breakpoint()
#     if not exist:
#         return False
#         # raise HTTPException(status_code=status.HTTP_NOT_FOUND, details="user not exists")
#     return exist

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# SECRET_KEY = SECRET_KEY
# ALGORITHM = ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES


# # def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],propreties):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         username: str = payload.get("sub")
# #         if username is None:
# #             raise credentials_exception
# #     except JWTError:
# #         raise credentials_exception
# #     user = get_user(propreties)
# #     if user is None:
# #         raise credentials_exception
# #     return user

# @app.post("/user", tags=["users"])
# def add_user(data: Data):
#     password=get_password_hash(data.password)
#     propreties=Data(name=data.name,password=password,username=data.username)
#     node = create_person_node(label="Person", propreties=propreties)
#     g = init_graph()
#     g.create(node)
#     return data.name


# @app.post("/login")
# def login(data:User):
#     user=get_user(data)
#     if user:
#         pas=verify_password(data.password,user.pasword)
#         if not pas:
#             raise HTTPException(details="password missmatch")
#         return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    name: str
    password: str
    username: str


class TokenData(BaseModel):
    username: str
    password: str


@app.post("/create_user/")
def create_user(data: User):
    name = data.name
    username = data.username
    password = data.password
    hashed_pass = get_password_hash(password)
    g = init_graph()
    node_data = Node("Person", name=name, password=hashed_pass, username=username)
    g.create(node_data)
    return data.name


@app.post("/login_dfa/")
def get_user(name: str, password: str):
    node_matcher = NodeMatcher(init_graph())
    person = node_matcher.match("Person", name=name).first()
    if person:
        p_password = person["password"]
        verify = verify_password(password, p_password)
        if verify:
            return name
        raise HTTPException(status_code=400, detail="password is not matching..")
    raise HTTPException(status_code=404, detail="not found")


# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# @app.post(
#     "/login",
#     summary="Create access and refresh tokens for user",
#     response_model=TokenData,
# )
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):

#     node_matcher = NodeMatcher(init_graph())
#     person = node_matcher.match("Person", name=form_data.username).first()
#     if person:
#         p_password = person["password"]
#         verify = verify_password(form_data.password, p_password)
#         if verify:
#             pass
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Incorrect email or password",
#             )
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password",
#         )

#     return {
#         "access_token": create_access_token(person["username"]),
#         "refresh_token": create_refresh_token(person["username"]),
#     }


# def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(
#             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#         )

#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
#     return encoded_jwt


# def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(
#             minutes=REFRESH_TOKEN_EXPIRE_MINUTES
#         )

#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
#     return encoded_jwt
