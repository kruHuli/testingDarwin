"""
Organism structure for the Corporate BS Translator.

Each organism represents a translation strategy with:
- Template-based patterns
- LLM prompt engineering rules
- Detection rules for specific manipulation types
- Response templates
"""

import json
import copy
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class DetectionPattern:
    """Pattern for detecting specific corporate BS tactics."""
    trigger_phrases: List[str]
    context_clues: List[str]
    manipulation_type: str
    weight: float = 1.0

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'DetectionPattern':
        return cls(**data)


@dataclass
class TranslationTemplate:
    """Template for translating detected BS into plain English."""
    pattern_name: str
    template: str
    examples: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'TranslationTemplate':
        return cls(**data)


@dataclass
class LLMPromptRules:
    """Rules for how to instruct the LLM to detect and translate BS."""
    system_prompt: str
    detection_instructions: List[str]
    translation_guidelines: List[str]
    focus_areas: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'LLMPromptRules':
        return cls(**data)


class TranslationOrganism:
    """
    An organism that evolves translation strategies for corporate BS.

    Each organism is specialized for a specific type of manipulation and contains:
    - Detection patterns (template-based matching)
    - LLM prompt engineering rules
    - Translation templates
    - Fitness score from evolution
    """

    def __init__(
        self,
        specialist_type: str,
        detection_patterns: Optional[List[DetectionPattern]] = None,
        translation_templates: Optional[List[TranslationTemplate]] = None,
        llm_prompt_rules: Optional[LLMPromptRules] = None,
        fitness: float = 0.0,
        generation: int = 0
    ):
        self.specialist_type = specialist_type
        self.detection_patterns = detection_patterns or []
        self.translation_templates = translation_templates or []
        self.llm_prompt_rules = llm_prompt_rules
        self.fitness = fitness
        self.generation = generation
        self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate a unique ID for this organism."""
        import hashlib
        import time
        content = f"{self.specialist_type}_{time.time()}_{self.generation}"
        return hashlib.md5(content.encode()).hexdigest()[:8]

    def clone(self) -> 'TranslationOrganism':
        """Create a deep copy of this organism."""
        return TranslationOrganism(
            specialist_type=self.specialist_type,
            detection_patterns=[copy.deepcopy(p) for p in self.detection_patterns],
            translation_templates=[copy.deepcopy(t) for t in self.translation_templates],
            llm_prompt_rules=copy.deepcopy(self.llm_prompt_rules),
            fitness=self.fitness,
            generation=self.generation + 1
        )

    def to_dict(self) -> Dict:
        """Convert organism to dictionary for serialization."""
        return {
            'specialist_type': self.specialist_type,
            'detection_patterns': [p.to_dict() for p in self.detection_patterns],
            'translation_templates': [t.to_dict() for t in self.translation_templates],
            'llm_prompt_rules': self.llm_prompt_rules.to_dict() if self.llm_prompt_rules else None,
            'fitness': self.fitness,
            'generation': self.generation,
            'id': self.id
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TranslationOrganism':
        """Create organism from dictionary."""
        return cls(
            specialist_type=data['specialist_type'],
            detection_patterns=[DetectionPattern.from_dict(p) for p in data['detection_patterns']],
            translation_templates=[TranslationTemplate.from_dict(t) for t in data['translation_templates']],
            llm_prompt_rules=LLMPromptRules.from_dict(data['llm_prompt_rules']) if data['llm_prompt_rules'] else None,
            fitness=data.get('fitness', 0.0),
            generation=data.get('generation', 0)
        )

    def get_detection_score(self, email_body: str, email_subject: str = "") -> float:
        """
        Calculate how strongly this organism detects its specialty in the email.
        Returns a score from 0.0 to 1.0.
        """
        score = 0.0
        text = f"{email_subject} {email_body}".lower()

        for pattern in self.detection_patterns:
            # Check trigger phrases
            phrase_matches = sum(1 for phrase in pattern.trigger_phrases if phrase.lower() in text)
            if phrase_matches > 0:
                score += pattern.weight * (phrase_matches / len(pattern.trigger_phrases))

            # Check context clues
            context_matches = sum(1 for clue in pattern.context_clues if clue.lower() in text)
            if context_matches > 0:
                score += pattern.weight * 0.5 * (context_matches / len(pattern.context_clues))

        # Normalize to 0-1 range
        return min(1.0, score / max(1, len(self.detection_patterns)))

    def __repr__(self) -> str:
        return f"TranslationOrganism({self.specialist_type}, fitness={self.fitness:.2f}, gen={self.generation}, id={self.id})"
