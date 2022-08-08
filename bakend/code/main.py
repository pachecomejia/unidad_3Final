import os
import sqlite3
from typing import List
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Union
from typing import List
import hashlib
from fastapi.middleware.cors import CORSMiddleware
import pyrebase
from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib import response
from fastapi.responses import RedirectResponse





######################################################
DATABASE_URL = os.path.join("clientes.sqlite")#base de datos a llamar 

class clientes(BaseModel):
    username: str
    level: int
class response(BaseModel): #define la clase 
    message: str
class User(BaseModel):
    email: str
    password: str

class Cliente(BaseModel):#define una clase 
    id_cliente: int
    nombre: str
    email: str
    numero: str
class cliente_add(BaseModel):
    nombre: str
    email: str
    numero: str
class Post(BaseModel):
    nombre: str
    email: str 
    numero: int
class Update(BaseModel):
    id_cliente: int
    nombre: str
    email: str 
    numero: int
class delete(BaseModel):
    id_cliente: int
    
##################################################################################
    


app = FastAPI()
firebaseConfig = {
    "apiKey": "AIzaSyCEkkxRet_lOOvEY4Joq22udSyrHI7gOa0",
    "authDomain": "fb-api-29ea3.firebaseapp.com",
    "databaseURL": "https://fb-api-29ea3-default-rtdb.firebaseio.com",
    "projectId": "fb-api-29ea3",
    "storageBucket": "fb-api-29ea3.appspot.com",
    "messagingSenderId": "500610176971",
    "appId": "1:500610176971:web:187e97d09e0a786a4a484e"
}

firebase = pyrebase.initialize_app(firebaseConfig)




#######################################################################################3
DATABASE_URL = os.path.join("clientes.sqlite")#base de datos a llamar 
app = FastAPI()
class Usuarios(BaseModel):
    username: str
    level: int
security = HTTPBasic()
origins = [
    "*",    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    
)
SecurityBasic = HTTPBasic()
SecurityBearer = HTTPBearer()

#######################################################################################3




@app.get("/", response_model=response,tags= ["get"])#url donde se puede buscar 
async def index(level: int() = Depends(SecurityBearer)):
    return {"message": "Fast API"}#mensaje de correcta ejecucion 
#################################################################################################################
#regresa a todos los usuarios agregados a la base de datos 
@app.get("/user/", response_model=List[Cliente],
status_code= status.HTTP_202_ACCEPTED,
summary = "Lista de clientes",
description = "Da una lista de todos los clientes",
tags= ["GET"])
async def get_clientes(credentials: HTTPAuthorizationCredentials = Depends(SecurityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        with sqlite3.connect('clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)

##########################################################################################
@app.get("/cliente/{id_cliente}", response_model=Cliente,
status_code= status.HTTP_202_ACCEPTED,
summary = "Clientes por ID",
description = "Retorna un cliente baso en un ID",
tags =["get"])
async def clientes_parametros(id_cliente: int, credentials: HTTPAuthorizationCredentials = Depends(SecurityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        with sqlite3.connect("clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("Select * From clientes where id_cliente = {}".format(id_cliente))
            response = cursor.fetchone()
            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="id_cliente no encontrado",
                    headers={"WWW-Authenticate": "Basic"},
            )
            return response
    except Exception as error:
            print(f"Error: {error}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#########################################################################################3
@app.post("/cliente/", response_model=response,
status_code= status.HTTP_202_ACCEPTED,
summary = "Agrega un nuevo cliente",
description = "Agrega un cliente",
tags= ["POST"])

async def cliente_add(cliente_add: Post, credentials: HTTPAuthorizationCredentials = Depends(SecurityBearer)): #definicion de campos que pueden añadir 
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        with sqlite3.connect("clientes.sqlite") as connection: #creacion  de donde se conectara y dopnde se ecuentra la base de datos creada 
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "insert into clientes(nombre,email,numero) values ('{nombre}', '{email}','{numero}')".format(nombre=cliente_add.nombre, email=cliente_add.email, numero=cliente_add.numero)) #campos que incluira la base de datos creada esto para poder relizar una comparacion con la que se ecnuentra en el archivo clientes.sql
            connection.commit()
            return {"message":"usuario agregado"}#mensaje de la correcta ejecucion del post al añadir algun cambio 
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)

@app.put("/clientes/", response_model=response,
status_code= status.HTTP_202_ACCEPTED,
summary = "Actualizara algun cliente",
description = "Actualizara un cliente basado en un id y nombre",
tags = ["PUT"])

async def cliente_put(cliente_put: Update,credentials:  HTTPAuthorizationCredentials = Depends(SecurityBearer)): #en esta parte define los campos que deberia lleavar para poder modificar 
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']
        with sqlite3.connect("clientes.sqlite") as connection:#creacion de la conectividad y la ruta donde se encunetra el archivo de ejecucion
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("Update clientes set nombre = '{name}', email = '{email}',numero ='{numero}' where id_cliente = {id}".format(name=cliente_put.nombre,email=cliente_put.email,numero=cliente_put.numero,id=cliente_put.id_cliente))#campos que debe incluir el campo donde se de sea ejecutar
            connection.commit()
            return {"message":"usuario actualizado"}#mensaje de una correcta ejecucion 
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)     

@app.delete("/delete/{id_cliente}", response_model=response,
status_code= status.HTTP_202_ACCEPTED,
summary = "Lista de clientes",
description = "Da una lista de todos los clientes",
tags= ["DELETE"])#crea una url donde se puede buscar dicho campo asi como los apartados que debe de llevar 
async def cliente_delete(cliente_delete: delete, credentials: HTTPAuthorizationCredentials = Depends(SecurityBearer)):#muestra el campo adicional 
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']
        with sqlite3.connect("clientes.sqlite") as connection:#conectividad con la carpeta en la que se debe alojar 
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("delete from clientes where id_cliente = {}".format(cliente_delete.id_cliente))#campos que se pueden eliminar 
            connection.commit()        
            return {"message":"usuario borrado"}#mensaje de que la ejhecucion del delete se ejecuto de manera correcta 

    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)


@app.get(
    "/users/token/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for user ",
    description="Get a token for user ",
    tags=["auth"]
)
async def get_token(credentials: HTTPBasicCredentials = Depends(SecurityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)

        response = {
            "token": user['idToken'],
        }
        return response
    except Exception as error:
        print(f"ERROR: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get(
    "/users/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a user",
    description="Get a user",
    tags=["auth"]
)
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(SecurityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()

        response = {
            "user_data": user_data
        }
        return response
    except Exception as error:
        print(f"ERROR: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post(
    "/users/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Agregar Usuario",
    description="Agregar Usuario",
    tags=["add"]
)

async def add_user(add_post: User ):
    try:
        email = add_post.email
        password = add_post.password
        auth = firebase.auth()
        datos = {
            'email':email, 
            'nivel': '1',
            'nombre': 'user'
        }
        dato = auth.create_user_with_email_and_password(email, password)
        db=firebase.database()
        db.child("users").child(dato["localId"]).set (datos)
        return {"message":"usuario agregado"} 

    except Exception as error:
        print(f"ERROR: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)