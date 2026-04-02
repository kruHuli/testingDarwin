#!/usr/bin/env python3
import json
import random
from src.darwinian_bs_translator.swarm_system import SwarmSystem
from src.darwinian_bs_translator.evaluator import TranslationEvaluator
from src.darwinian_bs_translator.translator import BSEmailTranslator
from src.darwinian_bs_translator.mutator import OrganismMutator
from src.darwinian_bs_translator.ensemble import EmailRouter, EnsembleTranslator

# Load system
evaluator = TranslationEvaluator()
translator = BSEmailTranslator()
mutator = OrganismMutator()

swarm_system = SwarmSystem(evaluator, translator, mutator)
swarm_system.load('evolved_swarms.json')

router = EmailRouter(swarm_system)
ensemble = EnsembleTranslator(swarm_system, translator, router)

# Load test emails
with open('emails.json', 'r') as f:
    data = json.load(f)
    emails = data['corporate_email_training_data_21_100']

# Test 3 random samples
random.seed(42)
samples = random.sample(emails, 3)

for i, email in enumerate(samples, 1):
    print(f'\n{"="*70}')
    print(f'EMAIL {i}/{len(samples)}')
    print("="*70)
    print(f'Subject: {email["subject"]}')
    print(f'Sender: {email["sender"]} ({email.get("sender_level", "unknown")})')
    print(f'\n📧 ORIGINAL EMAIL:')
    print(email['body'][:200] + '...' if len(email['body']) > 200 else email['body'])
    print(f'\n🎯 GROUND TRUTH (what they really want):')
    print(email.get('what_the_sender_really_wants', 'N/A'))

    result = ensemble.translate(email)
    print(f'\n🤖 AI TRANSLATION:')
    print(result['final_translation'])
    print(f'\n✨ Specialists Used: {" + ".join(result["specialists_used"])}')

print(f'\n{"="*70}')
print('SUMMARY: All translations completed successfully!')
print("="*70)
