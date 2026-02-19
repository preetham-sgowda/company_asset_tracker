from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from . import models, database
from .routers import assets, employees, assignments, departments, locations, vendors, categories, maintenance

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Opti Assist API",
    description="Enterprise Asset Management System API",
    version="1.0.0",
)

# --- Register all routers ---
app.include_router(assets.router)
app.include_router(employees.router)
app.include_router(assignments.router)
app.include_router(departments.router)
app.include_router(locations.router)
app.include_router(vendors.router)
app.include_router(categories.router)
app.include_router(maintenance.router)


@app.get("/", tags=["System"])
def read_root():
    return {"message": "Welcome to Opti Assist API"}


@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(database.get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
