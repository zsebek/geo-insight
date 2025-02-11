from fastapi import FastAPI
from routers import auth, games, stats, plots

app = FastAPI(title="GeoInsight API")

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(games.router, prefix="/games", tags=["Game Data"])
app.include_router(stats.router, prefix="/stats", tags=["Game Statistics"])
app.include_router(plots.router, prefix="/plots", tags=["Plots"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the GeoInsight API"}
