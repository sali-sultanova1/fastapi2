from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, HTTPException
from typing import List
import json
import hashlib
from models import UserCreate, PasswordUpdate
from utils import load_users, save_users, logs
from fastapi.middleware.cors import CORSMiddleware 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#1
@app.post("/users")
def create(data: UserCreate):
    #12
    if data.username == "" or data.password == "":
        return {"error": "Имя или пароль не могут быть пустыми"}

    #4
    if len(data.password) < 6 or data.password.isdigit():
        return {"error": "Слишком простой пароль"}

    users = load_users()
    
    #5
    for i in users:
        if i["username"] == data.username:
            return {"error": "Такой пользователь уже существует"}
        
    new_id = 1
    if len(users) > 0:
        maxx = users[0]["id"]
        for i in users:
            if i["id"] > maxx:
                maxx = i["id"]
        new_id = maxx + 1
    
    #15
    hashed_pass = hashlib.sha256(data.password.encode()).hexdigest()

    new_user = {
        "id": new_id,
        "username": data.username,
        "password": hashed_pass,
        "role": data.role
    }

    users.append(new_user)
    save_users(users)
    
    logs(f"Пользователь {data.username} зарегистрирован")
            
    #new3
    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "role": new_user["role"]
    }
            

#2
@app.get("/users")
def get_users():
    users = load_users()
    filtered = []
    for i in users:
        filtered.append({
            "id": i["id"],
            "username": i["username"],
            "role": i["role"]
        })
    return filtered


#new2
@app.post("/login")
def login(data: UserCreate):
    users = load_users()
    incoming_hash = hashlib.sha256(data.password.encode()).hexdigest()

    for i in users:
        if i["username"] == data.username and i["password"] == incoming_hash:
            return {"message": "Успешный вход"}

    return {"error": "Неверный логин или пароль"}


#11
@app.middleware("http")
async def log_requests(request: Request, next):
    print(f"{request.method} {request.url.path}")
    response = await next(request)
    return response


#6&8
@app.get("/users/search")
def search(text: str):
    users = load_users()
    filtered = []
    for i in users:
        if text.lower() in i["username"].lower():
            filtered.append({
                "id": i["id"],
                "username": i["username"],
                "role": i["role"]
            })
    return filtered
    

#7&7
@app.get("/users/count")
def get_users_count():
    users = load_users()
    return {"count": len(users)}

@app.get("/users/stats")
def get_users_stats():
    users = load_users()
    if len(users) == 0:
        return {"users_count": 0, "longest_username": ""}

    longest_name = users[0]["username"]
    for i in users:
        if len(i["username"]) > len(longest_name):
            longest_name = i["username"]

    return {
        "users_count": len(users),
        "longest_username": longest_name
    }

#9
@app.get("/users/sort")
def sort_users(order: str = "asc"):
    users = load_users()

    temp_list = []
    for i in users:
        temp_list.append([i["username"], i["id"], i["role"]])
    
    temp_list.sort()
    if order == "desc":
        temp_list.reverse()

    clean_users = []
    for i in temp_list:
        clean_users.append({
            "id": i[1],
            "username": i[0],
            "role": i[2]
        })

    return clean_users


#3&3
@app.get("/users/{user_id}")
def get_user(user_id: int):
    users = load_users()
    for i in users:
        if i["id"] == user_id:
            return {
                "id": i["id"],
                "username": i["username"],
                "role": i["role"]
            }
    return {"error": "Пользователь не найден"}


#4
@app.put("/users/{user_id}")
def update_password(user_id: int, data: PasswordUpdate):
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            user["password"] = hashlib.sha256(data.password.encode()).hexdigest()
            save_users(users)

            logs(f"Пароль пользователя {user['username']} изменен")

            return {"message": "Пароль успешно изменен"}
            
    return {"error": "Пользователь не найден"}


#new1
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    users = load_users()
    found_index = -1

    for i in range(len(users)):
        if users[i]["id"] == user_id:
            found_index = i
            break

    if found_index == -1:
        return {"error": "Пользователь не найден"}

    deleted_user = users.pop(found_index)
    save_users(users)
    logs(f"Пользователь {deleted_user['username']} удален")

    return {"message": "Пользователь удален"}