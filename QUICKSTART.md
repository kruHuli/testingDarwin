# Quick Start Guide

Get up and running with the Corporate BS Email Translator in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))
- 10-15 minutes for initial training

## Installation

```bash
# 1. Clone or download this repository
cd corporate-bs-translator

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Validate Installation

```bash
# Run validation tests (no API key needed)
python test_system.py
```

You should see:
```
✓ ALL TESTS PASSED!
```

## Train the System

First time setup requires training the evolutionary swarms:

```bash
# Quick training (5 generations, ~5 minutes, $2-3 in API costs)
python bs_translator.py train --generations 5

# Recommended training (10 generations, ~10 minutes, $5-7 in API costs)
python bs_translator.py train --generations 10

# High-quality training (15 generations, parallel, ~8 minutes, $10-15 in API costs)
python bs_translator.py train --generations 15 --parallel
```

Training output:
```
============================================================
EVOLVING ALL SWARMS
Training emails: 80
Generations: 10
============================================================

Evolving urgency_manipulator specialist
Generation 1/10
  Best fitness: 6.23
  Avg fitness: 4.87

...

Generation 10/10
  Best fitness: 8.67
  Avg fitness: 7.45

Evolution complete!

============================================================
EVOLUTION COMPLETE - Final Results:
============================================================
urgency_manipulator               Best Fitness: 8.67
flattery_manipulator             Best Fitness: 8.34
scope_creep                      Best Fitness: 8.91
responsibility_dodging           Best Fitness: 7.89
visibility_manipulation          Best Fitness: 8.23
============================================================

Swarms saved to evolved_swarms.json
```

## Test the System

```bash
# Test on 5 sample emails
python bs_translator.py test

# Test on more samples
python bs_translator.py test --num-samples 10
```

Example test output:
```
============================================================
TEST EMAIL 1/5
============================================================

ORIGINAL EMAIL:
Subject: Quick favor?
From: sarah_manager (boss)

Body:
Hey! Could you put together a quick analysis of our Q4 performance
metrics? Nothing fancy - just key insights, trend analysis, competitive
benchmarking, and recommendations. Leadership meeting tomorrow at 9 AM
so would need this by tonight.

GROUND TRUTH:
Manager wants 8 hours of work with 12 hours notice due to poor planning

============================================================
TRANSLATION:
Manager wants 6-8 hours of detailed analysis work with 12 hours notice
because of their poor planning. Using fake urgency ('leadership meeting'),
scope creep ('quick' but 4 deliverables), to pressure you into working late.

Specialists used: scope_creep, urgency_manipulator
```

## Translate Your Own Emails

### Interactive Mode

```bash
python bs_translator.py translate
```

Then enter your email details when prompted.

### From File

Create a JSON file with your email:

```json
{
  "subject": "URGENT: Need your help",
  "sender": "boss",
  "sender_level": "boss",
  "body": "Your email text here..."
}
```

Translate it:
```bash
python bs_translator.py translate --email-file my_email.json
```

## Common Use Cases

### 1. Before Responding to Requests

```bash
# Copy suspicious email to suspicious_email.json
python bs_translator.py translate --email-file suspicious_email.json
# Read the translation
# Craft appropriate response based on real intent
```

### 2. Weekly Email Analysis

```bash
# Collect week's emails in weekly_emails.json
python bs_translator.py test --test-data weekly_emails.json --num-samples 20
# Review patterns in manipulation tactics
```

### 3. Training Others

```bash
# Show colleagues examples
python bs_translator.py test --num-samples 10 > examples.txt
# Discuss translation accuracy and tactics
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'anthropic'"

Solution:
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### "Error: ANTHROPIC_API_KEY not found"

Solution:
```bash
# Make sure .env file exists and contains:
ANTHROPIC_API_KEY=your_actual_key_here
```

### "Evolution is very slow"

Solutions:
- Use `--parallel` flag for parallel evolution (faster, more API usage)
- Reduce `--generations` for faster training
- Reduce `--population-size` for fewer organisms per generation

### "Poor translation quality"

Solutions:
- Train longer: `--generations 15` or `--generations 20`
- Increase population: `--population-size 15`
- Add more training data to `emails.json`
- Retrain from scratch

## Understanding the Output

### Fitness Scores

- **8.5+**: Excellent - catches manipulation clearly
- **7.0-8.5**: Good - identifies most tactics
- **5.0-7.0**: Fair - misses some nuances
- **<5.0**: Poor - needs more training

### Specialist Activation

Multiple specialists can activate on one email:
- **detection > 0.7**: Strong match
- **detection 0.4-0.7**: Moderate match
- **detection < 0.4**: Weak match

### Translation Quality

Good translations should:
1. Expose real intent ("wants you to do X")
2. Identify manipulation tactics used
3. Estimate actual work/time required
4. Call out whose fault the situation is

## Cost Estimates

Training costs (approximate):
- 5 generations: $2-3
- 10 generations: $5-7
- 15 generations: $8-12
- 20 generations: $12-18

Per-translation costs:
- ~$0.01-0.02 per email (negligible)

## Next Steps

1. ✅ Run validation tests
2. ✅ Train the system (10 generations recommended)
3. ✅ Test on sample emails
4. ✅ Translate your own emails
5. 📖 Read [EXAMPLES.md](EXAMPLES.md) for detailed examples
6. 📖 Read [README.md](README.md) for full documentation
7. 🔧 Customize organisms in `initial_population.py`
8. 🧪 Experiment with different evolution parameters

## Getting Help

Check these files:
- `README.md` - Full system documentation
- `EXAMPLES.md` - Detailed translation examples
- `test_system.py` - System validation
- Issue tracker - Report bugs or request features

## Tips for Best Results

1. **More training = better results**: 15+ generations for production use
2. **Test regularly**: Check translation quality on known emails
3. **Add training data**: More examples = better learning
4. **Understand patterns**: Review `initial_population.py` to see what it detects
5. **Iterate**: Retrain when you find new BS tactics

---

Happy BS detecting! 🎯
