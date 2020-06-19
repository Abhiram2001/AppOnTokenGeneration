import uvicorn
import os, random, string
from fastapi import FastAPI
from fastapi_mail import FastMail
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from config import MONGODB_URL, MONGODB_DB_NAME, MAIL_PASS
from passlib.context import CryptContext
from models import UserInDB, User, Photo
from fastapi.middleware.cors import CORSMiddleware
import jwt
import datetime
import base64
import PIL
import face_recognition

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = AsyncIOMotorClient(MONGODB_URL)
db = client.get_database("MONGODB_DB_NAME")
collection = db.get_collection("Users")
pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


@app.post("/Signupcheck")
async def Signupcheck(user: UserInDB):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Users")
    row = await collection.find_one({"username": user.username})
    if row:
        print("User Already Exists")
        return {"message": "False"}
    else:
        print("No User Exists")
        usr = {'username': user.username, 'role': 'user', 'DateOfBirth': user.DateOfBirth, 'FirstName': user.FirstName,
               'LastName': user.LastName, 'Email': user.Email,
               'password': pwd_context.hash(user.password)}

        dbuser = UserInDB(**usr)
        collection.insert_one(dbuser.dict())

    return {"message": "True"}


@app.post("/Logincheck")
async def Logincheck(user: User):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Users")
    row = await collection.find_one({"username": user.username})
    if row:
        mpassword = row['password']
        password = user.password
        if pwd_context.verify(password, mpassword):
            token = jwt.encode(
                {'user': user.username, 'scope': 'user', 'iss': 'Your Service Provider',
                 'sub': 'Subject',
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                'SECRET_KEY')

            return {'message': 'True', 'token': token}
        else:
            return {'message': 'False', 'token': 'Token Not Generated Due to Wrong Credentials'}
    return {'message': 'False', 'token': 'Token Not Generated Due to Wrong Credentials'}


@app.post("/Usercheck")
async def Usercheck(user: User):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Users")
    row = await collection.find_one({"username": user.username})
    if row:
        return {"message": "True"}
    else:
        return {"message": "False"}


@app.post("/Photocheck")
async def Photocheck(photo: Photo):
    header, encoded = photo.image.split(",", 1)
    data = base64.b64decode(encoded)
    with open("image.png", "wb") as f:
        f.write(data)
    return {"message": "ture"}


@app.post("/genpassword")
async def genpassword(background_tasks: BackgroundTasks, user: UserInDB) -> JSONResponse:
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Users")
    row = await collection.find_one({"username": user.username})
    if row:
        length = 13
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        random.seed = (os.urandom(1024))
        newpass = (''.join(random.choice(chars) for i in range(length)))
        mail = FastMail(email="Your Gmail Account", password=MAIL_PASS, tls=True, port="587",
                        service="gmail")
        background_tasks.add_task(mail.send_message, recipient=row["Email"], subject="AUTH-E Password Generation",
                                  body="Generated password is :  " + newpass, text_format="html")
        # row['password'] = pwd_context.hash(newpass)
        print(newpass)
        return {"message": "True"}

    else:
        return {"message": "False"}


if __name__ == '__main__':
    uvicorn.run(app)
