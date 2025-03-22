from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.document_controller import router as document_router
from controllers.chapter_controller import router as chapter_router
from controllers.explainer_controller import router as explainer_router
from dotenv import load_dotenv
# inititalizing the application
import uvicorn
import string

load_dotenv()

app = FastAPI(title = "LEX.AI", description = "An AI service for educational content analysis", version = "0.1")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router)
app.include_router(chapter_router)
app.include_router(explainer_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
    