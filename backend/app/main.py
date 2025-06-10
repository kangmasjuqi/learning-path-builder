# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, users, courses, lessons, quizzes, progress # Import your routers

# Create the FastAPI app instance
app = FastAPI(
    title="Interactive Learning Path Builder API",
    description="A full-stack EdTech platform for creating interactive learning paths with quizzes and progress tracking.",
    version="0.1.0",
    docs_url="/docs", # Default Swagger UI documentation
    redoc_url="/redoc", # Default ReDoc documentation
)

# Configure CORS (Cross-Origin Resource Sharing)
# This is crucial for allowing your Next.js frontend to talk to your backend
# In production, replace "*" with your frontend's actual URL(s)
origins = [
    "http://localhost",
    "http://localhost:3000", # Next.js default development port
    # Add your frontend's production URL here when deployed
    # "https://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers, including Authorization
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(lessons.router, prefix="/api/v1/lessons", tags=["Lessons"])
app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["Quizzes"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])

@app.get("/api/v1/health", summary="Health Check")
async def health_check():
    return {"status": "ok", "message": "API is running"}

# Basic root endpoint (optional)
@app.get("/")
async def root():
    return {"message": "Welcome to the Interactive Learning Path Builder API"}