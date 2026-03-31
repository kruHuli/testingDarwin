# Corporate BS Email Translation System
## Using Darwinian Evolution with Specialized Expert Swarms

A revolutionary system that evolves AI agents to translate manipulative corporate emails into brutally honest plain English. Each specialist swarm independently evolves to detect specific types of BS: urgency manipulation, flattery tactics, scope creep, responsibility dodging, and career manipulation.

## Overview

This system demonstrates how evolutionary algorithms can solve real-world communication problems by:

1. **Evolving 5 specialist swarms**, each expert at detecting different manipulation tactics
2. **Using Darwinian evolution** to improve translation strategies over generations
3. **Combining LLM capabilities** with evolved pattern recognition
4. **Routing emails intelligently** to the right specialists
5. **Producing clear, honest translations** that expose the sender's true intent

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CORPORATE BS EMAIL                       │
│  "Quick question - could you do a small analysis by EOD?"   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   EMAIL ROUTER                              │
│  Detects which manipulation types are present               │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┼────────────┬────────────┐
          ▼            ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
    │Urgency  │  │Flattery │  │  Scope  │  │Visibility│
    │ Swarm   │  │  Swarm  │  │  Creep  │  │  Swarm  │
    │(Gen 10) │  │(Gen 10) │  │  Swarm  │  │(Gen 10) │
    └─────────┘  └─────────┘  │(Gen 10) │  └─────────┘
                               └─────────┘
          │            │            │            │
          └────────────┴────────────┴────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 ENSEMBLE COMBINER                           │
│   Merges specialist insights into final translation         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   TRANSLATION OUTPUT                        │
│  "Sender wants 8 hours of work done in 2 hours because of  │
│   their poor planning. Using fake urgency + scope creep."  │
└─────────────────────────────────────────────────────────────┘
```

## Specialist Swarm Types

### 1. Urgency Manipulator Translator
Detects fake deadlines, artificial urgency, and deadline pressure tactics.

**Example:**
- Input: "Need this ASAP - client meeting tomorrow!"
- Output: "Sender's poor planning created fake urgency to make their emergency your emergency"

### 2. Flattery/Ego Manipulator Translator
Catches expertise flattery, uniqueness lies, and ego stroking.

**Example:**
- Input: "You're the only one who can help with this..."
- Output: "Sender flatters your skills (lie) to get free work others could easily do"

### 3. Scope Creep Translator
Identifies work minimization and hidden scope expansion.

**Example:**
- Input: "Quick question - need budget breakdown, projections, and ROI analysis"
- Output: "Claims 'quick question' but wants 8 hours of detailed financial analysis"

### 4. Responsibility Dodging Translator
Exposes blame-shifting, authority shields, and fake sympathy.

**Example:**
- Input: "Leadership wants this, my hands are tied..."
- Output: "Hides behind vague 'leadership' to avoid taking responsibility for decision"

### 5. Visibility/Career Manipulation Translator
Reveals false promises of exposure, growth, and opportunity.

**Example:**
- Input: "Great visibility opportunity - lead this initiative!"
- Output: "Promises vague career benefits for 20 hours of unpaid work that benefits them"

## Organism Structure

Each evolved organism contains:

```python
TranslationOrganism {
    specialist_type: "urgency_manipulator"

    detection_patterns: [
        {
            trigger_phrases: ["ASAP", "urgent", "right away", "EOD"],
            context_clues: ["need this", "can't wait"],
            manipulation_type: "urgency",
            weight: 1.5
        }
    ]

    translation_templates: [
        {
            pattern_name: "urgent_with_short_notice",
            template: "Sender wants {task} done {timeframe} due to poor planning",
        }
    ]

    llm_prompt_rules: {
        system_prompt: "Expert at detecting fake urgency...",
        detection_instructions: [...],
        translation_guidelines: [...],
        focus_areas: ["urgency", "deadlines", "time pressure"]
    }

    fitness: 8.7  # Evolved score
    generation: 10
}
```

## Installation

```bash
# Clone or navigate to the repository
cd corporate-bs-translator

# Install dependencies
pip install -r requirements.txt

# Set up your Anthropic API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Quick Start

### 1. Train the System (Evolve the Swarms)

