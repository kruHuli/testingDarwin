# Personal Portfolio Website

A unique personal portfolio website with an AI-powered philosophical gate that determines which version of the site visitors experience.

## Features

### 🤔 Philosophical Question Gate
- Daily AI-generated deep questions (existential, ethical, reflective, creative)
- AI evaluation of answers based on quality (1-10) and effort (1-10)
- Dynamic routing based on response:
  - **Skip**: Professional timeline view
  - **Quality 6+**: Access granted
  - **Effort 8+**: Personality blog view

### 💼 Professional Timeline Page
- Sleek, majestic timeline with graphics
- Balanced text and visual presentation
- Highlighted awards using design best practices
- Warm and welcoming aesthetic
- Expandable timeline items for detailed information
- Skills showcase

### 🎨 Personality Blog Page
- Bold, creative design showcasing personality
- Blog with support for text, images, and videos
- **Semantic search** across all content using AI embeddings
- Achievement highlights
- Tech stack and superpowers showcase
- Modal views for expanded posts

## Tech Stack

- **Framework**: Next.js 16+ with TypeScript
- **Styling**: Tailwind CSS with custom warm color palette
- **Animations**: Framer Motion
- **AI**: Anthropic Claude API for question generation and answer evaluation
- **Semantic Search**: Xenova Transformers (all-MiniLM-L6-v2)
- **Deployment**: Ready for Vercel, Netlify, or any Node.js host

## Getting Started

### Prerequisites

- Node.js 20.x or higher
- npm or yarn
- Anthropic API key

### Installation

1. Clone the repository:
```bash
cd personal-website
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file:
```bash
cp .env.local.example .env.local
```

4. Add your Anthropic API key to `.env.local`:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the site.

### Build for Production

```bash
npm run build
npm start
```

## Customization

### Adding Blog Posts

Edit `/lib/blogData.ts` to add new blog posts or achievements:

```typescript
export const blogPosts: BlogPost[] = [
  {
    id: "unique-id",
    title: "Your Title",
    content: "Your content...",
    date: "YYYY-MM-DD",
    type: "text", // or "image" or "video"
    media: "optional-media-url",
    tags: ["tag1", "tag2"],
  },
  // ... more posts
];
```

### Customizing Timeline

Edit `/components/ProfessionalTimeline.tsx` to update the `timelineData` array with your experiences.

### Changing Colors

Modify the color palette in `/app/globals.css`:

```css
:root {
  --background: #faf8f5;
  --warm-beige: #e8dfd0;
  --warm-terracotta: #d4926f;
  --warm-sage: #9caf88;
  --warm-cream: #f5f1e8;
  --accent-gold: #c9a961;
}
```

## How It Works

### The Gate System

1. User visits the site
2. AI generates a daily philosophical question (same question for everyone on a given day)
3. User can either:
   - **Skip** → See professional timeline
   - **Answer** → AI evaluates the response

### AI Evaluation

The evaluation system rates answers on two dimensions:
- **Quality** (1-10): How thoughtful and insightful
- **Effort** (1-10): How much effort was put in

Rules:
- Quality ≥ 6 AND Effort ≥ 8 → Personality blog
- Otherwise → Professional timeline

### Semantic Search

The personality blog includes semantic search powered by transformer embeddings:
- Searches across blog posts AND achievements
- Uses cosine similarity to find relevant content
- Results ranked by relevance score

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

Add your `ANTHROPIC_API_KEY` in the Vercel dashboard under Environment Variables.

### Netlify

1. Connect your repository
2. Build command: `npm run build`
3. Publish directory: `.next`
4. Add `ANTHROPIC_API_KEY` in Environment Variables

## License

MIT

## Author

Built with Claude Code and creativity.
