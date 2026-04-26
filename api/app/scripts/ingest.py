import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm
import os
import re

# Configuration
DATA_DIR = "data"
GENERIC_DATA = os.path.join(DATA_DIR, "generic.csv")
QA_DATA = os.path.join(DATA_DIR, "bangla-med-qa.csv")
DB_PATH = "vector_db"

def clean_html(text):
    if not isinstance(text, str):
        return ""
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # Remove extra whitespace
    text = " ".join(text.split())
    return text

def ingest_qa_data(collection):
    print("📥 Ingesting Medical Q&A data...")
    df = pd.read_csv(QA_DATA)
    
    batch_size = 100
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        
        documents = []
        ids = []
        metadatas = []
        
        for idx, row in batch.iterrows():
            # Create a rich document from Q, A and Explanation
            doc = f"প্রশ্ন: {row['question']}\nউত্তর: {row['answer']}\nব্যাখ্যা: {row['explanation']}"
            documents.append(doc)
            ids.append(f"qa_{idx}")
            metadatas.append({"source": "BanglaMedQA", "type": "qa"})
            
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

def ingest_generic_data(collection):
    print("📥 Ingesting Generic Medicine data...")
    # Using low_memory=False for larger CSVs
    df = pd.read_csv(GENERIC_DATA, low_memory=False)
    
    batch_size = 50 # Smaller batch for larger text content
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        
        documents = []
        ids = []
        metadatas = []
        
        for idx, row in batch.iterrows():
            # Clean descriptions
            indication = clean_html(row.get('indication description', ''))
            pharmacology = clean_html(row.get('pharmacology description', ''))
            side_effects = clean_html(row.get('side effects description', ''))
            
            if not indication and not pharmacology:
                continue
                
            doc = f"Medicine: {row['generic name']}\nIndication: {indication}\nPharmacology: {pharmacology}\nSide Effects: {side_effects}"
            
            documents.append(doc)
            ids.append(f"gen_{idx}")
            metadatas.append({
                "source": "MedexGenerics", 
                "generic_name": str(row['generic name']),
                "type": "medicine_info"
            })
            
        if documents:
            collection.add(ids=ids, documents=documents, metadatas=metadatas)

def run_ingestion():
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Use the multilingual model as planned in the project goal
    bangla_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="shihab17/bangla-sentence-transformer"
    )

    collection = client.get_or_create_collection(
        name="med_knowledge",
        embedding_function=bangla_ef
    )

    # Ingest QA Data
    if os.path.exists(QA_DATA):
        ingest_qa_data(collection)
    
    # Ingest Generic Data
    if os.path.exists(GENERIC_DATA):
        ingest_generic_data(collection)

    print(f"✅ Ingestion complete. Vector DB updated at {DB_PATH}")

if __name__ == "__main__":
    run_ingestion()
    