```bash
# Basic training (10 generations, sequential)
python bs_translator.py train

# Advanced training with parallel evolution
python bs_translator.py train --generations 15 --population-size 12 --parallel

# Custom training data
python bs_translator.py train --training-data my_emails.json --output my_swarms.json
```

Training takes approximately:
- Sequential mode: ~10-15 minutes for 10 generations
- Parallel mode: ~5-8 minutes for 10 generations (more API usage)

### 2. Test the System

```bash
# Test on 5 random sample emails
python bs_translator.py test

# Test on more samples
python bs_translator.py test --num-samples 10

# Test with custom swarms
python bs_translator.py test --swarms my_swarms.json
```

### 3. Translate Emails

```bash
# Interactive mode - enter email details manually
python bs_translator.py translate

# Translate from JSON file
python bs_translator.py translate --email-file sample_email.json
```

## Usage Examples

### Training Output

```
============================================================
EVOLVING ALL SWARMS
Training emails: 80
Generations: 10
Parallel: False
============================================================

============================================================
Evolving urgency_manipulator specialist
Population: 10, Generations: 10
============================================================

Generation 1/10
  Best fitness: 6.23
  Avg fitness: 4.87
  All-time best: 6.23

Generation 2/10
  Best fitness: 7.12
  Avg fitness: 5.94
  All-time best: 7.12

...

Generation 10/10
  Best fitness: 8.67
  Avg fitness: 7.45
  All-time best: 8.67

Evolution complete!
Final best fitness: 8.67

============================================================
EVOLUTION COMPLETE - Final Results:
============================================================
urgency_manipulator               Best Fitness: 8.67
flattery_manipulator             Best Fitness: 8.34
scope_creep                      Best Fitness: 8.91
responsibility_dodging           Best Fitness: 7.89
visibility_manipulation          Best Fitness: 8.23
============================================================
```

### Translation Output

```
ORIGINAL EMAIL:
Subject: Quick favor?
From: sarah_manager (boss)

Body:
Hey! Could you put together a quick analysis of our Q4 performance
metrics? Nothing fancy - just need key insights, trend analysis,
competitive benchmarking, and recommendations. Leadership meeting
tomorrow at 9 AM so would need this by tonight. You're so good at
this type of analysis!

============================================================
TRANSLATION:
Sarah wants 6-8 hours of detailed analysis work with 12 hours notice
because of her poor planning. Using fake urgency ('leadership meeting'),
scope creep ('quick' but 4 deliverables), and flattery ('you're so good')
to manipulate you into working late.

Specialists used: scope_creep, urgency_manipulator, flattery_manipulator
```

## Python API Usage

```python
from src.darwinian_bs_translator import (
    SwarmSystem, TranslationEvaluator, BSEmailTranslator,
    OrganismMutator, EmailRouter, EnsembleTranslator
)

# Initialize components
evaluator = TranslationEvaluator(api_key="your-key")
translator = BSEmailTranslator(api_key="your-key")
mutator = OrganismMutator(api_key="your-key")

# Create swarm system
swarm_system = SwarmSystem(evaluator, translator, mutator)

# Initialize and evolve swarms
swarm_system.initialize_swarms()
swarm_system.evolve_all_swarms(training_data, generations=10)

# Save evolved swarms
swarm_system.save('evolved_swarms.json')

# Later: Load and use for translation
swarm_system.load('evolved_swarms.json')
router = EmailRouter(swarm_system)
ensemble = EnsembleTranslator(swarm_system, translator, router)

# Translate an email
email = {
    'subject': 'Quick question',
    'sender': 'boss',
    'body': 'Need this ASAP...'
}
result = ensemble.translate(email)
print(result['final_translation'])
```

## Training Data Format

The system expects JSON with email objects containing:

```json
{
  "corporate_email_training_data_21_100": [
    {
      "id": 21,
      "subject": "Per my last email...",
      "sender": "derek_compliance",
      "sender_level": "peer",
      "time_sent": "8:30 AM",
      "body": "Hi, Per my last email regarding...",
      "your_gut_reaction": "Annoyed - passive aggressive",
      "actual_urgency_level": "3 - probably important but artificially urgent",
      "manipulation_tactics_you_see": "gaslighting, artificial deadline",
      "how_you_would_respond": "Ask for clarification",
      "what_the_sender_really_wants": "Cover their ass by making it look like I'm the bottleneck"
    }
  ]
}
```

