import Anthropic from "@anthropic-ai/sdk";
import { NextRequest, NextResponse } from "next/server";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    const { question, answer } = await request.json();

    if (!answer || answer.trim().length === 0) {
      return NextResponse.json({
        quality: 0,
        effort: 0,
        showPersonality: false,
      });
    }

    const message = await client.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: `You are evaluating a user's answer to a philosophical question.

Question: "${question}"

User's Answer: "${answer}"

Rate the answer on two dimensions (1-10):

1. QUALITY (1-10): How thoughtful, coherent, and insightful is the answer?
   - 1-3: Minimal thought, generic, or nonsensical
   - 4-5: Basic attempt but superficial
   - 6-7: Demonstrates genuine reflection and perspective
   - 8-9: Deep, nuanced, and well-articulated
   - 10: Exceptional insight and originality

2. EFFORT (1-10): How much effort did the person put into their response?
   - 1-3: One word, joke, or dismissive response
   - 4-5: Brief but sincere attempt
   - 6-7: Reasonable length and consideration
   - 8-9: Substantial thought and elaboration
   - 10: Extensive, detailed, multi-faceted response

Return your evaluation in this exact JSON format:
{
  "quality": <number 1-10>,
  "effort": <number 1-10>,
  "reasoning": "<brief explanation>"
}`,
        },
      ],
    });

    const responseText =
      message.content[0].type === "text" ? message.content[0].text : "";

    // Extract JSON from response
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error("Failed to parse evaluation");
    }

    const evaluation = JSON.parse(jsonMatch[0]);
    const showPersonality = evaluation.quality >= 6 && evaluation.effort >= 8;

    return NextResponse.json({
      quality: evaluation.quality,
      effort: evaluation.effort,
      reasoning: evaluation.reasoning,
      showPersonality,
    });
  } catch (error) {
    console.error("Error evaluating answer:", error);
    return NextResponse.json(
      { error: "Failed to evaluate answer" },
      { status: 500 }
    );
  }
}
