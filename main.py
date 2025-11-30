from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser Angular à parler à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En prod, mettre l'URL Vercel ici
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de données (Validation Pydantic)
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    week: str

# Données simulées (In-Memory pour l'instant)
roadmap_db = [
    {"id": 1, "week": "Semaine 1", "title": "Installer Linux", "completed": False},
    {"id": 2, "week": "Semaine 2", "title": "Apprendre Type Hints", "completed": False},
]

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return roadmap_db

@app.post("api/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    for task in roadmap_db:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return task
    raise HTTPException(status_code=404, detail="Task not found")