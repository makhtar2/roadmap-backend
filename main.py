from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle complet (ce que l'API renvoie)
class Task(BaseModel):
    id: int
    week: str
    title: str
    completed: bool

# Modèle d'entrée (ce que le Frontend envoie pour créer)
class TaskInput(BaseModel):
    week: str
    title: str

# Base de données simulée
db = [
    {"id": 1, "week": "Semaine 1", "title": "Installer Linux", "completed": True},
    {"id": 2, "week": "Semaine 2", "title": "Apprendre Type Hints", "completed": False},
]

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return db

@app.post("/api/tasks", response_model=Task)
def create_task(task: TaskInput):
    # On génère un ID simple (le max actuel + 1)
    new_id = 1
    if len(db) > 0:
        new_id = max(t["id"] for t in db) + 1
        
    new_task = {
        "id": new_id,
        "week": task.week,
        "title": task.title,
        "completed": False
    }
    db.append(new_task)
    return new_task

@app.post("/api/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    for task in db:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return task
    raise HTTPException(status_code=404, detail="Tâche non trouvée")

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    global db
    # On garde toutes les tâches SAUF celle qui a l'ID donné
    db = [t for t in db if t["id"] != task_id]
    return {"message": "Tâche supprimée"}