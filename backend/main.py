from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from QAChain import get_chain_result
from pydantic import BaseModel

from utils import clean_answer, parse_request

class QAResponse(BaseModel):
    question: str
    answer: str

class Config:
    ALLOWED_ORIGINS = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:8081", 
        "http://localhost:8082",
        "http://localhost:8085",
    ]
    SEPARATOR = "+++"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{request}", response_model=QAResponse)
async def get_qa_response(request: str) -> QAResponse:
    """Process QA request and return response"""
    try:
        query_parts = parse_request(request, Config.SEPARATOR)
        if not query_parts:
            raise HTTPException(status_code=400, detail="Invalid request format")
        
        raw_response = await get_chain_result(request)
        cleaned_answer = clean_answer(raw_response)
        
        return QAResponse(
            question=query_parts[-1],
            answer=cleaned_answer
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}")