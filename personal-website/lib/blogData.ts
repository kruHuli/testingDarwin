export interface BlogPost {
  id: string;
  title: string;
  content: string;
  date: string;
  type: "text" | "image" | "video";
  media?: string;
  tags: string[];
}

export const blogPosts: BlogPost[] = [
  {
    id: "welcome",
    title: "Welcome to My World",
    content: `Hey there! If you're reading this, you put in the effort to answer that question. That means something to me. This is the real me - not just the polished resume version.

This space is where I share thoughts, projects, and ideas that excite me. Sometimes it's technical deep-dives, sometimes it's random musings, sometimes it's just cool stuff I'm working on.

Thanks for being curious enough to get here.`,
    date: "2026-03-30",
    type: "text",
    tags: ["welcome", "personal"],
  },
  {
    id: "why-ai",
    title: "Why I'm Obsessed with AI",
    content: `Everyone talks about AI like it's magic or the end of the world. But here's what gets me excited: AI is the ultimate translator between human intention and machine execution.

I've spent years translating - complex rule systems for 100+ referees, technical requirements into workflows, customer pain points into product features. AI takes that translation challenge and turns it up to 11.

When I built Receipted, converting messy user stories into structured skill profiles, it hit me: we're teaching machines to understand context the way humans do. That's not just cool tech - that's fundamentally changing how we work and think.

The best part? We're still at the beginning.`,
    date: "2026-03-28",
    type: "text",
    tags: ["AI", "technology", "thoughts"],
  },
  {
    id: "lessons-phillies",
    title: "What the Phillies Taught Me About Data",
    content: `Leading analytics for the Phillies retail team taught me something crucial: data without context is just noise.

We had 750k+ transactions. Cool. But what mattered was understanding WHY fans buy what they buy, WHEN they're most engaged, and HOW that connects to the game experience.

The dashboards we built weren't just pretty visualizations - they told stories that ops teams could act on. That's the difference between being an analyst and being valuable.

Data storytelling > data science.`,
    date: "2026-03-25",
    type: "text",
    tags: ["data", "analytics", "lessons", "sports"],
  },
];

export const achievements: BlogPost[] = [
  {
    id: "receipted-demo",
    title: "Receipted - Live Demo at Continual Learning Hackathon SF",
    content: "Presented our AI platform that converts user stories into verifiable skill profiles. Explained the technical architecture to both technical judges and non-technical audiences.",
    date: "2026-01",
    type: "text",
    tags: ["project", "AI", "presentation"],
  },
  {
    id: "phillies-fellowship",
    title: "Fellowship Award for Outstanding Team Lead",
    content: "Recognized for leading a cross-functional analytics team that delivered actionable insights from 750k+ transactions for the Philadelphia Phillies.",
    date: "2023-12",
    type: "text",
    tags: ["award", "leadership", "analytics"],
  },
  {
    id: "rutgers-recreation-award",
    title: "Rutgers University Recreation Leadership Excellence Award",
    content: "Awarded for improving operational efficiency by 33% through process redesign and leading technical onboarding for 100+ referees.",
    date: "2023",
    type: "text",
    tags: ["award", "leadership", "operations"],
  },
];

export const allContent = [...blogPosts, ...achievements];
