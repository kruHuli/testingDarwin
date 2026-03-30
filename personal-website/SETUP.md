# Quick Setup Guide

## Prerequisites
- Node.js 20.x or higher installed
- An Anthropic API key (get one at https://console.anthropic.com/)

## Step-by-Step Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment Variables
```bash
# Copy the example file
cp .env.local.example .env.local

# Edit .env.local and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### 3. Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Test the Website

#### Testing the Question Gate
1. Visit the homepage
2. You'll see a philosophical question
3. Try both paths:
   - Click "Skip" → See the professional timeline
   - Write a thoughtful, detailed answer → See the personality blog

#### Testing Semantic Search
1. Answer the question with high quality and effort
2. Once in the personality blog, use the search bar
3. Try searches like:
   - "AI and technology"
   - "leadership"
   - "data analytics"
   - "Phillies"

### 5. Customize Your Content

#### Update Resume/Timeline Data
Edit `/components/ProfessionalTimeline.tsx`:
- Find the `timelineData` array
- Replace with your own experiences
- Update the skills section

#### Add Blog Posts
Edit `/lib/blogData.ts`:
- Add entries to `blogPosts` array
- Add entries to `achievements` array
- Include your own thoughts and experiences

#### Change Colors
Edit `/app/globals.css`:
- Modify the CSS variables in `:root`
- Adjust warm-beige, warm-terracotta, warm-sage, etc.

### 6. Build for Production
```bash
npm run build
npm start
```

## Deployment

### Deploy to Vercel (Easiest)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts
4. Add `ANTHROPIC_API_KEY` in Vercel dashboard

### Deploy to Netlify
1. Connect your Git repository
2. Build command: `npm run build`
3. Publish directory: `.next`
4. Add `ANTHROPIC_API_KEY` environment variable

## Troubleshooting

### Build Fails
- Make sure Node.js version is 20.x or higher: `node -v`
- Delete `node_modules` and `.next`, then run `npm install` again
- Check that `ANTHROPIC_API_KEY` is set correctly

### Question Gate Not Working
- Verify `ANTHROPIC_API_KEY` is set in `.env.local`
- Check browser console for errors
- Make sure the API key has sufficient credits

### Semantic Search Not Working
- First search might be slow (model loading)
- Check browser console for errors
- Verify transformers package is installed: `npm list @xenova/transformers`

## Features Overview

### The Gate System
- **Skip**: Shows professional timeline (warm, welcoming design)
- **Answer with quality ≥6 AND effort ≥8**: Shows personality blog (bold, creative design)

### Professional Timeline
- Interactive timeline with expandable items
- Awards highlighted with special styling
- Skills showcase
- Warm color palette

### Personality Blog
- Semantic search across all content
- Blog posts and achievements
- Modal views for expanded reading
- Bold, creative design

## Next Steps

1. **Get an Anthropic API Key**: Visit https://console.anthropic.com/
2. **Customize the Content**: Replace placeholder content with your own
3. **Adjust the Design**: Tweak colors and styling to match your brand
4. **Deploy**: Share your unique portfolio with the world!

Need help? Check the main README.md for more detailed documentation.
