export interface IDevPulseSource {
  id: string;
  type: 'github_repo' | 'rss_blog' | 'docs';
  url: string;
  lastScrapedAt: Date;
}

export interface IDevPulseContent {
  sourceId: string;
  title: string;
  content: string; // The raw text
  url: string;
  tags: string[];
  metadata: Record<string, any>;
  embeddingId?: string; // Reference to Qdrant ID
}