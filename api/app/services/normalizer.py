import os
import json
from cerebras.cloud.sdk import Cerebras
from functools import lru_cache
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

class BanglishNormalizer:
    def __init__(self):
        api_key = os.getenv("API_KEY")
        if not api_key:
            logger.error("API_KEY not found in environment variables.")
        self.client = Cerebras(api_key=api_key)
        
    @lru_cache(maxsize=1000)
    def normalize(self, text: str) -> dict:
        """
        Normalize Banglish to Bangla Unicode and Clinical English using Cerebras.
        Uses lru_cache for cost efficiency.
        """
        logger.debug(f"Normalizing query: {text}")
        
        prompt = f"""You are a clinical transliterator. Convert this medical query into pure Bengali Unicode AND clinical English.
        Input: "{text}"
        Return ONLY JSON format:
        {{
            "bangla": "Bengali script",
            "english": "Clinical English",
            "is_banglish": true/false
        }}"""

        try:
            response = self.client.chat.completions.create(
                model="llama3.1-8b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=150
            )
            
            content = response.choices[0].message.content.strip()
            # Handle potential markdown formatting in LLM response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            result = json.loads(content)
            logger.info(f"Normalization success for '{text}'")
            return result
            
        except Exception as e:
            logger.error(f"Normalization failed for '{text}': {str(e)}")
            return {
                "bangla": text,
                "english": text,
                "is_banglish": False
            }
