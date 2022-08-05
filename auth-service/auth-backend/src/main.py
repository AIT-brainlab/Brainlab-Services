from __future__ import annotations
import argon2
from fastapi import FastAPI, HTTPException, Response, Cookie, Request, Header
from fastapi.responses import RedirectResponse
import pymongo
from pymongo.errors import DuplicateKeyError
from config import BASE_PATH, DOMAIN, LASTEST_PASSWORD_ALG, URL_RESET_EMAIL
from pydantic import BaseModel
from mongo_service import MongoService
from datetime import datetime
from typing import Any
from argon2 import PasswordHasher
from hashlib import sha256
from passlib.hash import phpass  # type:ignore
import secrets
import uuid
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

password_hasher = PasswordHasher()
MongoService.init_db()
app = FastAPI(docs_url=None)
origins = [
    os.environ["HOST"]
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    username: str
    email: str
    password: str


class User(UserInput):
    user_id:str
    user_type: str
    extended_permissions:list
    is_activated: bool
    register_data: float
    alg: str

    @staticmethod
    def from_user_input(user_input: UserInput) -> User:
        user = User(**user_input.dict(),
                    user_id=str(uuid.uuid4()),
                    user_type="NORMAL_USER",
                    extended_permissions=[],
                    is_activated=False,
                    register_data=datetime.now().timestamp(),
                    alg=LASTEST_PASSWORD_ALG)

        user.password = password_hasher.hash(user.password)
        return user

    def save_to_db(self) -> None:
        data: dict[str, Any] = self.dict()
        MongoService.get_user_collection_instance().insert_one(data)


@app.post(BASE_PATH+"/register")
def register(user_input: UserInput):
    try:
        User.from_user_input(user_input).save_to_db()
    except DuplicateKeyError:
        raise HTTPException(400, detail="duplicated username")
    return {"result": 1}


# TODO: activate account

class LoginInput(BaseModel):
    username: str
    password: str


@app.get(BASE_PATH+"/login")
def login(username: str, password: str, resp:Response)->dict:
    user: User
    q = MongoService.get_user_collection_instance().find_one(
        {'username': username})
    if q is None:
        raise HTTPException(400, detail="username and password are incorrect.")
    user = User(**q)
    if user.alg != LASTEST_PASSWORD_ALG:
        try:
            if user.alg == 'wp':
                new_hash: str = wp_rehash(user.password, password)
                user = User(**MongoService.get_user_collection_instance().find_one_and_update(
                    {"username": username},
                    {'$set': {'password': new_hash,'alg':LASTEST_PASSWORD_ALG}},
                    return_document=pymongo.ReturnDocument.AFTER
                ))


        except RehashCannotVerify:
            raise HTTPException(400, detail="username and password are incorrect.")


    try:
        password_hasher.verify(user.password, password)
    except (argon2.exceptions.InvalidHash,argon2.exceptions.VerifyMismatchError):
        raise HTTPException(400,detail="username and password are incorrect.")
    session_id = secrets.token_urlsafe(32)
    MongoService.get_user_session_instance().insert_one({
        "session_id":hash_function(session_id),
        "user_id":user.user_id,
        "created_time":datetime.utcnow()
    }) 
    resp.set_cookie("session_id",session_id)


    return {"result":1}


class RehashCannotVerify(RuntimeError):
    pass


def wp_rehash(stored_password: str, password: str) -> str:

    if not phpass.verify(password, stored_password):
        raise RehashCannotVerify()
    return password_hasher.hash(password)


class ForgetMypasswordInput(BaseModel):
    username: str


@app.post(BASE_PATH+"/forget-mypassword")
def forget_mypassword(forget_input: ForgetMypasswordInput):
    token: str = secrets.token_urlsafe(32)
    q = MongoService.get_user_collection_instance().find_one(
        {"username": forget_input.username})
    if q is None:
        raise HTTPException(404, detail="username not found")

    print(
        f"token reset password link: {URL_RESET_EMAIL}/auth/#/reset-password?token={token}")
    # TODO: email to user

    token_in_db: str = hash_function(token)
    MongoService.get_forget_password_token_instance().insert_one({
        "user_id": q['user_id'],
        "token": token_in_db,
        "created_time":datetime.utcnow()
    })
    return {"result":1}


class ResetPasswordInput(BaseModel):
    token: str
    new_password: str


@app.put(BASE_PATH+"/forget-mypassword/reset")
def forget_mypassword_verify_token(session: ResetPasswordInput):
    q = MongoService.get_forget_password_token_instance().find_one_and_delete({
        "token": hash_function(session.token)
    })
    if q is None:
        raise HTTPException(404, detail="token not found")
    user_id: str = q['user_id']
    
    q = MongoService.get_user_collection_instance().find_one_and_update(
        {"user_id": user_id},
        {"$set": {"password": password_hasher.hash(session.new_password),
        'alg':LASTEST_PASSWORD_ALG}}
    )
    if q is None:
        raise HTTPException(404, detail="user not found")
    return {"result":1}


def hash_function(data: str) -> str:
    return sha256(data.encode("utf-8")).hexdigest()


def hash_verify(hash1: str, hash2: str) -> bool:
    bools: list[bool] = []
    for h1, h2 in zip(hash1, hash2):
        bools.append(h1 == h2)
    return all(bools)





@app.get('/authc/who_are_they')
def get_user_id_by_session_id( head:str=Header(default="",alias="X-Forwarded-Uri"), session_id:str = Cookie(default="")):
    username = head.split("/")[1]
    
  
    user = MongoService.get_user_session_instance().find_one({"session_id":hash_function(session_id)})
    if user is None:
        raise HTTPException(404,"session not found")
    user_id:str = user['user_id']
    q = MongoService.get_user_collection_instance().find_one({"user_id":user_id})

    if q is None:
        raise HTTPException(404,"session not found")
    q_username = q['username']
    if q_username != username:
        raise HTTPException(404,"session not found")

    q = MongoService.get_user_session_instance().find_one_and_update(
        {
            "session_id": hash_function(session_id)
        },
        {
            "$set":{"created_time":datetime.utcnow()}
        }
    
    )
    if q is None:
        raise HTTPException(404,"session not found")
    return {"user_id":q['user_id']}
    