The `what_the_sender_really_wants` field is used as ground truth during evolution.

## How Evolution Works

### Fitness Evaluation

Each organism is evaluated on sample emails using these criteria:

1. **Intent Exposure (40%)**: Did it reveal what sender really wants?
2. **BS Detection (30%)**: Did it catch the manipulation tactics?
3. **Clarity (20%)**: Is the translation clear and understandable?
4. **Conciseness (10%)**: Is it appropriately concise?

### Mutation Strategies

1. **Add Pattern**: Add new detection patterns for missed BS
2. **Modify Pattern**: Adjust trigger phrases and weights
3. **Adjust Weights**: Fine-tune pattern importance
4. **Update Prompts**: Improve LLM instruction quality
5. **LLM-Guided**: Analyze failures and learn new patterns

### Selection Process

1. Evaluate all organisms on training data
2. Keep top 3 organisms (elite selection)
3. Generate rest through mutation of top performers
4. Repeat for N generations

## Performance Characteristics

- **Training Time**: ~10-15 min for 10 generations (sequential mode)
- **API Calls**: ~500-1000 during training (depends on settings)
- **Translation Speed**: ~2-3 seconds per email
- **Accuracy**: Typically achieves 8.0+ fitness score after 10 generations

## Advanced Configuration

### Custom Population Size

Larger populations explore more strategies but cost more:

```bash
python bs_translator.py train --population-size 20 --generations 15
```

### Parallel Evolution

Evolves all 5 swarms simultaneously (faster, more API intensive):

```bash
python bs_translator.py train --parallel
```

### Custom Mutation Rate

Adjust in code (`evolution.py`):

```python
engine = EvolutionEngine(
    evaluator, translator, mutator,
    mutation_rate=0.5  # Higher = more exploration
)
```

## File Structure

```
corporate-bs-translator/
├── src/
│   └── darwinian_bs_translator/
│       ├── __init__.py
│       ├── __main__.py
│       ├── organism.py           # Organism data structures
│       ├── initial_population.py # Initial swarm creators
│       ├── evaluator.py          # LLM-based fitness evaluation
│       ├── translator.py         # Email translation with LLM
│       ├── mutator.py            # Organism mutation strategies
│       ├── evolution.py          # Darwinian evolution engine
│       ├── swarm_system.py       # Multi-swarm management
│       ├── ensemble.py           # Email routing & combination
│       └── cli.py                # Command-line interface
├── bs_translator.py              # Main entry point
├── emails.json                   # Training data (80 emails)
├── requirements.txt
├── .env.example
└── README.md
```

## Real-World Applications

1. **Email Inbox Assistant**: Browser extension that shows BS translation on hover
2. **Corporate Training**: Teach employees to recognize manipulation tactics
3. **Communication Analysis**: Audit company culture by analyzing email patterns
4. **Personal Defense**: Protect yourself from manipulative requests
5. **Management Tool**: Help managers understand how their emails are perceived

## Limitations

- Requires Anthropic API key (costs apply during training/use)
- Training data bias affects results
- May not catch novel manipulation tactics until retrained
- Cultural context varies (optimized for US corporate culture)

## Future Enhancements

- [ ] Multi-objective optimization (clarity vs. brevity trade-offs)
- [ ] Online learning (continuous improvement from user feedback)
- [ ] Cross-validation for better generalization
- [ ] Explanation generation (why this is BS)
- [ ] Suggested responses (how to politely decline)
- [ ] Sentiment analysis integration
- [ ] Support for other languages

## Contributing

This is a demonstration project showing how evolutionary algorithms can solve real-world problems. Feel free to:

- Add new specialist types
- Improve mutation strategies
- Enhance the ensemble combination logic
- Add more training data
- Optimize fitness functions

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built with:
- Anthropic Claude API for LLM capabilities
- Darwinian evolution principles
- Multi-agent swarm intelligence concepts
- Real corporate email patterns (anonymized)

---

**Disclaimer**: This system is for educational and defensive purposes. Use it to protect yourself from manipulation, not to manipulate others. Always communicate honestly and directly in professional settings.
