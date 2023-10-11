import asyncio

import uvicorn
from fastapi import FastAPI
from routers.boards.apis import boards_router
from routers.notes import notes_router

notes_app = FastAPI()
notes_app.include_router(notes_router)
notes_app.include_router(boards_router)

if __name__ == "__main__":
    uvicorn.run(notes_app, host="0.0.0.0", port=8000)
