<h1 align="center">🩺 Amr-Doctor: Multilingual Medical RAG Assistant</h1>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&center=true&width=600&lines=Agentic+RAG+Pipeline;Banglish+to+Bangla+Normalizer;Medical+Emergency+Interceptor;Cerebras+LLM+Integration" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Y2ZndxeXQyZndxeXQyZndxeXQyZndxeXQyZndxeXQyZndxeXQyJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKSjPqcKGRZaO3u/giphy.gif" width="400" />
</p>

---

### 🚀 Project Summary
**Amr-Doctor** is a production-grade medical RAG (Retrieval-Augmented Generation) system engineered specifically for the Bangladeshi community. It bridges the gap between Romanized "Banglish" queries and Standard Bengali medical knowledge using an advanced agentic pipeline, ensuring high-accuracy retrieval and clinical safety.

### 🛠️ Key Technical Features
- **Banglish Normalization:** Real-time transliteration layer using Cerebras (Llama 3.1) to convert phonetic input into proper Unicode and Clinical English.
- **Agentic Retrieval:** Multi-stage cognitive process that decomposes queries into medical entities (Symptoms/Diseases) before searching.
- **Hybrid Search Architecture:** Simultaneous multi-collection querying across verified QA, Drugs, and Generic datasets with distance-based thresholding.
- **Medical Safety Interceptor:** Pre-retrieval emergency keyword scanner that triggers immediate hospital/emergency guidance for high-risk symptoms.

### 🔹 AI & LLMOps (The Core)
<p>
  <img src="https://img.shields.io/badge/Cerebras_AI-FF6B6B?style=for-the-badge&logo=ai&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-00C7B7?style=for-the-badge&logo=vector&logoColor=white" />
  <img src="https://img.shields.io/badge/Sentence_Transformers-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Agentic_RAG-9b59b6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2Zy..." />
</p>

### 🔹 Backend & Infrastructure
<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/Telegraf-26A69A?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux_VPS-FCC624?style=for-the-badge&logo=linux&logoColor=000" />
</p>

---

### 🏗️ Architecture Workflow
1. **Input Normalization:** `amr matha betha` → `আমার মাথা ব্যথা` + `Headache`.
2. **Emergency Check:** Scans for keywords like *Chest Pain, Stroke, Bleeding*.
3. **Optimized Search:** Hybrid query across `med_qa` and `generics` collections.
4. **Self-Correction:** Thresholding (Distance > 1.5) prevents low-confidence hallucinations.
5. **Generation:** Llama 3.1-70B generates empathetic, context-strict responses in professional Bangla.

### 📖 Setup & Usage
```bash
# 1. Start the RAG API (Python/FastAPI)
cd api && python app/main.py

# 2. Start the Telegram Bot (Node.js/Express)
cd server && npm run dev
```

---

<p align="center">
  <b>Developed with Clinical Precision for Bangladesh</b><br>
  <i>এটি কেবল তথ্যের জন্য। জরুরি প্রয়োজনে ডাক্তারের পরামর্শ নিন।</i>
</p>
