from fastapi import FastAPI
from routes import auth, games

app = FastAPI(title="GeoInsight API")

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(games.router, prefix="/data", tags=["Game Data"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the GeoInsight API"}
