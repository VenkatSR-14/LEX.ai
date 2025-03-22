from fastapi import FastAPI, APIRouter, HTTPException
from services.document_processor import DocumentProcessor
from views.api_schema import ChapteAnalysisRequest


router = APIRouter()
document_processor = DocumentProcessor()

@router.post("/analyze/chapter")
async def analyze_chapter(request: ChapteAnalysisRequest):
    """
    Analyze the chapter content
    """
    
    try:
        result = document_processor.analyze_chapter(request.content, request.document_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing chapter: {str(e)}")