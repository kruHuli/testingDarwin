"""
LLM-based evaluator for translation quality.

Uses Claude to judge how well a translation exposes corporate BS and manipulation.
"""

import os
import json
from typing import Dict, Any, Optional
from anthropic import Anthropic


class TranslationEvaluator:
    """
    Evaluates translation quality using LLM judgment.

    Scores translations on:
    - Clarity (1-10): How clear is the translation?
    - BS Detection (1-10): Did it catch the corporate jargon?
    - Intent Exposure (1-10): Did it reveal the real intent/manipulation?
    - Conciseness (1-10): Is it concise or overly verbose?
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def evaluate_translation(
        self,
        original_email: Dict[str, Any],
        translation: str,
        specialist_type: str
    ) -> Dict[str, float]:
        """
        Evaluate a translation and return scores.

        Args:
            original_email: The original email data
            translation: The translated/decoded version
            specialist_type: Type of specialist that made the translation

        Returns:
            Dictionary with scores and feedback
        """
        email_body = original_email.get('body', '')
        email_subject = original_email.get('subject', '')
        ground_truth = original_email.get('what_the_sender_really_wants', '')

        prompt = f"""You are evaluating a corporate email translation system that converts manipulative corporate-speak into plain English.

SPECIALIST TYPE: {specialist_type}

ORIGINAL EMAIL:
Subject: {email_subject}
Body: {email_body}

GROUND TRUTH (what sender really wants): {ground_truth}

TRANSLATION PRODUCED:
{translation}

Please evaluate this translation on the following criteria (1-10 scale):

1. CLARITY: Is the translation clear and easy to understand?
   - 10 = Crystal clear, anyone would understand
   - 5 = Somewhat clear but could be better
   - 1 = Confusing or unclear

2. BS_DETECTION: Did it successfully identify and remove corporate jargon/manipulation?
   - 10 = Caught all the BS and manipulation tactics
   - 5 = Caught some but missed important parts
   - 1 = Missed most of the manipulation

3. INTENT_EXPOSURE: Did it reveal what the sender REALLY wants?
   - 10 = Perfectly exposes true intent, matches ground truth
   - 5 = Partially exposes intent
   - 1 = Doesn't expose the real agenda

4. CONCISENESS: Is the translation appropriately concise?
   - 10 = Perfectly concise, no wasted words
   - 5 = Somewhat verbose but acceptable
   - 1 = Way too long or verbose

Respond ONLY with valid JSON in this exact format:
{{
    "clarity_score": <1-10>,
    "bs_detection_score": <1-10>,
    "intent_exposure_score": <1-10>,
    "conciseness_score": <1-10>,
    "overall_score": <average of above>,
    "feedback": "<brief explanation of scores>",
    "missed_manipulations": ["<list any manipulation tactics that were missed>"],
    "improvements": ["<specific suggestions for improvement>"]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text.strip()

            # Extract JSON if it's wrapped in markdown
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            result = json.loads(result_text)
            return result

        except Exception as e:
            print(f"Evaluation error: {e}")
            # Return default low scores on error
            return {
                'clarity_score': 1.0,
                'bs_detection_score': 1.0,
                'intent_exposure_score': 1.0,
                'conciseness_score': 1.0,
                'overall_score': 1.0,
                'feedback': f'Error during evaluation: {str(e)}',
                'missed_manipulations': [],
                'improvements': []
            }

    def calculate_fitness(self, evaluation: Dict[str, float]) -> float:
        """
        Calculate fitness score from evaluation.

        Weights:
        - Intent exposure: 40% (most important)
        - BS detection: 30%
        - Clarity: 20%
        - Conciseness: 10%
        """
        intent = evaluation.get('intent_exposure_score', 0)
        bs_detection = evaluation.get('bs_detection_score', 0)
        clarity = evaluation.get('clarity_score', 0)
        conciseness = evaluation.get('conciseness_score', 0)

        fitness = (
            intent * 0.40 +
            bs_detection * 0.30 +
            clarity * 0.20 +
            conciseness * 0.10
        )

        return fitness
