"""
Initial population generators for different specialist types.

Each specialist swarm starts with hand-crafted initial strategies that will
then evolve through the Darwinian process.
"""

from typing import List
from .organism import TranslationOrganism, DetectionPattern, TranslationTemplate, LLMPromptRules


def create_urgency_manipulator_specialist() -> TranslationOrganism:
    """Create initial organism for detecting urgency manipulation."""

    detection_patterns = [
        DetectionPattern(
            trigger_phrases=["ASAP", "urgent", "right away", "as soon as possible", "time-sensitive",
                           "end of day", "EOD", "deadline", "critical"],
            context_clues=["need this", "important that", "can't wait", "immediately"],
            manipulation_type="urgency",
            weight=1.5
        ),
        DetectionPattern(
            trigger_phrases=["just following up", "per my last email", "haven't heard back",
                           "following up on", "circling back", "follow up", "wanted to follow up",
                           "get ahead of", "trying to get ahead of"],
            context_clues=["waiting for", "still need", "reminder", "came up", "questions came up"],
            manipulation_type="fake_urgency",
            weight=1.2
        ),
        DetectionPattern(
            trigger_phrases=["today", "by end of week", "before you leave", "this afternoon"],
            context_clues=["short notice", "last minute", "tight timeline"],
            manipulation_type="deadline_pressure",
            weight=1.3
        )
    ]

    translation_templates = [
        TranslationTemplate(
            pattern_name="urgent_with_short_notice",
            template="Sender wants {task} done {timeframe} because of their poor planning, using {pressure_tactic} to make you feel guilty about saying no.",
            examples=["Sender wants the report done by EOD because of their poor planning, using fake urgency to make you feel guilty about saying no."]
        ),
        TranslationTemplate(
            pattern_name="follow_up_pressure",
            template="Sender is creating artificial urgency by claiming they sent something before (possibly true, possibly not) to pressure you into dropping everything.",
            examples=[]
        ),
        TranslationTemplate(
            pattern_name="deadline_transfer",
            template="Sender has a real deadline but waited until the last minute to involve you, now making their emergency your emergency.",
            examples=[]
        )
    ]

    llm_prompt_rules = LLMPromptRules(
        system_prompt="You are an expert at detecting fake urgency and deadline manipulation in corporate emails.",
        detection_instructions=[
            "Look for urgency words combined with short timeframes",
            "Identify if the urgency is artificial (sender's poor planning) vs real business need",
            "Notice passive-aggressive follow-up language",
            "Check if sender is transferring their deadline stress to recipient"
        ],
        translation_guidelines=[
            "Call out artificial urgency explicitly",
            "Identify whose fault the time pressure really is",
            "Translate deadline language into actual impact",
            "Expose guilt-tripping tactics"
        ],
        focus_areas=["urgency", "deadlines", "time pressure", "follow-ups"]
    )

    return TranslationOrganism(
        specialist_type="urgency_manipulator",
        detection_patterns=detection_patterns,
        translation_templates=translation_templates,
        llm_prompt_rules=llm_prompt_rules
    )


def create_flattery_manipulator_specialist() -> TranslationOrganism:
    """Create initial organism for detecting flattery manipulation."""

    detection_patterns = [
        DetectionPattern(
            trigger_phrases=["you're the best at", "you're the only one who", "your expertise",
                           "you always", "so good at", "expert opinion", "you're literally the only",
                           "your experience", "given your experience", "your perspective"],
            context_clues=["need your help", "could you", "would you mind", "favor", "benefit from your"],
            manipulation_type="expertise_flattery",
            weight=1.6
        ),
        DetectionPattern(
            trigger_phrases=["great insights", "valuable perspective", "brilliant", "talented",
                           "nobody else can", "perfect person for"],
            context_clues=["quick question", "small favor", "just need"],
            manipulation_type="ego_stroking",
            weight=1.4
        ),
        DetectionPattern(
            trigger_phrases=["everyone says", "team loves", "known for", "reputation for"],
            context_clues=["wondering if you could", "would love your", "could really use"],
            manipulation_type="social_proof_flattery",
            weight=1.3
        )
    ]

    translation_templates = [
        TranslationTemplate(
            pattern_name="expertise_flattery_for_work",
            template="Sender is flattering your {skill} skills so you'll do {actual_work} for free/for them.",
            examples=["Sender is flattering your analytical skills so you'll do their data analysis for free."]
        ),
        TranslationTemplate(
            pattern_name="uniqueness_lie",
            template="Sender claims 'you're the only one who can help' (lie) to manipulate you into saying yes when others could easily do this.",
            examples=[]
        ),
        TranslationTemplate(
            pattern_name="ego_trap",
            template="Sender is stroking your ego about {quality} to trap you into {commitment} you don't have time for.",
            examples=[]
        )
    ]

    llm_prompt_rules = LLMPromptRules(
        system_prompt="You are an expert at detecting flattery and ego manipulation in corporate emails.",
        detection_instructions=[
            "Look for excessive compliments followed by requests",
            "Identify 'you're the only one' manipulation (usually false)",
            "Notice expertise flattery paired with 'small favors'",
            "Catch social proof manipulation (everyone thinks you're great at X)"
        ],
        translation_guidelines=[
            "Expose flattery as manipulation tactic",
            "Identify the real work being requested",
            "Call out the 'uniqueness lie' when used",
            "Translate compliments into what sender actually wants"
        ],
        focus_areas=["flattery", "expertise claims", "ego stroking", "compliments"]
    )

    return TranslationOrganism(
        specialist_type="flattery_manipulator",
        detection_patterns=detection_patterns,
        translation_templates=translation_templates,
        llm_prompt_rules=llm_prompt_rules
    )


