from fastapi import APIRouter,HTTPException,status,Depends
from typing import List
from bson import ObjectId
from jose import jwt,JWTError
import os

from app.db.db import tasks_collection,users_collection
from app.models.tasks import TaskCreateSchema,TaskUpdateSchema
from app.routes.auth import oauth2_scheme
from app.core.config import settings


router = APIRouter()




def get_current_user(token: str =Depends(oauth2_scheme)):
    credential_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload= jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        email:str=payload.get("sub")
        if email is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user=users_collection.find_one({"email":email})
    if user is None:
        raise credential_exception
    return user
@router.post("/",response_description="Add a new task")
def create_task(task: TaskCreateSchema,current_user: dict=Depends(get_current_user)):
    if current_user["role"]!="admin":
        raise HTTPException(status_code=403,detail="Only admins can create tasks")
    task_dict = task.dict()
    
    result=tasks_collection.insert_one(task_dict)
    return{"id": str(result.inserted_id),"Message": "Task created"}
@router.get("/",response_description="List all tasks")
def show_tasks(current_user: dict=Depends(get_current_user)):
    tasks= list(tasks_collection.find({}))

    for task in tasks:
        task["_id"]= str(task["_id"])
    return tasks

@router.put("/{id}")
def update_task(id: str, task_data: TaskUpdateSchema, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400,detail="Invalid ID")
    update_data = {k: v for k, v in task_data.dict().items() if v is not None}

    if current_user.get("role") != "admin":

        if "title" in update_data or "description" in update_data:
            raise HTTPException(status_code=403,detail="You can only update the status of the task")
    result = tasks_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        return {"message": "Task updated successfully"}
    raise HTTPException(status_code=404,detail="Task not found")

@router.delete("/{id}",response_description="Delete a task")
def delete_task(id: str,current_user: dict= Depends(get_current_user)):
    if current_user["role"]!="admin":
        raise HTTPException(status_code=403,detail="Only admins can delete tasks")
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400,detail="Invalid ID")
    result= tasks_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count==1:
        return{"message":"Task deleted successfully"}
    raise HTTPException(status_code=404,detail="Task not found")