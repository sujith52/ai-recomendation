from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.item import router as item_router
from app.routes.interactions import router as interaction_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is working!"}

# Include all route modules
app.include_router(user_router)
app.include_router(item_router)
app.include_router(interaction_router)


