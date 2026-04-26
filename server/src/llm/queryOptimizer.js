import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

/**
 * Extracts medical symptoms and entities from user queries to improve retrieval.
 * This acts as the "Thinker" component in the Agentic RAG system.
 */
export const optimizeMedicalQuery = async (userQuery) => {
    try {
        const response = await axios.post(
            "https://api.groq.com/openai/v1/chat/completions",
            {
                model: "llama3-8b-8192", // Fast model for extraction
                messages: [
                    {
                        role: "system",
                        content: `Extract ONLY the medical symptoms, body parts, and diseases from the user's query in both Bangla and English. 
                        Format: "Symptom1, Symptom2, Disease". 
                        If the query is purely social (e.g., "Hi", "How are you"), return "GENERAL".`
                    },
                    { 
                        role: "user", 
                        content: userQuery 
                    }
                ],
                temperature: 0
            },
            { 
                headers: { 
                    Authorization: `Bearer ${process.env.GROQ_API_KEY}`,
                    "Content-Type": "application/json"
                } 
            }
        );

        return response.data.choices[0].message.content;
    } catch (error) {
        console.error("Query Optimizer Error:", error.response?.data || error.message);
        return userQuery; // Fallback to original query if LLM fails
    }
};
