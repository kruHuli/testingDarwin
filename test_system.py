#!/usr/bin/env python3
"""
Test script to validate system components without requiring API calls.
"""

import json
from src.darwinian_bs_translator.organism import (
    TranslationOrganism, DetectionPattern, TranslationTemplate, LLMPromptRules
)
from src.darwinian_bs_translator.initial_population import (
    create_urgency_manipulator_specialist,
    create_flattery_manipulator_specialist,
    create_scope_creep_specialist,
    create_responsibility_dodging_specialist,
    create_visibility_manipulation_specialist,
    create_initial_population
)


def test_organism_creation():
    """Test creating organisms."""
    print("Testing organism creation...")

    # Test urgency manipulator
    organism = create_urgency_manipulator_specialist()
    assert organism.specialist_type == "urgency_manipulator"
    assert len(organism.detection_patterns) > 0
    assert len(organism.translation_templates) > 0
    assert organism.llm_prompt_rules is not None
    print("  ✓ Urgency manipulator created successfully")

    # Test flattery manipulator
    organism = create_flattery_manipulator_specialist()
    assert organism.specialist_type == "flattery_manipulator"
    assert len(organism.detection_patterns) > 0
    print("  ✓ Flattery manipulator created successfully")

    # Test scope creep
    organism = create_scope_creep_specialist()
    assert organism.specialist_type == "scope_creep"
    print("  ✓ Scope creep specialist created successfully")

    # Test responsibility dodging
    organism = create_responsibility_dodging_specialist()
    assert organism.specialist_type == "responsibility_dodging"
    print("  ✓ Responsibility dodging specialist created successfully")

    # Test visibility manipulation
    organism = create_visibility_manipulation_specialist()
    assert organism.specialist_type == "visibility_manipulation"
    print("  ✓ Visibility manipulation specialist created successfully")

    print("✓ All organism types created successfully\n")


def test_detection_scoring():
    """Test detection pattern scoring."""
    print("Testing detection pattern scoring...")

    urgency_organism = create_urgency_manipulator_specialist()

    # Test email with urgency manipulation
    email_body = "Need this ASAP! Critical deadline by end of day. Very urgent!"
    score = urgency_organism.get_detection_score(email_body)

    print(f"  Urgency email detection score: {score:.2f}")
    assert score > 0.3, "Should detect urgency manipulation"
    print("  ✓ Urgency detection working")

    # Test email without urgency
    email_body = "Hi, when you have time, could you review this document? No rush."
    score = urgency_organism.get_detection_score(email_body)

    print(f"  Non-urgent email detection score: {score:.2f}")
    assert score < 0.5, "Should have low score for non-urgent email"
    print("  ✓ Non-urgent detection working")

    # Test flattery detection
    flattery_organism = create_flattery_manipulator_specialist()
    email_body = "You're the best at this! You're the only one who can help. Your expertise is amazing!"
    score = flattery_organism.get_detection_score(email_body)

    print(f"  Flattery email detection score: {score:.2f}")
    assert score > 0.15, "Should detect flattery manipulation"
    print("  ✓ Flattery detection working")

    print("✓ Detection scoring works correctly\n")


def test_population_creation():
    """Test creating initial populations."""
    print("Testing population creation...")

    for specialist_type in ['urgency_manipulator', 'flattery_manipulator', 'scope_creep']:
        population = create_initial_population(specialist_type, population_size=5)
        assert len(population) == 5
        assert all(org.specialist_type == specialist_type for org in population)
        print(f"  ✓ Created {specialist_type} population of 5")

    print("✓ Population creation works\n")


def test_serialization():
    """Test organism serialization."""
    print("Testing serialization...")

    organism = create_urgency_manipulator_specialist()
    organism.fitness = 7.5

    # Convert to dict
    data = organism.to_dict()
    assert isinstance(data, dict)
    assert data['specialist_type'] == 'urgency_manipulator'
    assert data['fitness'] == 7.5
    print("  ✓ Organism to dict works")

    # Convert back to organism
    restored = TranslationOrganism.from_dict(data)
    assert restored.specialist_type == organism.specialist_type
    assert restored.fitness == organism.fitness
    assert len(restored.detection_patterns) == len(organism.detection_patterns)
    print("  ✓ Organism from dict works")

    print("✓ Serialization works correctly\n")


def test_cloning():
    """Test organism cloning."""
    print("Testing cloning...")

    organism = create_urgency_manipulator_specialist()
    organism.fitness = 8.0

    clone = organism.clone()
    assert clone.specialist_type == organism.specialist_type
    assert clone.generation == organism.generation + 1
    assert len(clone.detection_patterns) == len(organism.detection_patterns)

    # Modify clone shouldn't affect original
    clone.fitness = 9.0
    assert organism.fitness == 8.0

    print("  ✓ Cloning creates independent copy")
    print("✓ Cloning works correctly\n")


def test_training_data():
    """Test loading training data."""
    print("Testing training data loading...")

    with open('emails.json', 'r') as f:
        data = json.load(f)

    emails = data['corporate_email_training_data_21_100']
    print(f"  Loaded {len(emails)} emails")

    # Check first email structure
    email = emails[0]
    assert 'subject' in email
    assert 'sender' in email
    assert 'body' in email
    assert 'what_the_sender_really_wants' in email

    print(f"  ✓ Email structure valid")
    print(f"  Sample email: '{email['subject']}'")

    print("✓ Training data loads correctly\n")


def test_multi_specialist_detection():
    """Test that emails can trigger multiple specialists."""
    print("Testing multi-specialist detection...")

    # Email with both urgency and flattery
    email_body = """You're the only one who can help with this!
    Need this ASAP - critical deadline by EOD.
    Your expertise is really needed here."""

    urgency = create_urgency_manipulator_specialist()
    flattery = create_flattery_manipulator_specialist()

    urgency_score = urgency.get_detection_score(email_body)
    flattery_score = flattery.get_detection_score(email_body)

    print(f"  Urgency score: {urgency_score:.2f}")
    print(f"  Flattery score: {flattery_score:.2f}")

    assert urgency_score > 0.2, "Should detect urgency"
    assert flattery_score > 0.1, "Should detect flattery"

    print("  ✓ Multiple specialists can detect same email")
    print("✓ Multi-specialist detection works\n")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("CORPORATE BS TRANSLATOR - SYSTEM VALIDATION")
    print("="*60 + "\n")

    try:
        test_organism_creation()
        test_detection_scoring()
        test_population_creation()
        test_serialization()
        test_cloning()
        test_training_data()
        test_multi_specialist_detection()

        print("="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nSystem is ready for use.")
        print("\nNext steps:")
        print("1. Set ANTHROPIC_API_KEY in .env file")
        print("2. Run: python bs_translator.py train")
        print("3. Run: python bs_translator.py test")
        print("\n")

        return 0

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
