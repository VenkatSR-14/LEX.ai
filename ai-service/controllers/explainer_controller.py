from fastapi import FastAPI, APIRouter, HTTPException
from services.explainer import AIExplainer
from views.api_schema import ExplainRequest

router = APIRouter()
ai_explainer = AIExplainer()

@router.post("/explain")
async def explain_text(request: ExplainRequest):
    """
    Generate AI explanation for selected text
    """
    
    try:
        explanation = ai_explainer.explain(request.text, request.context)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining text: {str(e)}")
    