from fastapi import APIRouter, HTTPException, UploadFile, File
from services.document_processor import DocumentProcessor    
import uuid
import os

router = APIRouter()
document_processor = DocumentProcessor()

@router.post("/analyze/document")
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze the document and extract structure
    """
    
    try:
        temp_file_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.file.read())
        result = document_processor.analyze_document(temp_file_path)
        os.remove(temp_file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")
    
