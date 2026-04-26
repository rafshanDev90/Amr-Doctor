import os
import gc
import json
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm
from cerebras.cloud.sdk import Cerebras
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

# --- 1. Banglish Normalizer (Your LLM Layer) ---
class BanglishNormalizer:
    def __init__(self):
        api_key = os.getenv("API_KEY") # Ensure this matches your .env
        self.client = Cerebras(api_key=api_key)
        
    @lru_cache(maxsize=1000)
    def normalize(self, text: str) -> dict:
        prompt = f"""You are a medical translator. Convert Banglish to Bangla and English JSON.
Input: "{text}"
Return ONLY JSON: {{"bangla": "", "english": "", "keywords_bn": [], "keywords_en": []}}"""
        try:
            response = self.client.chat.completions.create(
                model="llama3.1-8b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            content = response.choices[0].message.content.strip()
            if "```json" in content: content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception:
            return {"bangla": text, "english": text, "keywords_bn": [text], "keywords_en": [text]}

normalizer = BanglishNormalizer()

# --- 2. Emergency Logic ---
EMERGENCY_KEYWORDS = ["heart attack", "stroke", "রক্তপাত", "শ্বাসকষ্ট", "অজ্ঞান", "বুকের ব্যথা"]

def check_emergency(query: str, normalized_text: str):
    combined = (query + " " + normalized_text).lower()
    if any(kw in combined for kw in EMERGENCY_KEYWORDS):
        return "⚠️ জরুরী: অবিলম্বে নিকটস্থ হাসপাতালে যান বা ৯৯৯ এ কল করুন।"
    return None

# --- 3. Core RAG System ---
class MedicalRAG:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "vector_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="shihab17/bangla-sentence-transformer"
        )
        # Re-using your collection names
        self.collections = {
            'qa': self.client.get_or_create_collection("med_qa", embedding_function=self.ef),
            'drugs': self.client.get_or_create_collection("drugs", embedding_function=self.ef)
        }

    def ask(self, user_query: str):
        # Step 1: Normalize (Fixes the 'amr matha betha' issue)
        norm = normalizer.normalize(user_query)
        bangla_query = norm['bangla']
        
        # Step 2: Emergency Check
        emergency_msg = check_emergency(user_query, bangla_query)
        if emergency_msg: return emergency_msg

        # Step 3: Search using the CLEANED Bangla Script
        # We query the Q&A collection first
        results = self.collections['qa'].query(
            query_texts=[bangla_query],
            n_results=2
        )

        if not results['documents'][0]:
            return "দুঃখিত, আমি এই বিষয়ে সঠিক তথ্য খুঁজে পাইনি। দয়া করে একজন ডাক্তারের পরামর্শ নিন।"

        # Step 4: Final Response Construction (LLM Reranking)
        context = "\n".join(results['documents'][0])
        return self.generate_answer(bangla_query, context)

    def generate_answer(self, query, context):
        prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer in friendly Bengali:"
        response = normalizer.client.chat.completions.create(
            model="llama3.1-8b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content

# --- 4. Execution Logic ---
if __name__ == "__main__":
    rag = MedicalRAG()
    
    # Test with your problematic query
    user_input = "amr matha betha korche ki korbo"
    print(f"User: {user_input}")
    
    response = rag.ask(user_input)
    print(f"Bot: {response}")
