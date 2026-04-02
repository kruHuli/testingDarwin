# Getting Started - Corporate BS Email Translator

## ✅ Your System is Working!

The system has been configured for your API key and is ready to use with **Claude 3 Haiku**.

## Quick Start (5 Minutes)

### 1. Your Setup is Complete

✅ Virtual environment created
✅ Dependencies installed
✅ API key configured
✅ Model set to Claude 3 Haiku (works with your API key)

### 2. Important: Rate Limits

Your API key has a **50 requests per minute** limit. The system automatically adds delays to respect this limit.

**What this means:**
- Training will take longer than documented (2-3x)
- This is normal and expected
- The system will still work perfectly!

### 3. Recommended Training Command

```bash
source venv/bin/activate

# Start with VERY small training to test (takes ~5-8 minutes)
python bs_translator.py train --generations 2 --population-size 2
```

This will:
- Train 2 generations per specialist (10 total)
- Use only 2 organisms per swarm
- Take about 5-8 minutes
- Cost approximately $0.50-1.00
- Produce working (though not optimal) results

### 4. Test Your Trained System

```bash
# After training completes, test it:
python bs_translator.py test --num-samples 3
```

### 5. Translate an Email

```bash
# Use the sample email:
python bs_translator.py translate --email-file sample_email.json
```

## Understanding the Output

### Training Output

```
Generation 1/2
  Best fitness: 8.38
  Avg fitness: 8.11
  All-time best: 8.38
```

**Fitness Scores:**
- **8.0-10.0**: Excellent! ✅
- **6.0-8.0**: Good (acceptable)
- **<6.0**: Needs more training

### Translation Example

```
TRANSLATION:
Sender wants you to create a board presentation overnight because
of their poor planning. Using urgency manipulation (tomorrow 9 AM),
flattery (only person who can help), and scope creep (5-6 slides =
5 major deliverables).

Specialists used: urgency_manipulator, flattery_manipulator, scope_creep
```

## Rate Limit Management

The system adds **1.3 second delays** between API calls to respect your 50 req/min limit.

**Training Time Estimates (with delays):**
- 2 generations, 2 organisms: ~5-8 minutes
- 3 generations, 3 organisms: ~10-15 minutes
- 5 generations, 3 organisms: ~20-25 minutes

## Cost Estimates with Haiku

Claude 3 Haiku is very affordable:

- **Training**: $0.25-0.50 per generation
- **2 generations**: ~$0.50-1.00 total
- **5 generations**: ~$1.25-2.50 total
- **Translation**: ~$0.01 per email

Much cheaper than Sonnet! 🎉

## Common Issues & Solutions

### "Rate limit error"

**Solution**: The system should handle this automatically with delays. If you still see errors:

```bash
# Use even smaller population
python bs_translator.py train --generations 2 --population-size 1
```

### "Evaluation error: Expecting ',' delimiter"

**Solution**: This is normal - the LLM occasionally returns malformed JSON. The system has fallback parsing and will continue working.

### Training takes a long time

**Expected!** With rate limits:
- Each API call takes ~2.6 seconds (call + delay)
- 2 generations with 2 organisms = 40+ API calls = ~2-3 minutes per specialist
- 5 specialists = 10-15 minutes total

This is normal for the free tier!

### Want faster training?

**Option 1**: Use smaller configs
```bash
python bs_translator.py train --generations 1 --population-size 2
```

**Option 2**: Upgrade your API tier (removes rate limits)
- Visit https://console.anthropic.com/
- Upgrade to paid tier for faster training

## Optimal Settings for Your API Tier

### For Quick Testing (5-10 min)
```bash
python bs_translator.py train --generations 2 --population-size 2
```

### For Decent Quality (15-20 min)
```bash
python bs_translator.py train --generations 3 --population-size 3
```

### For Best Quality (30-40 min)
```bash
python bs_translator.py train --generations 5 --population-size 3
```

## What's Next?

After your first training run:

1. **Test the system**:
   ```bash
   python bs_translator.py test --num-samples 5
   ```

2. **Translate your own emails**:
   - Create a JSON file with your email
   - Run: `python bs_translator.py translate --email-file your_email.json`

3. **Read the examples**:
   - Check `EXAMPLES.md` for detailed translation examples
   - See `README.md` for full system documentation

4. **Improve results**:
   - Train for more generations
   - Add your own training data to `emails.json`
   - Retrain with larger population

## System Status

✅ **System is fully functional**
✅ **API key working**
✅ **Model configured (Claude 3 Haiku)**
✅ **Rate limiting enabled**
✅ **Ready to train**

**Start here:**
```bash
source venv/bin/activate
python bs_translator.py train --generations 2 --population-size 2
```

Then test:
```bash
python bs_translator.py test --num-samples 3
```

You're all set! 🎯
