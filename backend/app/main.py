from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth,tasks
app=FastAPI(title="Assignment",version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])



@app.get("/")
def root():
    return("Backend is live")