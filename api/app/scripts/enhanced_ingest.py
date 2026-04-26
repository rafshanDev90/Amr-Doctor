import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm
import os
import gc

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "vector_db")

EMERGENCY_KEYWORDS_BN = [
    "হার্ট অ্যাটাক", "স্ট্রোক", "রক্তপাত", "স্কুই", "খাবারে পয়লা",
    "শ্বাসকষ্ট", "অজ্ঞান", "হারিয়ে যাওয়া", "মাথা ঘোরা", "বুকে ব্যথা",
    "ডায়াবেটিস", "প্রেগন্যান্সি", "এলার্জি", "সাপ কামড়", "বিষ খাওয়া"
]

EMERGENCY_KEYWORDS_EN = [
    "heart attack", "stroke", "bleeding", "suicide", "food poisoning",
    "breathlessness", "unconscious", "lost consciousness", "dizziness", "chest pain",
    "diabetes", "pregnancy", "allergy", "snake bite", "poison"
]


def get_emergency_response(query: str) -> tuple[bool, str]:
    query_lower = query.lower()
    for kw in EMERGENCY_KEYWORDS_BN + EMERGENCY_KEYWORDS_EN:
        if kw.lower() in query_lower:
            return True, "⚠️ জরুরী: অনুগ্রহ করে immediately ডাক্তারের কাছে যান বা হাসপাতালে যোগাযোগ করুন। এটি জরুরী মেডিকেল পরিস্থিতি হতে পারে।\n\n☎️ জরুরী হেল্পলাইন: ৯৯৯"
    return False, ""


def create_collections(client, bangla_ef):
    """Create separate collections for different data sources"""
    collections = {}
    
    collections['med_qa'] = client.get_or_create_collection(
        name="med_qa",
        embedding_function=bangla_ef
    )
    
    collections['drugs'] = client.get_or_create_collection(
        name="drugs",
        embedding_function=bangla_ef
    )
    
    collections['generics'] = client.get_or_create_collection(
        name="generics",
        embedding_function=bangla_ef
    )
    
    return collections


def ingest_med_qa(collections, batch_size=100):
    """Ingest medical Q&A from exam dataset"""
    print("\n📚 Ingesting Medical Q&A...")
    df = pd.read_csv(f"{RAW_DATA_PATH}/bangla-med-qa.csv")
    print(f"   Found {len(df)} Q&A records")
    
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        
        documents = [
            f"প্রশ্ন: {row['question']} উত্তর: {row['answer']} ব্যাখ্যা: {row.get('explanation', '')}"
            for _, row in batch.iterrows()
        ]
        ids = [f"qa_{idx}" for idx in batch.index]
        metadatas = [
            {"source": "med_qa", "exam": str(row.get('exam_name', ''))}
            for _, row in batch.iterrows()
        ]
        
        collections['med_qa'].add(ids=ids, documents=documents, metadatas=metadatas)
        del documents, ids, metadatas
        gc.collect()
    
    print(f"   ✅ Ingested {len(df)} Q&A records")


def ingest_medicine(collections, batch_size=50):
    """Ingest medicine brand data"""
    print("\n💊 Ingesting Medicine brands...")
    df = pd.read_csv(f"{RAW_DATA_PATH}/medicine.csv")
    print(f"   Found {len(df)} medicine records")
    
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        
        documents = []
        ids = []
        metadatas = []
        
        for _, row in batch.iterrows():
            doc = f"ওষুধ: {row['brand name']} | প্রতিরূপ (Generic): {row['generic']} | শক্তি: {row['strength']} | কোম্পানি: {row['manufacturer']} | রূপ: {row['dosage form']}"
            documents.append(doc)
            ids.append(f"med_{row['brand id']}")
            metadatas.append({
                "source": "medicine",
                "brand": row['brand name'],
                "generic": row['generic'],
                "manufacturer": row['manufacturer']
            })
        
        collections['drugs'].add(ids=ids, documents=documents, metadatas=metadatas)
        del documents, ids, metadatas
        gc.collect()
    
    print(f"   ✅ Ingested {len(df)} medicine records")


def ingest_generics(collections, batch_size=50):
    """Ingest generic drug information"""
    print("\n🔬 Ingesting Generic drugs...")
    df = pd.read_csv(f"{RAW_DATA_PATH}/generic.csv")
    print(f"   Found {len(df)} generic records")
    
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        
        documents = []
        ids = []
        metadatas = []
        
        for _, row in batch.iterrows():
            doc = f"ওষুধ: {row['generic name']} | শ্রেণী: {row.get('drug class', '')} | ব্যবহার: {row.get('indication', '')} | ডোজ: {row.get('dosage description', '')} | পার্শ্বপ্রতিক্রিয়া: {row.get('side effects description', '')} | সতর্কতা: {row.get('precautions description', '')}"
            documents.append(doc)
            ids.append(f"gen_{row['generic id']}")
            metadatas.append({
                "source": "generics",
                "name": row['generic name'],
                "drug_class": row.get('drug class', ''),
                "indication": row.get('indication', '')
            })
        
        collections['generics'].add(ids=ids, documents=documents, metadatas=metadatas)
        del documents, ids, metadatas
        gc.collect()
    
    print(f"   ✅ Ingested {len(df)} generic records")


def run_ingestion():
    print("🚀 Starting Enhanced Ingestion Pipeline...")
    print("=" * 50)
    
    client = chromadb.PersistentClient(path=DB_PATH)
    bangla_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="shihab17/bangla-sentence-transformer"
    )
    
    collections = create_collections(client, bangla_ef)
    
    ingest_med_qa(collections)
    ingest_medicine(collections)
    ingest_generics(collections)
    
    print("\n" + "=" * 50)
    print("📊 Collection Stats:")
    for name, coll in collections.items():
        print(f"   {name}: {coll.count()} documents")
    
    print("\n✅ Ingestion Complete!")


if __name__ == "__main__":
    run_ingestion()