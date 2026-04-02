"""
Email routing and ensemble combination system.

Routes emails to appropriate specialist swarms and combines their outputs.
"""

from typing import List, Dict, Any, Tuple
from .organism import TranslationOrganism
from .translator import BSEmailTranslator
from .swarm_system import SwarmSystem


class EmailRouter:
    """
    Routes emails to appropriate specialist swarms.

    Can activate multiple specialists if email contains multiple BS types.
    """

    def __init__(self, swarm_system: SwarmSystem):
        self.swarm_system = swarm_system

    def route(
        self,
        email: Dict[str, Any],
        threshold: float = 0.01,  # 1% threshold - catch even subtle patterns
        min_specialists: int = 3,  # Minimum 3 for comprehensive analysis
        max_specialists: int = 5   # Can use all 5 if they all detect something
    ) -> List[Tuple[str, TranslationOrganism, float]]:
        """
        Determine which specialists should handle this email.

        Strategy: Include ALL specialists above 5% threshold for comprehensive analysis.
        This ensures multi-pattern emails get full coverage from all relevant specialists.

        Args:
            email: Email data
            threshold: Minimum detection score to activate specialist (5%)
            min_specialists: Minimum number to activate (default 2)
            max_specialists: Maximum number to activate (default 5)

        Returns:
            List of (specialist_type, best_organism, detection_score) tuples
        """
        all_scores = []

        email_body = email.get('body', '')
        email_subject = email.get('subject', '')

        # Get detection scores from ALL specialists
        for specialist_type, swarm in self.swarm_system.swarms.items():
            best_organism = swarm.get_best()

            # Calculate how strongly this specialist detects its BS in the email
            detection_score = best_organism.get_detection_score(email_body, email_subject)

            all_scores.append((specialist_type, best_organism, detection_score))

        # Sort by detection score (strongest first)
        all_scores.sort(key=lambda x: x[2], reverse=True)

        specialists_to_activate = []

        # Strategy: Include ALL specialists above threshold (comprehensive analysis)
        # Then ensure minimum count if needed
        for specialist_type, organism, score in all_scores:
            # Include if above threshold OR we haven't hit minimum yet
            if score >= threshold:
                specialists_to_activate.append((specialist_type, organism, score))
            elif len(specialists_to_activate) < min_specialists:
                specialists_to_activate.append((specialist_type, organism, score))

            # Stop at max_specialists
            if len(specialists_to_activate) >= max_specialists:
                break

        # Ensure we always have at least min_specialists (even with very low scores)
        while len(specialists_to_activate) < min_specialists and len(all_scores) > len(specialists_to_activate):
            idx = len(specialists_to_activate)
            specialists_to_activate.append(all_scores[idx])

        return specialists_to_activate


class EnsembleTranslator:
    """
    Combines outputs from multiple specialist translators.
    """

    def __init__(
        self,
        swarm_system: SwarmSystem,
        translator: BSEmailTranslator,
        router: EmailRouter
    ):
        self.swarm_system = swarm_system
        self.translator = translator
        self.router = router

    def translate(
        self,
        email: Dict[str, Any],
        max_specialists: int = 5  # Allow up to all 5 specialists
    ) -> Dict[str, Any]:
        """
        Translate email using ensemble of specialists.

        Args:
            email: Email to translate
            max_specialists: Maximum number of specialists to use (default 5)

        Returns:
            Dictionary with translation results
        """
        # Route to specialists (router already handles max_specialists)
        specialists = self.router.route(email)

        # Don't limit further - let the router's logic decide
        # specialists = specialists[:max_specialists]  # REMOVED - router handles this

        if not specialists:
            return {
                'final_translation': "Error: No specialists activated",
                'specialist_translations': {},
                'specialists_used': []
            }

        # Get translations from each specialist
        specialist_translations = {}

        for specialist_type, organism, detection_score in specialists:
            translation = self.translator.translate(email, organism)
            specialist_translations[specialist_type] = {
                'translation': translation,
                'detection_score': detection_score,
                'organism_fitness': organism.fitness
            }

        # Combine translations
        final_translation = self._combine_translations(
            email,
            specialist_translations,
            specialists
        )

        return {
            'final_translation': final_translation,
            'specialist_translations': specialist_translations,
            'specialists_used': [s[0] for s in specialists]
        }

    def _combine_translations(
        self,
        email: Dict[str, Any],
        specialist_translations: Dict[str, Dict],
        specialists: List[Tuple[str, TranslationOrganism, float]]
    ) -> str:
        """
        Combine multiple specialist translations into one coherent translation.

        Strategy:
        - If only one specialist: use its translation
        - If multiple: combine insights, prioritizing higher detection scores
        """
        if len(specialists) == 1:
            specialist_type = specialists[0][0]
            return specialist_translations[specialist_type]['translation']

        # Multiple specialists - combine intelligently
        combined_parts = []

        # Start with highest-scoring specialist's translation
        primary = specialists[0][0]
        primary_translation = specialist_translations[primary]['translation']

        combined_parts.append(primary_translation)

        # Add insights from other specialists
        for specialist_type, organism, score in specialists[1:]:
            translation = specialist_translations[specialist_type]['translation']

            # Extract key manipulation mentions (simple approach)
            if specialist_type == 'urgency_manipulator' and 'urgent' in translation.lower():
                if 'urgent' not in primary_translation.lower():
                    combined_parts.append(f"Also using fake urgency.")

            elif specialist_type == 'flattery_manipulator' and 'flatter' in translation.lower():
                if 'flatter' not in primary_translation.lower():
                    combined_parts.append(f"Includes flattery manipulation.")

            elif specialist_type == 'scope_creep' and ('scope' in translation.lower() or 'hours' in translation.lower()):
                if 'scope' not in primary_translation.lower():
                    combined_parts.append(f"Plus scope creep tactics.")

        # Combine into final translation
        final = ' '.join(combined_parts)

        return final
