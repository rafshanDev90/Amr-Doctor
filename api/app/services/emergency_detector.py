import os
import re
from typing import Optional
from app.utils.logger import logger

class MedicalEmergencyDetector:
    def __init__(self):
        # Emergency keywords in both Bangla and English
        self.EMERGENCY_KEYWORDS = [
            # English
            "chest pain", "heart attack", "stroke", "heavy bleeding", 
            "difficulty breathing", "unconscious", "poisoning", "seizure",
            "paralysis", "major accident", "choking", "suicidal thoughts",
            # Bangla
            "বুকে ব্যথা", "হার্ট অ্যাটাক", "স্ট্রোক", "অতিরিক্ত রক্তপাত",
            "শ্বাসকষ্ট", "অজ্ঞান", "বিষক্রিয়া", "খিঁচুনি", "প্যারালাইসিস",
            "দুর্ঘটনা", "দম বন্ধ", "আত্মহত্যার চিন্তা",
            # Banglish
            "buk e betha", "heart attack", "stroke", "rokto", "shash kosto",
            "ogyan", "bish", "khichuni", "paralysis"
        ]
        
    def check_emergency(self, text: str) -> Optional[str]:
        """
        Scans for emergency keywords and returns an emergency message if found.
        """
        text_lower = text.lower()
        found_keywords = [kw for kw in self.EMERGENCY_KEYWORDS if kw.lower() in text_lower]
        
        if found_keywords:
            logger.warning(f"🚨 Emergency detected! Keywords: {found_keywords}")
            return (
                "⚠️ জরুরী সতর্কবার্তা: আপনার বর্ণিত লক্ষণগুলো একটি মেডিকেল ইমার্জেন্সি হতে পারে। "
                "অনুগ্রহ করে তাৎক্ষণিকভাবে নিকটস্থ হাসপাতালের জরুরী বিভাগে যান অথবা ৯৯৯-এ কল করুন। "
                "দেরি করবেন না!"
            )
        return None
