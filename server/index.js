import { Telegraf } from "telegraf";
import dotenv from "dotenv";
import { getRelevantContext } from "./src/database/vectorStore.js";
import { getLlmResponse } from "./src/llm/cerebras.services.js";

dotenv.config();

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => ctx.reply("স্বাগতম! আপনার স্বাস্থ্য বিষয়ক প্রশ্নটি এখানে লিখুন (Bangla/Banglish)."));

bot.on("text", async (ctx) => {
    const userQuery = ctx.message.text;
    
    try {
        await ctx.sendChatAction("typing");
        
        const context = await getRelevantContext(userQuery);
        const answer = await getLlmResponse(userQuery, context);
        
        await ctx.reply(answer);
    } catch (error) {
        console.error("Bot Error:", error);
        await ctx.reply("দুঃখিত, এই মুহূর্তে আমি উত্তর দিতে পারছি না। পরে চেষ্টা করুন।");
    }
});

bot.launch();
console.log("🚀 Medical Bot is running on Linux...");
