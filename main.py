from fastapi import Depends, FastAPI, HTTPException
from passlib.context import CryptContext

# from datetime import datetime, timedelta
# from jose import JWTError, jwt
from py2neo import Node, NodeMatcher
from pydantic import BaseModel

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

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# SECRET_KEY = SECRET_KEY
# ALGORITHM = ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES


# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


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


class User(BaseModel):
    name: str
    password: str
    username: str


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


@app.get("/get_user/")
def get_user(name: str, password: str):
    node_matcher = NodeMatcher(init_graph())
    person = node_matcher.match("Person", name=name).first()
    if person:
        p_password = person["password"]
        verify = verify_password(password, p_password)
        if verify:
            return name
        raise HTTPException(status_code=400, detail="password is not matching")
    raise HTTPException(status_code=404, detail="not found")
