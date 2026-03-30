import Anthropic from "@anthropic-ai/sdk";
import { NextResponse } from "next/server";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function GET() {
  try {
    // Generate a daily question based on the current date
    const today = new Date().toISOString().split("T")[0];

    const message = await client.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: `Generate a single thought-provoking philosophical or deep question that challenges perspective.
          The question should be:
          - Existential, ethical, reflective, creative, or imaginative
          - Open-ended and meaningful
          - Something that makes people think deeply
          - Not too abstract or academic
          - Engaging and accessible

          Date seed: ${today}

          Return ONLY the question, nothing else.`,
        },
      ],
    });

    const question =
      message.content[0].type === "text" ? message.content[0].text : "";

    return NextResponse.json({ question });
  } catch (error) {
    console.error("Error generating question:", error);
    return NextResponse.json(
      { error: "Failed to generate question" },
      { status: 500 }
    );
  }
}
