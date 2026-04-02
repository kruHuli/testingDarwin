#!/bin/bash
echo "=== DIAGNOSTIC SCRIPT ==="
echo "Working directory: $(pwd)"
echo ""
echo "evolved_swarms.json info:"
ls -lh evolved_swarms.json 2>&1
echo ""
echo "File hash:"
md5sum evolved_swarms.json 2>&1
echo ""
echo "Python location:"
which python
echo ""
echo "Pydantic test:"
python -c "import pydantic_core; print('✅ pydantic_core works')" 2>&1
echo ""
echo "Testing urgency detection:"
python3 << 'PYEOF'
import json
from src.darwinian_bs_translator.organism import TranslationOrganism

with open('evolved_swarms.json', 'r') as f:
    data = json.load(f)

best_org = TranslationOrganism.from_dict(data['swarms']['urgency_manipulator']['best_organism'])

with open('david_email.json', 'r') as f:
    email = json.load(f)

score = best_org.get_detection_score(email['body'], email['subject'])
print(f"Urgency score: {score*100:.1f}%")

for p in best_org.detection_patterns:
    if p.manipulation_type == 'fake_urgency':
        print(f"Trigger phrases: {len(p.trigger_phrases)}")
        if 'follow up' in p.trigger_phrases:
            print("✅ Has 'follow up'")
        else:
            print("❌ Missing 'follow up'")
PYEOF
