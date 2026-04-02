"""
Actionable Email Analyzer - Constructive reframing of translations.

Instead of calling out "manipulation", provides helpful insights and action plans.
"""

import os
from typing import Dict, Any
from anthropic import Anthropic


class ActionableEmailAnalyzer:
    """
    Analyzes emails and provides constructive insights + action plans.
    """

    def __init__(self, api_key: str = None, model: str = "claude-3-haiku-20240307"):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def reframe_translation(
        self,
        email: Dict[str, Any],
        raw_translation: str,
        specialist_types: list
    ) -> Dict[str, Any]:
        """
        Convert negative translation into constructive action plan.

        Args:
            email: Original email data
            raw_translation: The BS-detecting translation
            specialist_types: Which specialists were activated

        Returns:
            Dictionary with constructive reframing
        """
        email_subject = email.get('subject', '')
        email_body = email.get('body', '')
        sender = email.get('sender', 'Sender')

        # Map specialist types to constructive categories
        categories = {
            'urgency_manipulator': 'Timeline Pressure',
            'flattery_manipulator': 'Relationship Building',
            'scope_creep': 'Scope Clarification Needed',
            'responsibility_dodging': 'Decision Ownership',
            'visibility_manipulation': 'Career Opportunity'
        }

        active_categories = [categories.get(s, s) for s in specialist_types]

        prompt = f"""You are a helpful email analyzer that provides constructive insights and action plans.

ORIGINAL EMAIL:
Subject: {email_subject}
From: {sender}
Body: {email_body}

DETECTED PATTERNS: {', '.join(active_categories)}

Your job is to reframe this email analysis in a HELPFUL, NON-JUDGMENTAL way that:

1. WHAT'S REALLY BEING ASKED: Clearly state what work/commitment is actually requested
2. KEY OBSERVATIONS: Note important patterns (time pressure, scope, etc.) without being negative
3. ESTIMATED EFFORT: Realistically estimate time/work required
4. SMART ACTION PLAN: Give 2-3 specific response options

TONE: Professional, helpful, constructive. Don't use words like "manipulation", "trick", "BS", etc.
Instead use: "note", "pattern", "consideration", "opportunity to clarify", etc.

Respond in this exact format:

📋 WHAT'S REALLY BEING ASKED:
[Clear, direct summary of actual request]

🔍 KEY OBSERVATIONS:
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]

⏱️ ESTIMATED EFFORT:
[Realistic time estimate for what's requested]

✅ RECOMMENDED RESPONSE OPTIONS:

Option 1 - Direct Acceptance:
[How to say yes with clear boundaries]

Option 2 - Negotiate Scope:
[How to accept partially or negotiate timeline]

Option 3 - Polite Decline:
[How to decline professionally if needed]

Keep it concise and actionable."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            reframed = response.content[0].text.strip()

            return {
                'actionable_analysis': reframed,
                'patterns_detected': active_categories,
                'tone': 'constructive'
            }

        except Exception as e:
            # Fallback if API fails
            return {
                'actionable_analysis': self._create_fallback_analysis(email, specialist_types),
                'patterns_detected': active_categories,
                'tone': 'constructive'
            }

    def _create_fallback_analysis(self, email: Dict[str, Any], specialists: list) -> str:
        """Create a detailed constructive analysis without API."""

        body = email.get('body', '').lower()
        subject = email.get('subject', '')

        # Analyze what's being asked
        request_summary = "The sender is requesting your input and assistance."
        if 'scope_creep' in specialists:
            if any(word in body for word in ['breakdown', 'analysis', 'review', 'estimate', 'detailed', 'comprehensive']):
                request_summary = "Multiple deliverables are requested (review, analysis, estimates, etc.) which will require significant time and effort."

        patterns = []
        if 'scope_creep' in specialists:
            patterns.append("- Work scope appears larger than initial framing suggests")
            patterns.append("- Phrases like 'quick', 'small', or 'just' may understate actual effort needed")
            patterns.append("- Consider listing all deliverables to clarify total scope")
        if 'urgency_manipulator' in specialists:
            patterns.append("- Timeline is tight and worth discussing")
            patterns.append("- Consider if urgency is due to external factors or planning issues")
        if 'flattery_manipulator' in specialists:
            patterns.append("- Your expertise and capabilities are highlighted")
            patterns.append("- Worth considering if this aligns with your core responsibilities")
        if 'visibility_manipulation' in specialists:
            patterns.append("- Career growth or visibility opportunity is mentioned")
            patterns.append("- Evaluate concrete benefits vs. time investment")
        if 'responsibility_dodging' in specialists:
            patterns.append("- Decision-making authority may need clarification")

        # Estimate effort based on patterns
        if 'scope_creep' in specialists and 'urgency_manipulator' in specialists:
            effort = "8-12 hours of work"
            timeline = "this week"
        elif 'scope_creep' in specialists:
            effort = "4-8 hours of focused work"
            timeline = "next week"
        else:
            effort = "2-3 hours"
            timeline = "in the next few days"

        # Create concise pattern summary
        pattern_list = []
        if 'scope_creep' in specialists:
            pattern_list.append("scope larger than implied")
        if 'urgency_manipulator' in specialists:
            pattern_list.append("tight timeline")
        if 'flattery_manipulator' in specialists:
            pattern_list.append("expertise highlighted")
        if 'visibility_manipulation' in specialists:
            pattern_list.append("career opportunity")
        if 'responsibility_dodging' in specialists:
            pattern_list.append("authority unclear")

        pattern_text = ", ".join(pattern_list) if pattern_list else "standard request"

        return f"""📋 ACTUAL REQUEST: {request_summary}

⏱️ EFFORT: {effort} | 🔍 PATTERNS: {pattern_text}

✅ RESPONSE OPTIONS:

1️⃣ ACCEPT: "I can do this—needs {effort}. Ready by [date]?"

2️⃣ NEGOTIATE: "Quick feedback [soon] or detailed analysis [later]?"

3️⃣ DECLINE: "Swamped {timeline}. Can [colleague] help instead?"

💡 TIP: List all deliverables before committing."""
