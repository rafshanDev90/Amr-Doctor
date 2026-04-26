from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import time
import sys
import os

# Ensure the app directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.normalizer import BanglishNormalizer
from app.services.emergency_detector import MedicalEmergencyDetector
from app.services.rag_coordinator import RAGCoordinator
from app.utils.logger import logger

app = FastAPI(title="Bangla Med AI - Refactored")

# Initialize modular services
normalizer = BanglishNormalizer()
emergency_detector = MedicalEmergencyDetector()
rag_coordinator = RAGCoordinator()

class QueryRequest(BaseModel):
    query: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} | Duration: {duration:.2f}s | Status: {response.status_code}")
    return response

@app.post("/query")
async def handle_query(request: QueryRequest):
    try:
        user_query = request.query.strip()
        logger.info(f"Incoming query: {user_query}")

        # 1. Emergency Check (The Interceptor)
        emergency_msg = emergency_detector.check_emergency(user_query)
        if emergency_msg:
            return {"answer": emergency_msg, "status": "emergency"}

        # 2. Input Normalization (Banglish to Bangla/English)
        normalized_data = normalizer.normalize(user_query)

        # 3. Context Retrieval (Multi-collection with thresholding)
        context = rag_coordinator.retrieve_context(normalized_data)
        logger.debug(f"Retrieved context length: {len(context)}")

        # 4. Answer Generation (With strict guardrails)
        answer = rag_coordinator.generate_answer(user_query, context)
        
        return {
            "answer": answer,
            "normalized": normalized_data,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Endpoint error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
