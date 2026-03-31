"""
Mutator that improves organisms based on failed translations.
"""

import random
import copy
import os
from typing import Dict, Any, List
from anthropic import Anthropic
from .organism import TranslationOrganism, DetectionPattern, TranslationTemplate


class OrganismMutator:
    """
    Mutates organisms to improve their translation strategies.

    Uses LLM to analyze failures and suggest improvements.
    """

    def __init__(self, api_key: str = None, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def mutate(
        self,
        organism: TranslationOrganism,
        failed_translations: List[Dict[str, Any]] = None,
        mutation_rate: float = 0.3
    ) -> TranslationOrganism:
        """
        Create a mutated version of the organism.

        Args:
            organism: Organism to mutate
            failed_translations: List of failed translation examples
            mutation_rate: Probability of mutation (0.0 to 1.0)

        Returns:
            Mutated organism
        """
        if random.random() > mutation_rate:
            return organism.clone()

        mutated = organism.clone()

        # Choose mutation type
        mutation_types = ['add_pattern', 'modify_pattern', 'adjust_weights', 'update_prompts']

        if failed_translations and len(failed_translations) > 0:
            # If we have failed examples, use LLM-guided mutation
            mutation_types.append('llm_guided')

        mutation_type = random.choice(mutation_types)

        if mutation_type == 'add_pattern':
            self._add_detection_pattern(mutated)
        elif mutation_type == 'modify_pattern':
            self._modify_pattern(mutated)
        elif mutation_type == 'adjust_weights':
            self._adjust_weights(mutated)
        elif mutation_type == 'update_prompts':
            self._update_prompts(mutated)
        elif mutation_type == 'llm_guided':
            self._llm_guided_mutation(mutated, failed_translations)

        return mutated

    def _add_detection_pattern(self, organism: TranslationOrganism):
        """Add a new detection pattern."""
        # Common BS phrases that could be added
        new_phrases_by_type = {
            'urgency_manipulator': ['critical path', 'blocking issue', 'needs attention', 'drop everything'],
            'flattery_manipulator': ['nobody does it like you', 'natural talent', 'gift for'],
            'scope_creep': ['one more thing', 'forgot to mention', 'oh and also'],
            'responsibility_dodging': ['out of my hands', 'just the messenger', 'orders from up top'],
            'visibility_manipulation': ['resume builder', 'portfolio piece', 'showcase opportunity']
        }

        phrases = new_phrases_by_type.get(organism.specialist_type, ['please', 'need', 'help'])

        new_pattern = DetectionPattern(
            trigger_phrases=random.sample(phrases, min(3, len(phrases))),
            context_clues=['could you', 'would you', 'need your'],
            manipulation_type=f"{organism.specialist_type}_variant",
            weight=random.uniform(1.0, 1.5)
        )

        organism.detection_patterns.append(new_pattern)

    def _modify_pattern(self, organism: TranslationOrganism):
        """Modify an existing pattern."""
        if not organism.detection_patterns:
            return

        pattern = random.choice(organism.detection_patterns)

        # Add a new trigger phrase
        if random.random() < 0.5:
            new_phrase = random.choice([
                'at your earliest convenience', 'when you get a chance',
                'no pressure', 'just checking in', 'wanted to touch base'
            ])
            pattern.trigger_phrases.append(new_phrase)
        else:
            # Adjust weight
            pattern.weight *= random.uniform(0.8, 1.2)

    def _adjust_weights(self, organism: TranslationOrganism):
        """Adjust pattern weights."""
        for pattern in organism.detection_patterns:
            pattern.weight *= random.uniform(0.9, 1.1)

    def _update_prompts(self, organism: TranslationOrganism):
        """Update LLM prompt rules."""
        if not organism.llm_prompt_rules:
            return

        # Add a new detection instruction
        new_instructions = [
            "Watch for time pressure tactics",
            "Notice qualification or ego-stroking language",
            "Identify work being framed as opportunities",
            "Catch passive-aggressive language",
            "Look for responsibility avoidance"
        ]

        if random.random() < 0.5:
            organism.llm_prompt_rules.detection_instructions.append(
                random.choice(new_instructions)
            )

    def _llm_guided_mutation(
        self,
        organism: TranslationOrganism,
        failed_translations: List[Dict[str, Any]]
    ):
        """Use LLM to suggest improvements based on failures."""
        if not failed_translations:
            return

        # Take up to 3 failed examples
        examples = failed_translations[:3]

        prompt = f"""You are improving a corporate BS detection system.

SPECIALIST TYPE: {organism.specialist_type}

CURRENT DETECTION PATTERNS:
{self._format_patterns(organism.detection_patterns)}

FAILED TRANSLATIONS (these translations scored poorly):
"""

        for i, failure in enumerate(examples, 1):
            prompt += f"\nExample {i}:\n"
            prompt += f"Email: {failure.get('email_subject', '')} - {failure.get('email_body', '')[:200]}...\n"
            prompt += f"Translation produced: {failure.get('translation', '')}\n"
            prompt += f"Why it failed: {failure.get('feedback', '')}\n"
            prompt += f"Missed: {', '.join(failure.get('missed_manipulations', []))}\n"

        prompt += f"""

Based on these failures, suggest 2-3 NEW trigger phrases that should be added to detect {organism.specialist_type} manipulation better.

Respond with ONLY a JSON array of strings:
["phrase1", "phrase2", "phrase3"]"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=256,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text.strip()

            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            import json
            new_phrases = json.loads(result_text)

            # Add new pattern with suggested phrases
            if new_phrases and isinstance(new_phrases, list):
                new_pattern = DetectionPattern(
                    trigger_phrases=new_phrases,
                    context_clues=['need', 'want', 'help'],
                    manipulation_type=f"{organism.specialist_type}_learned",
                    weight=1.5
                )
                organism.detection_patterns.append(new_pattern)

        except Exception as e:
            # Fallback to simple mutation if LLM fails
            self._add_detection_pattern(organism)

    def _format_patterns(self, patterns: List[DetectionPattern]) -> str:
        """Format patterns for display."""
        if not patterns:
            return "None"

        result = ""
        for pattern in patterns[:5]:  # Show top 5
            result += f"- {pattern.manipulation_type}: {', '.join(pattern.trigger_phrases[:3])}\n"
        return result