def create_scope_creep_specialist() -> TranslationOrganism:
    """Create initial organism for detecting scope creep."""

    detection_patterns = [
        DetectionPattern(
            trigger_phrases=["quick question", "small favor", "super quick", "just need",
                           "one small thing", "real quick", "tiny ask", "simple request"],
            context_clues=["also", "and", "while you're at it", "and if you could"],
            manipulation_type="minimization",
            weight=1.7
        ),
        DetectionPattern(
            trigger_phrases=["and also", "and then", "along with", "while we're at it",
                           "on that note", "related to that"],
            context_clues=["breakdown", "analysis", "detailed", "comprehensive"],
            manipulation_type="scope_expansion",
            weight=1.5
        ),
        DetectionPattern(
            trigger_phrases=["shouldn't take long", "probably just", "simple", "easy for you"],
            context_clues=["just", "only", "quick"],
            manipulation_type="effort_minimization",
            weight=1.4
        )
    ]

    translation_templates = [
        TranslationTemplate(
            pattern_name="small_favor_lie",
            template="Sender claims this is a '{minimizer}' but actually wants {real_scope} which is {actual_time} of work.",
            examples=["Sender claims this is a 'quick question' but actually wants full budget analysis which is 8 hours of work."]
        ),
        TranslationTemplate(
            pattern_name="incremental_scope_creep",
            template="Sender starts with {initial_ask} then adds {item2}, {item3}, and {item4} - classic scope creep in a single email.",
            examples=[]
        ),
        TranslationTemplate(
            pattern_name="effort_downplaying",
            template="Sender says '{minimizing_phrase}' but ignores that this requires {actual_effort}.",
            examples=[]
        )
    ]

    llm_prompt_rules = LLMPromptRules(
        system_prompt="You are an expert at detecting scope creep and work minimization in corporate emails.",
        detection_instructions=[
            "Look for minimizing language (quick, small, simple) followed by complex requests",
            "Count the number of deliverables being requested",
            "Notice 'and also' additions that expand scope",
            "Identify effort minimization (shouldn't take long) that's unrealistic"
        ],
        translation_guidelines=[
            "Expose the real scope hidden by minimizing language",
            "Count and list all the actual deliverables requested",
            "Estimate realistic time/effort required",
            "Call out scope creep explicitly"
        ],
        focus_areas=["scope creep", "minimization", "hidden work", "effort estimation"]
    )

    return TranslationOrganism(
        specialist_type="scope_creep",
        detection_patterns=detection_patterns,
        translation_templates=translation_templates,
        llm_prompt_rules=llm_prompt_rules
    )


def create_responsibility_dodging_specialist() -> TranslationOrganism:
    """Create initial organism for detecting responsibility dodging."""

    detection_patterns = [
        DetectionPattern(
            trigger_phrases=["leadership wants", "from above", "management decided",
                           "not my decision", "company policy", "directive from",
                           "came up in", "questions came up", "leadership sync", "exec team asked"],
            context_clues=["unfortunately", "I know it's frustrating", "I agree but", "came up", "asked for"],
            manipulation_type="authority_shield",
            weight=1.6
        ),
        DetectionPattern(
            trigger_phrases=["team decided", "we all agreed", "consensus was", "group thinks"],
            context_clues=["wanted to let you know", "need to inform you"],
            manipulation_type="group_shield",
            weight=1.4
        ),
        DetectionPattern(
            trigger_phrases=["per the process", "policy states", "according to",
                           "as outlined in", "standard procedure"],
            context_clues=["required to", "must", "have to"],
            manipulation_type="process_shield",
            weight=1.3
        ),
        DetectionPattern(
            trigger_phrases=["I understand your frustration", "I hear you", "I'm on your side",
                           "between you and me", "personally I agree"],
            context_clues=["but", "unfortunately", "however", "my hands are tied"],
            manipulation_type="fake_sympathy",
            weight=1.5
        )
    ]

    translation_templates = [
        TranslationTemplate(
            pattern_name="authority_blame_shift",
            template="Sender is hiding behind '{authority}' to avoid taking responsibility for {decision}, may or may not be true.",
            examples=["Sender is hiding behind 'leadership wants this' to avoid taking responsibility for the budget cut, may or may not be true."]
        ),
        TranslationTemplate(
            pattern_name="fake_sympathy_dodge",
            template="Sender pretends to be on your side but is delivering {bad_news} while avoiding any personal accountability.",
            examples=[]
        ),
        TranslationTemplate(
            pattern_name="process_excuse",
            template="Sender uses '{process}' as excuse for {action} instead of admitting it's their choice or explaining real reason.",
            examples=[]
        )
    ]

    llm_prompt_rules = LLMPromptRules(
        system_prompt="You are an expert at detecting responsibility dodging and blame-shifting in corporate emails.",
        detection_instructions=[
            "Look for authority figures being cited (leadership, management, company)",
            "Notice 'I agree with you but my hands are tied' patterns",
            "Identify process/policy being used as shields",
            "Catch fake sympathy followed by bad news"
        ],
        translation_guidelines=[
            "Call out responsibility dodging explicitly",
            "Identify what decision is being hidden behind authority",
            "Expose fake sympathy as manipulation",
            "Question whether the authority/process excuse is real"
        ],
        focus_areas=["blame-shifting", "authority shields", "policy excuses", "fake sympathy"]
    )

    return TranslationOrganism(
        specialist_type="responsibility_dodging",
        detection_patterns=detection_patterns,
        translation_templates=translation_templates,
        llm_prompt_rules=llm_prompt_rules
    )


