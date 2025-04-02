from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from models import *
import os


# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def populate_db():
    session = Session(engine)

    for k in TileSpecificsTemplate.keys():
        addTileSpecificsTemplates = TileSpecifics(name=k, specifics=TileSpecificsTemplate[k])
        session.add(addTileSpecificsTemplates)

    session.commit()

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     init_db()
#     yield

# app = FastAPI(lifespan=lifespan)
init_db()

populate_db()

app = FastAPI()

# Serve static files from the "frontend" directory
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file_path = os.path.join("frontend", "index.html")
    with open(index_file_path) as f:
        return HTMLResponse(content=f.read())

# @app.get("/items")
# async def read_items(db=Depends(get_session)):
#     items = db.query(ChecklistItem).all()
#     return items

# @app.get("/items/new")
# async def create_item(db=Depends(get_session)):
#     new_item = ChecklistItem(description="New Item", completed=False)
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, updated_item: ChecklistItemUpdate, db=Depends(get_session)):
#     db_item = db.query(ChecklistItem).filter(ChecklistItem.id == item_id).first()
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     db_item.description = updated_item.description
#     db_item.completed = updated_item.completed
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")
