"""
Specialized swarm system that manages multiple expert swarms.
"""

import json
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from .organism import TranslationOrganism
from .initial_population import create_initial_population
from .evolution import EvolutionEngine
from .evaluator import TranslationEvaluator
from .translator import BSEmailTranslator
from .mutator import OrganismMutator


class SpecialistSwarm:
    """
    A swarm of organisms specialized for one type of BS detection.
    """

    def __init__(
        self,
        specialist_type: str,
        population: List[TranslationOrganism],
        best_organism: Optional[TranslationOrganism] = None
    ):
        self.specialist_type = specialist_type
        self.population = population
        self.best_organism = best_organism or (population[0] if population else None)

    def get_best(self) -> TranslationOrganism:
        """Get the best organism in this swarm."""
        if self.best_organism:
            return self.best_organism
        return max(self.population, key=lambda o: o.fitness)

    def to_dict(self) -> Dict:
        """Serialize swarm."""
        return {
            'specialist_type': self.specialist_type,
            'population': [o.to_dict() for o in self.population],
            'best_organism': self.best_organism.to_dict() if self.best_organism else None
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SpecialistSwarm':
        """Deserialize swarm."""
        population = [TranslationOrganism.from_dict(o) for o in data['population']]
        best = TranslationOrganism.from_dict(data['best_organism']) if data.get('best_organism') else None
        return cls(data['specialist_type'], population, best)


class SwarmSystem:
    """
    Manages multiple specialist swarms working together.
    """

    SPECIALIST_TYPES = [
        'urgency_manipulator',
        'flattery_manipulator',
        'scope_creep',
        'responsibility_dodging',
        'visibility_manipulation'
    ]

    def __init__(
        self,
        evaluator: TranslationEvaluator,
        translator: BSEmailTranslator,
        mutator: OrganismMutator,
        population_size: int = 10
    ):
        self.evaluator = evaluator
        self.translator = translator
        self.mutator = mutator
        self.population_size = population_size
        self.swarms: Dict[str, SpecialistSwarm] = {}

    def initialize_swarms(self):
        """Create initial populations for all specialist types."""
        print("\nInitializing specialist swarms...")

        for specialist_type in self.SPECIALIST_TYPES:
            print(f"  Creating {specialist_type} swarm...")
            population = create_initial_population(specialist_type, self.population_size)
            self.swarms[specialist_type] = SpecialistSwarm(specialist_type, population)

        print(f"Initialized {len(self.swarms)} specialist swarms\n")

    def evolve_all_swarms(
        self,
        training_data: List[Dict[str, Any]],
        generations: int = 10,
        parallel: bool = True
    ):
        """
        Evolve all swarms on training data.

        Args:
            training_data: Email data for training
            generations: Number of generations per swarm
            parallel: Run swarms in parallel (faster but uses more API calls)
        """
        print(f"\n{'='*60}")
        print(f"EVOLVING ALL SWARMS")
        print(f"Training emails: {len(training_data)}")
        print(f"Generations: {generations}")
        print(f"Parallel: {parallel}")
        print(f"{'='*60}\n")

        if parallel:
            self._evolve_parallel(training_data, generations)
        else:
            self._evolve_sequential(training_data, generations)

        # Update best organisms
        for swarm in self.swarms.values():
            swarm.population.sort(key=lambda o: o.fitness, reverse=True)
            swarm.best_organism = swarm.population[0]

        print(f"\n{'='*60}")
        print("EVOLUTION COMPLETE - Final Results:")
        print(f"{'='*60}")
        for specialist_type, swarm in self.swarms.items():
            best = swarm.get_best()
            print(f"{specialist_type:30s} Best Fitness: {best.fitness:.2f}")
        print(f"{'='*60}\n")

    def _evolve_sequential(
        self,
        training_data: List[Dict[str, Any]],
        generations: int
    ):
        """Evolve swarms one at a time."""
        for specialist_type, swarm in self.swarms.items():
            # Filter training data for this specialist
            filtered_data = self._filter_training_data(training_data, specialist_type)

            if not filtered_data:
                print(f"Warning: No training data for {specialist_type}, using all data")
                filtered_data = training_data

            engine = EvolutionEngine(
                self.evaluator,
                self.translator,
                self.mutator,
                population_size=self.population_size,
                elite_size=3,
                mutation_rate=0.4
            )

            evolved_population = engine.evolve(
                swarm.population,
                filtered_data,
                generations=generations,
                verbose=True
            )

            swarm.population = evolved_population

    def _evolve_parallel(
        self,
        training_data: List[Dict[str, Any]],
        generations: int
    ):
        """Evolve swarms in parallel (faster but more API intensive)."""
        print("Evolving swarms in parallel...\n")

        def evolve_swarm(specialist_type: str, swarm: SpecialistSwarm):
            filtered_data = self._filter_training_data(training_data, specialist_type)
            if not filtered_data:
                filtered_data = training_data

            engine = EvolutionEngine(
                self.evaluator,
                self.translator,
                self.mutator,
                population_size=self.population_size,
                elite_size=3,
                mutation_rate=0.4
            )

            evolved = engine.evolve(
                swarm.population,
                filtered_data,
                generations=generations,
                verbose=True
            )

            return specialist_type, evolved

        with ThreadPoolExecutor(max_workers=3) as executor:  # Limit to 3 parallel to avoid rate limits
            futures = {
                executor.submit(evolve_swarm, stype, swarm): stype
                for stype, swarm in self.swarms.items()
            }

            for future in as_completed(futures):
                specialist_type, evolved_population = future.result()
                self.swarms[specialist_type].population = evolved_population

    def _filter_training_data(
        self,
        training_data: List[Dict[str, Any]],
        specialist_type: str
    ) -> List[Dict[str, Any]]:
        """
        Filter training data to emails relevant for this specialist.

        Uses manipulation_tactics_you_see field to identify relevant emails.
        """
        relevant_keywords = {
            'urgency_manipulator': ['urgency', 'urgent', 'deadline', 'pressure', 'asap', 'artificial'],
            'flattery_manipulator': ['flattery', 'ego', 'expertise', 'compliment', 'stroking'],
            'scope_creep': ['scope', 'minimization', 'small', 'quick', 'creep'],
            'responsibility_dodging': ['blame', 'responsibility', 'dodging', 'shield', 'fault'],
            'visibility_manipulation': ['visibility', 'opportunity', 'exposure', 'career', 'growth']
        }

        keywords = relevant_keywords.get(specialist_type, [])
        filtered = []

        for email in training_data:
            tactics = email.get('manipulation_tactics_you_see', '').lower()
            if any(keyword in tactics for keyword in keywords):
                filtered.append(email)

        return filtered

    def save(self, filepath: str):
        """Save all swarms to file."""
        data = {
            'swarms': {
                stype: swarm.to_dict()
                for stype, swarm in self.swarms.items()
            },
            'population_size': self.population_size
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Swarms saved to {filepath}")

    def load(self, filepath: str):
        """Load swarms from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.swarms = {
            stype: SpecialistSwarm.from_dict(swarm_data)
            for stype, swarm_data in data['swarms'].items()
        }

        print(f"Loaded {len(self.swarms)} swarms from {filepath}")