def create_visibility_manipulation_specialist() -> TranslationOrganism:
    """Create initial organism for detecting visibility/career manipulation."""

    detection_patterns = [
        DetectionPattern(
            trigger_phrases=["great opportunity", "visibility", "exposure", "leadership will see",
                           "high-profile", "strategic initiative", "career growth",
                           "leadership sync", "leadership meeting", "exec team", "board meeting"],
            context_clues=["would be great for you", "perfect opportunity", "showcase your",
                           "great visibility", "visibility for you", "board"],
            manipulation_type="exposure_promise",
            weight=1.7
        ),
        DetectionPattern(
            trigger_phrases=["get your name out there", "people will notice", "great for your career",
                           "make an impact", "show what you can do", "prove yourself"],
            context_clues=["this could lead to", "stepping stone", "next level"],
            manipulation_type="career_dangling",
            weight=1.6
        ),
        DetectionPattern(
            trigger_phrases=["stretch assignment", "growth opportunity", "challenging project",
                           "learn from this", "develop your skills"],
            context_clues=["no budget", "extra work", "in addition to", "on top of"],
            manipulation_type="unpaid_opportunity",
            weight=1.5
        )
    ]

    translation_templates = [
        TranslationTemplate(
            pattern_name="exposure_for_free_work",
            template="Sender promises '{exposure_claim}' in exchange for {work_requested}, which is {actual_hours} of unpaid/extra work with no guarantee of payoff.",
            examples=["Sender promises 'leadership visibility' in exchange for leading the initiative, which is 20 hours of unpaid work with no guarantee of payoff."]
        ),
        TranslationTemplate(
            pattern_name="career_bait",
            template="Sender dangles vague career benefits ('{promise}') to get you to do {actual_task} that primarily benefits them.",
            examples=[]
        ),
        TranslationTemplate(
            pattern_name="opportunity_exploitation",
            template="Sender frames {work} as 'opportunity for you' when really it's work they need done with no budget/compensation.",
            examples=[]
        )
    ]

    llm_prompt_rules = LLMPromptRules(
        system_prompt="You are an expert at detecting visibility and career manipulation in corporate emails.",
        detection_instructions=[
            "Look for promises of exposure, visibility, or career growth",
            "Notice when 'opportunities' come with no compensation/budget",
            "Identify vague promises paired with concrete work requests",
            "Catch 'great for you' framing that benefits sender more"
        ],
        translation_guidelines=[
            "Expose false promises of career advancement",
            "Calculate the real work-to-benefit ratio",
            "Call out unpaid work disguised as opportunity",
            "Identify who really benefits from the arrangement"
        ],
        focus_areas=["career manipulation", "exposure promises", "opportunity framing", "visibility"]
    )

    return TranslationOrganism(
        specialist_type="visibility_manipulation",
        detection_patterns=detection_patterns,
        translation_templates=translation_templates,
        llm_prompt_rules=llm_prompt_rules
    )


def create_initial_population(specialist_type: str, population_size: int) -> List[TranslationOrganism]:
    """
    Create initial population for a specialist swarm.

    Args:
        specialist_type: Type of specialist (urgency_manipulator, flattery_manipulator, etc.)
        population_size: Number of organisms to create

    Returns:
        List of initial organisms with slight variations
    """
    creators = {
        'urgency_manipulator': create_urgency_manipulator_specialist,
        'flattery_manipulator': create_flattery_manipulator_specialist,
        'scope_creep': create_scope_creep_specialist,
        'responsibility_dodging': create_responsibility_dodging_specialist,
        'visibility_manipulation': create_visibility_manipulation_specialist
    }

    if specialist_type not in creators:
        raise ValueError(f"Unknown specialist type: {specialist_type}")

    base_organism = creators[specialist_type]()
    population = [base_organism]

    # Create variations by cloning the base
    for _ in range(population_size - 1):
        clone = base_organism.clone()
        population.append(clone)

    return population
