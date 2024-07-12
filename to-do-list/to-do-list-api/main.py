from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

from models.tasks import Task

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

load_dotenv()
mongo_url = os.getenv("MONGO_URL")
mongo_db_name = os.getenv("MONGO_DB_NAME")
mongo_collection_name = os.getenv("MONGO_COLLECTION_NAME")

client = MongoClient(mongo_url)
db = client.get_database(mongo_db_name)
task_collection = db[mongo_collection_name]

@app.get('/')
async def root():
    return "Hello my friend"

@app.get('/tasks/')
async def get_tasks():
    try:
        tasks = task_collection.find()
        task_list = []
        for task in tasks:
            task_list.append({
                "id": str(task["_id"]),
                "title": task["title"],
                "description": task["description"],
                "status": task["status"]
            })
        return JSONResponse(content={"tasks": task_list})
    except Exception as e:
        return {"error": str(e)}

@app.post('/tasks/')
async def create_task(task: Task):
    try:
        result = task_collection.insert_one(task.dict())
        new_task = task_collection.find_one({"_id": result.inserted_id})
        new_task["id"] = str(new_task["_id"])
        return JSONResponse(content=new_task)
    except Exception as e:
        return {"error": str(e)}

@app.put('/tasks/{task_id}')
async def edit_task(task_id: str, task: Task):
    try:
        result = task_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": task.dict()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        updated_task = task_collection.find_one({"_id": ObjectId(task_id)})
        updated_task["id"] = str(updated_task["_id"])
        return JSONResponse(content=updated_task)
    except Exception as e:
        return {"error": str(e)}

@app.delete('/tasks/{task_id}')
async def delete_task(task_id: str):
    try:
        result = task_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted"}
    except Exception as e:
        return {"error": str(e)}
