#!/usr/bin/env python3
"""Debug routing for David's email."""

import json
from src.darwinian_bs_translator.swarm_system import SwarmSystem
from src.darwinian_bs_translator.evaluator import TranslationEvaluator
from src.darwinian_bs_translator.translator import BSEmailTranslator
from src.darwinian_bs_translator.mutator import OrganismMutator
from src.darwinian_bs_translator.ensemble import EmailRouter

# Load swarms
evaluator = TranslationEvaluator()
translator = BSEmailTranslator()
mutator = OrganismMutator()

swarm_system = SwarmSystem(evaluator, translator, mutator)
swarm_system.load('evolved_swarms.json')

# Load David's email
with open('david_email.json', 'r') as f:
    email = json.load(f)

# Create router
router = EmailRouter(swarm_system)

# Test routing
print("ROUTING DEBUG:")
print("="*60)

# Get all scores first
all_scores = []
for specialist_type, swarm in swarm_system.swarms.items():
    best_organism = swarm.get_best()
    detection_score = best_organism.get_detection_score(email['body'], email['subject'])
    all_scores.append((specialist_type, best_organism, detection_score))
    print(f"{specialist_type:30s} score: {detection_score*100:5.1f}%")

all_scores.sort(key=lambda x: x[2], reverse=True)

print("\n" + "="*60)
print("SORTED SCORES:")
for spec_type, org, score in all_scores:
    print(f"{spec_type:30s} {score*100:5.1f}%")

print("\n" + "="*60)
print("ROUTER OUTPUT:")
specialists = router.route(email, threshold=0.01, min_specialists=3, max_specialists=5)
for spec_type, org, score in specialists:
    print(f"{spec_type:30s} {score*100:5.1f}%")

print(f"\nTotal activated: {len(specialists)}")
