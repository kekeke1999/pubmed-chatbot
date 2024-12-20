from typing import List
from fastapi import HTTPException

def clean_answer(raw_answer: str) -> str:
    """Clean and format answer text"""
    answer = raw_answer.lower()
    for prefix in ["answer:", "answer："]:
        if prefix in answer:
            answer = answer.split(prefix)[1]
            break
    return answer.strip()

def parse_request(request: str, separator: str) -> List[str]:
    """Parse request string and return query parts"""
    if not request:
        raise HTTPException(status_code=400, detail="Empty request")
    return [part for part in request.split(separator) if part]