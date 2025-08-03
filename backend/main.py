from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import database
import asyncio
from datetime import datetime

app = FastAPI()

# ✅ Add this CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # or ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NoteIn(BaseModel):
    content: str
    tags: Optional[List[str]] = []

class NoteOut(BaseModel):
    id: int
    content: str
    tags: Optional[List[str]] = []
    created_at: datetime


@app.on_event("startup")
async def startup():
    import time
    for attempt in range(10):
        try:
            await database.database.connect()
            print("✅ Connected to database!")
            break
        except Exception as e:
            print(f"❌ DB connection failed (attempt {attempt + 1}): {e}")
            time.sleep(2)
    else:
        raise RuntimeError("Could not connect to the database after multiple attempts")


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


@app.get("/notes", response_model=List[NoteOut])
async def get_notes():
    query = database.notes.select()
    rows = await database.database.fetch_all(query)
    return [dict(row) for row in rows]


@app.post("/notes", response_model=NoteOut)
async def add_note(note: NoteIn):
    now = datetime.utcnow()
    query = database.notes.insert().values(
        content=note.content,
        tags=note.tags,
        created_at=now
    )
    note_id = await database.database.execute(query)
    return {**note.dict(), "id": note_id, "created_at": now}


@app.put("/notes/{note_id}", response_model=NoteOut)
async def update_note(note_id: int, note: NoteIn):
    query = database.notes.update().where(database.notes.c.id == note_id).values(
        content=note.content,
        tags=note.tags
    )
    result = await database.database.execute(query)
    if result:
        # Fetch the updated note
        fetch_query = database.notes.select().where(database.notes.c.id == note_id)
        updated = await database.database.fetch_one(fetch_query)
        return dict(updated)
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    query = database.notes.delete().where(database.notes.c.id == note_id)
    result = await database.database.execute(query)
    if result:
        return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Note not found")
