import mongoose, { Schema } from 'mongoose';

const ContentSchema = new Schema({
  sourceId: { type: String, required: true },
  title: { type: String, required: true },
  body: { type: String, required: true },
  url: { type: String, unique: true },
  processed: { type: Boolean, default: false }, // Useful for LLMOps retry logic
}, { timestamps: true });

export const ContentModel = mongoose.model('Content', ContentSchema);
