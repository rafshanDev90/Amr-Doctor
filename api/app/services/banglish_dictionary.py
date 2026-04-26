# Common Banglish→Bangla mappings
BANGLISH_TO_BANGLA_MAP = {
    # Body parts
    "matha": "মাথা",
    "mata": "মাথা",
    "mathay": "মাথায়",
    "buk": "বুক",
    "pet": "পেট",
    "hath": "হাত",
    "pa": "পা",
    "chokh": "চোখ",
    "kan": "কান",
    "nak": "নাক",
    "gola": "গলা",
    "dant": "দাঁত",
    "pith": "পিঠ",
    "komor": "কোমর",
    "hatu": "হাঁটু",
    
    # Symptoms
    "betha": "ব্যথা",
    "batha": "ব্যথা",
    "byatha": "ব্যথা",
    "korche": "করছে",
    "kortese": "করতেছে",
    "hochche": "হচ্ছে",
    "hocche": "হচ্ছে",
    "jontrona": "যন্ত্রণা",
    "jor": "জ্বর",
    "kashi": "কাশি",
    "sardi": "সর্দি",
    "matha ghora": "মাথা ঘোরা",
    
    # Common phrases
    "ki korbo": "কী করবো",
    "ki korte hobe": "কী করতে হবে",
    "kivabe": "কিভাবে",
    "kemon": "কেমন",
    "koto": "কত",
    "kothay": "কোথায়",
    
    # Medical
    "doctor": "ডাক্তার",
    "daktar": "ডাক্তার",
    "hospital": "হাসপাতাল",
    "oshudh": "ওষুধ",
    "oshud": "ওষুধ",
    "tablet": "ট্যাবলেট",
    "injection": "ইনজেকশন",
}

def quick_banglish_replace(text: str) -> str:
    """
    First pass: dictionary-based replacement
    Catches 60-70% of common Banglish terms instantly
    """
    words = text.lower().split()
    replaced = []
    
    for word in words:
        replaced.append(BANGLISH_TO_BANGLA_MAP.get(word, word))
    
    return " ".join(replaced)

def is_likely_banglish(text: str) -> bool:
    """
    Detect if text is Banglish (English characters but Bengali language)
    """
    # If contains Bengali Unicode characters, it's already Bangla
    bengali_chars = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
    if bengali_chars > len(text) * 0.3:  # >30% Bengali characters
        return False
    
    # If mostly ASCII but has Banglish markers
    banglish_markers = ['amr', 'amar', 'tumi', 'apni', 'ki', 'kivabe', 
                        'kemon', 'kno', 'keno', 'kothay', 'kobe']
    words = text.lower().split()
    if any(marker in words for marker in banglish_markers):
        return True
    
    return False
