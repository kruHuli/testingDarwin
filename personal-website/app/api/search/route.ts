import { NextRequest, NextResponse } from "next/server";
import { pipeline } from "@xenova/transformers";
import { allContent } from "@/lib/blogData";

// Simple in-memory cache for the model
let embedder: any = null;

async function getEmbedder() {
  if (!embedder) {
    embedder = await pipeline(
      "feature-extraction",
      "Xenova/all-MiniLM-L6-v2"
    );
  }
  return embedder;
}

function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json();

    if (!query || query.trim().length === 0) {
      return NextResponse.json({ results: allContent });
    }

    const model = await getEmbedder();

    // Get query embedding
    const queryEmbedding = await model(query, {
      pooling: "mean",
      normalize: true,
    });

    // Get embeddings for all content
    const contentWithScores = await Promise.all(
      allContent.map(async (item) => {
        const text = `${item.title} ${item.content} ${item.tags.join(" ")}`;
        const embedding = await model(text, {
          pooling: "mean",
          normalize: true,
        });

        const similarity = cosineSimilarity(
          Array.from(queryEmbedding.data),
          Array.from(embedding.data)
        );

        return {
          ...item,
          score: similarity,
        };
      })
    );

    // Sort by similarity score
    const results = contentWithScores
      .sort((a, b) => b.score - a.score)
      .filter((item) => item.score > 0.3); // Threshold for relevance

    return NextResponse.json({ results });
  } catch (error) {
    console.error("Search error:", error);
    return NextResponse.json(
      { error: "Search failed", results: allContent },
      { status: 500 }
    );
  }
}
