import axios from "axios";
import avro from "nodejs-avro-phonetic";
import dotenv from "dotenv";
import { optimizeMedicalQuery } from "../llm/queryOptimizer.js";

dotenv.config();

const RAG_API_URL = process.env.RAG_API_URL || "http://localhost:8000";

export const getRelevantContext = async (query) => {
    // 1. "Power Move": Use LLM to understand what to search for (Intent Extraction)
    const medicalKeywords = await optimizeMedicalQuery(query);
    
    if (medicalKeywords === "GENERAL") return "NO_MEDICAL_CONTEXT";

    // 2. Transliterate Banglish to Bangla
    const banglaQuery = avro.parse(query);
    
    // 3. Hybrid multi-query: original + transliterated + optimized keywords
    const expandedQuery = `${query} ${banglaQuery} ${medicalKeywords}`;
    
    try {
        const response = await axios.post(`${RAG_API_URL}/query`, {
            query: expandedQuery,
            n_results: 5 // Higher coverage for better RAG
        });

        // 4. Self-Correction: Return explicit flag if no context found
        return response.data.context || "EMPTY_CONTEXT";
    } catch (error) {
        console.error("VectorStore Error:", error.response?.data || error.message);
        return "ERROR_RETRIEVING";
    }
};
