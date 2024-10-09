from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.itemRoutes import router as item_router
from routes.authRoutes import router as auth_router
from database import get_db

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# Include the item and auth routes
app.include_router(item_router, dependencies=[Depends(get_db)])
app.include_router(auth_router)

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")