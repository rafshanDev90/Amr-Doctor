import { Cerebras } from '@cerebras/cerebras_cloud_sdk';
import dotenv from 'dotenv';

dotenv.config();

// Initialize the client
const client = new Cerebras({
    apiKey: process.env.API_KEY,
});

export const getLlmResponse = async (userQuery, context) => {
    try {
        const chatCompletion = await client.chat.completions.create({
                messages: [
                    {
                        role: "system",
                        content: `You are a professional Bangladeshi Medical Assistant.
                        
                        RULES:
                        1. If the context is "EMPTY_CONTEXT", "NO_MEDICAL_CONTEXT", or "ERROR_RETRIEVING", politely say you don't have that specific medical data in your database right now.
                        2. NEVER make up medicine names, treatments, or dosages not explicitly mentioned in the provided Context.
                        3. Use "Chain of Thought": 
                           - First, identify the symptoms from the user query.
                           - Second, scan the Context for matches.
                           - Third, provide the answer in Bangla based ONLY on that context.
                        4. If the user query is about something non-medical (e.g., farming, food, sports), state that you are a medical assistant and cannot help with that.
                        5. Maintain a professional, empathetic tone.
                        
                        Context: ${context}`
                    },
                    {
                        role: "user",
                        content: `User Question: ${userQuery}`
                    }
                ],
            // Use 'llama3.1-70b' or 'llama3.1-8b' for the best free-tier results
            model: "llama3.1-8b",
        });

        return chatCompletion.choices[0].message.content;
    } catch (error) {
        console.error("Cerebras SDK Error:", error.message);
        throw error;
    }
};
