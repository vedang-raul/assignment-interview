from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from bson import ObjectId
from jose import jwt,JWTError
import os

from app.models.user import UserRegisterSchema
from app.core.security import get_password_hash,verify_password,create_access_token
from app.db.db import users_collection
from app.core.config import settings

router = APIRouter()

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

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

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegisterSchema):
    if users_collection.find_one({"email":user.email}):
        raise HTTPException(status_code=400,detail="Email already registered")
    
    hashed_pwd= get_password_hash(user.password)

    role="user"

    if user.admin_code == settings.ADMIN_CODE:
        role="admin"

    user_dict= {
        "username": user.username,
        "email":user.email,
        "password": hashed_pwd,
        "role":role
        
    }

    users_collection.insert_one(user_dict)
    return{"message":"User created successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user=users_collection.find_one({"email": form_data.username})

    if not db_user or not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
    access_token= create_access_token(data={"sub": db_user["email"],"role": db_user["role"]})
    return{"access_token": access_token,"token_type": "bearer"}
@router.get("/get-all")
def get_all_users(current_user: dict=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Only admins can access this resource")
    users= list(users_collection.find({}))

    for user in users:
        user["_id"]= str(user["_id"])
    return users
@router.delete("/delete/{user_id}")
def delete_user(user_id:str,current_user: dict=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Only admins can delete users")
    result= users_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count==1:
        return{"message":"User deleted successfully"}
    else:
        raise HTTPException(status_code=404,detail="User not found")