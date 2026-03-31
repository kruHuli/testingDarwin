"""
Darwinian evolution engine for BS translation organisms.
"""

import random
import json
from typing import List, Dict, Any, Optional
from tqdm import tqdm
from .organism import TranslationOrganism
from .evaluator import TranslationEvaluator
from .translator import BSEmailTranslator
from .mutator import OrganismMutator


class EvolutionEngine:
    """
    Runs Darwinian evolution on translation organisms.

    Process:
    1. Evaluate fitness of all organisms on training data
    2. Select top performers
    3. Create next generation through mutation
    4. Repeat
    """

    def __init__(
        self,
        evaluator: TranslationEvaluator,
        translator: BSEmailTranslator,
        mutator: OrganismMutator,
        population_size: int = 10,
        elite_size: int = 3,
        mutation_rate: float = 0.4
    ):
        self.evaluator = evaluator
        self.translator = translator
        self.mutator = mutator
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate

    def evolve(
        self,
        initial_population: List[TranslationOrganism],
        training_data: List[Dict[str, Any]],
        generations: int = 10,
        verbose: bool = True
    ) -> List[TranslationOrganism]:
        """
        Run evolution for specified number of generations.

        Args:
            initial_population: Starting organisms
            training_data: Email data for training
            generations: Number of generations to evolve
            verbose: Print progress

        Returns:
            Final population sorted by fitness
        """
        population = initial_population
        specialist_type = population[0].specialist_type if population else "unknown"

        # Track best organism across all generations
        all_time_best = None
        all_time_best_fitness = 0.0

        if verbose:
            print(f"\n{'='*60}")
            print(f"Evolving {specialist_type} specialist")
            print(f"Population: {len(population)}, Generations: {generations}")
            print(f"{'='*60}\n")

        for gen in range(generations):
            if verbose:
                print(f"Generation {gen + 1}/{generations}")

            # Evaluate all organisms
            population = self._evaluate_population(
                population,
                training_data,
                verbose=verbose
            )

            # Track best
            best = max(population, key=lambda o: o.fitness)
            if best.fitness > all_time_best_fitness:
                all_time_best = best
                all_time_best_fitness = best.fitness

            if verbose:
                print(f"  Best fitness: {best.fitness:.2f}")
                print(f"  Avg fitness: {sum(o.fitness for o in population) / len(population):.2f}")
                print(f"  All-time best: {all_time_best_fitness:.2f}\n")

            # Create next generation
            if gen < generations - 1:  # Don't mutate on last generation
                population = self._create_next_generation(
                    population,
                    training_data,
                    verbose=verbose
                )

        # Final sort by fitness
        population.sort(key=lambda o: o.fitness, reverse=True)

        if verbose:
            print(f"Evolution complete!")
            print(f"Final best fitness: {population[0].fitness:.2f}")
            print(f"All-time best fitness: {all_time_best_fitness:.2f}\n")

        return population

    def _evaluate_population(
        self,
        population: List[TranslationOrganism],
        training_data: List[Dict[str, Any]],
        verbose: bool = True
    ) -> List[TranslationOrganism]:
        """Evaluate fitness of all organisms."""

        # Sample training data to avoid evaluating on all emails every time
        sample_size = min(10, len(training_data))
        sample_emails = random.sample(training_data, sample_size)

        for organism in population:
            total_fitness = 0.0

            for email in sample_emails:
                # Translate email using organism
                translation = self.translator.translate(email, organism)

                # Evaluate translation
                evaluation = self.evaluator.evaluate_translation(
                    email,
                    translation,
                    organism.specialist_type
                )

                # Calculate fitness
                fitness = self.evaluator.calculate_fitness(evaluation)
                total_fitness += fitness

            # Average fitness across sample
            organism.fitness = total_fitness / len(sample_emails)

        return population

    def _create_next_generation(
        self,
        population: List[TranslationOrganism],
        training_data: List[Dict[str, Any]],
        verbose: bool = True
    ) -> List[TranslationOrganism]:
        """
        Create next generation using selection and mutation.

        Strategy:
        1. Keep top elite_size organisms unchanged
        2. Fill rest with mutations of top performers
        """
        # Sort by fitness
        population.sort(key=lambda o: o.fitness, reverse=True)

        # Collect failed translations for LLM-guided mutation
        failed_translations = self._collect_failed_translations(
            population[-3:],  # Bottom 3 performers
            training_data[:5]  # Use a few training examples
        )

        next_generation = []

        # Elite selection - keep best unchanged
        elite = population[:self.elite_size]
        next_generation.extend(elite)

        if verbose:
            print(f"  Keeping {len(elite)} elite organisms")

        # Fill rest with mutations
        while len(next_generation) < self.population_size:
            # Select parent from top half of population
            parent = random.choice(population[:max(1, len(population) // 2)])

            # Mutate
            child = self.mutator.mutate(
                parent,
                failed_translations=failed_translations,
                mutation_rate=self.mutation_rate
            )

            next_generation.append(child)

        return next_generation

    def _collect_failed_translations(
        self,
        weak_organisms: List[TranslationOrganism],
        emails: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Collect examples of failed translations for learning."""
        failures = []

        for organism in weak_organisms[:2]:  # Limit to avoid too many API calls
            for email in emails[:3]:
                translation = self.translator.translate(email, organism)
                evaluation = self.evaluator.evaluate_translation(
                    email,
                    translation,
                    organism.specialist_type
                )

                if evaluation.get('overall_score', 0) < 5.0:
                    failures.append({
                        'email_subject': email.get('subject', ''),
                        'email_body': email.get('body', ''),
                        'translation': translation,
                        'feedback': evaluation.get('feedback', ''),
                        'missed_manipulations': evaluation.get('missed_manipulations', [])
                    })

        return failures
