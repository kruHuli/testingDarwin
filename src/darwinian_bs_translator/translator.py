"""
Translator that uses organism strategies to translate emails with LLM.
"""

import os
from typing import Dict, Any, Optional
from anthropic import Anthropic
from .organism import TranslationOrganism


class BSEmailTranslator:
    """
    Translates corporate BS emails using evolved organism strategies.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def translate(
        self,
        email: Dict[str, Any],
        organism: TranslationOrganism
    ) -> str:
        """
        Translate an email using the organism's evolved strategy.

        Args:
            email: Email data dictionary
            organism: TranslationOrganism with evolved strategy

        Returns:
            Plain English translation
        """
        email_body = email.get('body', '')
        email_subject = email.get('subject', '')
        sender = email.get('sender', 'unknown')
        sender_level = email.get('sender_level', 'unknown')

        # Build the LLM prompt using organism's evolved rules
        system_prompt = self._build_system_prompt(organism)
        user_prompt = self._build_user_prompt(email, organism)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.5,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            translation = response.content[0].text.strip()
            return translation

        except Exception as e:
            return f"Translation error: {str(e)}"

    def _build_system_prompt(self, organism: TranslationOrganism) -> str:
        """Build system prompt from organism's LLM rules."""
        if not organism.llm_prompt_rules:
            return "You translate corporate emails into plain English."

        rules = organism.llm_prompt_rules
        prompt = rules.system_prompt + "\n\n"

        if rules.detection_instructions:
            prompt += "DETECTION INSTRUCTIONS:\n"
            for instruction in rules.detection_instructions:
                prompt += f"- {instruction}\n"
            prompt += "\n"

        if rules.translation_guidelines:
            prompt += "TRANSLATION GUIDELINES:\n"
            for guideline in rules.translation_guidelines:
                prompt += f"- {guideline}\n"
            prompt += "\n"

        if rules.focus_areas:
            prompt += f"FOCUS AREAS: {', '.join(rules.focus_areas)}\n\n"

        prompt += """
Your job is to translate the corporate email into a single, direct sentence that exposes:
1. What the sender REALLY wants
2. What manipulation tactics they're using
3. Why this benefits them (not you)

Be concise, direct, and brutally honest. Cut through all the BS."""

        return prompt

    def _build_user_prompt(
        self,
        email: Dict[str, Any],
        organism: TranslationOrganism
    ) -> str:
        """Build user prompt with email and detection patterns."""
        prompt = f"""EMAIL TO TRANSLATE:
Subject: {email.get('subject', '')}
From: {email.get('sender', '')} ({email.get('sender_level', 'unknown')} level)
Sent: {email.get('time_sent', '')}

Body:
{email.get('body', '')}

"""

        # Add detection pattern hints
        if organism.detection_patterns:
            prompt += "MANIPULATION PATTERNS TO WATCH FOR:\n"
            for pattern in organism.detection_patterns:
                prompt += f"- {pattern.manipulation_type}: Look for phrases like {', '.join(pattern.trigger_phrases[:3])}\n"
            prompt += "\n"

        prompt += "TRANSLATION (1-2 sentences, brutally honest):"

        return prompt
