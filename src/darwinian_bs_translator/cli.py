"""
Command-line interface for the Corporate BS Email Translation System.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

from .swarm_system import SwarmSystem
from .evaluator import TranslationEvaluator
from .translator import BSEmailTranslator
from .mutator import OrganismMutator
from .ensemble import EmailRouter, EnsembleTranslator
from .actionable_translator import ActionableEmailAnalyzer

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class BSTranslatorCLI:
    """Command-line interface for the BS Translator."""

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('ANTHROPIC_API_KEY')

        if not self.api_key:
            print(f"{Fore.RED}Error: ANTHROPIC_API_KEY not found in environment")
            print(f"Please create a .env file with your API key or set it in environment{Style.RESET_ALL}")
            sys.exit(1)

        # Initialize components
        self.evaluator = TranslationEvaluator(api_key=self.api_key)
        self.translator = BSEmailTranslator(api_key=self.api_key)
        self.mutator = OrganismMutator(api_key=self.api_key)
        self.swarm_system = None
        self.ensemble = None

    def load_training_data(self, filepath: str) -> list:
        """Load training data from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Handle different data formats
        if isinstance(data, dict):
            # Assume it has a key with the emails
            key = list(data.keys())[0]
            emails = data[key]
        else:
            emails = data

        print(f"{Fore.GREEN}Loaded {len(emails)} training emails from {filepath}{Style.RESET_ALL}")
        return emails

    def train(self, args):
        """Train the system by evolving all swarms."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"CORPORATE BS EMAIL TRANSLATOR - TRAINING MODE")
        print(f"{'='*60}{Style.RESET_ALL}\n")

        # Load training data
        training_data = self.load_training_data(args.training_data)

        # Initialize swarm system
        self.swarm_system = SwarmSystem(
            self.evaluator,
            self.translator,
            self.mutator,
            population_size=args.population_size
        )

        # Initialize swarms
        self.swarm_system.initialize_swarms()

        # Evolve swarms
        self.swarm_system.evolve_all_swarms(
            training_data,
            generations=args.generations,
            parallel=args.parallel
        )

        # Save evolved swarms
        output_path = args.output or 'evolved_swarms.json'
        self.swarm_system.save(output_path)

        print(f"\n{Fore.GREEN}Training complete! Swarms saved to {output_path}{Style.RESET_ALL}")

    def translate(self, args):
        """Translate an email using evolved swarms."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"SMART EMAIL ANALYZER - AI-Powered Communication Insights")
        print(f"{'='*60}{Style.RESET_ALL}\n")

        # Load evolved swarms
        if not os.path.exists(args.swarms):
            print(f"{Fore.RED}Error: Swarms file not found: {args.swarms}")
            print(f"Please train the system first with: python -m darwinian_bs_translator train{Style.RESET_ALL}")
            sys.exit(1)

        self.swarm_system = SwarmSystem(
            self.evaluator,
            self.translator,
            self.mutator
        )
        self.swarm_system.load(args.swarms)

        # Initialize ensemble
        router = EmailRouter(self.swarm_system)
        self.ensemble = EnsembleTranslator(self.swarm_system, self.translator, router)

        # Load email to translate
        if args.email_file:
            with open(args.email_file, 'r') as f:
                email = json.load(f)
        else:
            # Interactive mode
            email = self._get_email_interactive()

        # Translate
        result = self.ensemble.translate(email)

        # Reframe into actionable analysis
        analyzer = ActionableEmailAnalyzer(api_key=self.api_key)
        actionable = analyzer.reframe_translation(
            email,
            result['final_translation'],
            result['specialists_used']
        )

        # Display results
        self._display_actionable_translation(email, result, actionable)

    def test(self, args):
        """Test system on sample emails."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"CORPORATE BS EMAIL TRANSLATOR - TEST MODE")
        print(f"{'='*60}{Style.RESET_ALL}\n")

        # Load evolved swarms
        self.swarm_system = SwarmSystem(
            self.evaluator,
            self.translator,
            self.mutator
        )
        self.swarm_system.load(args.swarms)

        # Initialize ensemble
        router = EmailRouter(self.swarm_system)
        self.ensemble = EnsembleTranslator(self.swarm_system, self.translator, router)

        # Load test emails
        test_emails = self.load_training_data(args.test_data)

        # Test on sample
        num_samples = min(args.num_samples, len(test_emails))
        import random
        samples = random.sample(test_emails, num_samples)

        print(f"Testing on {num_samples} sample emails...\n")

        for i, email in enumerate(samples, 1):
            print(f"\n{Fore.YELLOW}{'='*60}")
            print(f"TEST EMAIL {i}/{num_samples}")
            print(f"{'='*60}{Style.RESET_ALL}\n")

            result = self.ensemble.translate(email)
            self._display_translation(email, result)

            if i < num_samples:
                input(f"\n{Fore.CYAN}Press Enter for next email...{Style.RESET_ALL}")

    def _get_email_interactive(self) -> dict:
        """Get email input interactively."""
        print(f"{Fore.YELLOW}Enter email details:{Style.RESET_ALL}")

        subject = input("Subject: ")
        sender = input("Sender: ")
        sender_level = input("Sender level (boss/peer/junior): ")

        print("Email body (press Ctrl+D or Ctrl+Z when done):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        body = '\n'.join(lines)

        return {
            'subject': subject,
            'sender': sender,
            'sender_level': sender_level,
            'body': body
        }

    def _display_actionable_translation(self, email: dict, result: dict, actionable: dict):
        """Display actionable analysis results."""
        print(f"{Fore.CYAN}ORIGINAL EMAIL:{Style.RESET_ALL}")
        print(f"Subject: {Fore.WHITE}{email.get('subject', '')}{Style.RESET_ALL}")
        print(f"From: {email.get('sender', '')} ({email.get('sender_level', '')})")
        print(f"\nBody:\n{email.get('body', '')}")

        # Show patterns detected with confidence
        if result['specialist_translations']:
            print(f"\n{Fore.CYAN}📊 PATTERNS DETECTED:{Style.RESET_ALL}")
            for specialist, data in result['specialist_translations'].items():
                confidence_pct = data['detection_score'] * 100
                bar_length = int(data['detection_score'] * 20)
                bar = '█' * bar_length + '░' * (20 - bar_length)

                # Friendly names
                friendly_names = {
                    'urgency_manipulator': 'Time Sensitivity',
                    'flattery_manipulator': 'Expertise Recognition',
                    'scope_creep': 'Work Scope Analysis',
                    'responsibility_dodging': 'Authority Context',
                    'visibility_manipulation': 'Strategic Visibility'
                }
                friendly = friendly_names.get(specialist, specialist)
                print(f"  {friendly:25s} [{bar}] {confidence_pct:5.1f}%")

        # Show actionable analysis
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"AI COMMUNICATION INSIGHTS:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{actionable['actionable_analysis']}{Style.RESET_ALL}")

    def _display_translation(self, email: dict, result: dict):
        """Display translation results (legacy mode for testing)."""
        print(f"{Fore.CYAN}ORIGINAL EMAIL:{Style.RESET_ALL}")
        print(f"Subject: {Fore.WHITE}{email.get('subject', '')}{Style.RESET_ALL}")
        print(f"From: {email.get('sender', '')} ({email.get('sender_level', '')})")
        print(f"\nBody:\n{email.get('body', '')}")

        if email.get('what_the_sender_really_wants'):
            print(f"\n{Fore.YELLOW}GROUND TRUTH:{Style.RESET_ALL}")
            print(email['what_the_sender_really_wants'])

        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"TRANSLATION:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{result['final_translation']}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}Specialists used: {', '.join(result['specialists_used'])}{Style.RESET_ALL}")

        # Always show detection scores
        if result['specialist_translations']:
            print(f"\n{Fore.CYAN}Detection Confidence Scores:{Style.RESET_ALL}")
            for specialist, data in result['specialist_translations'].items():
                confidence_pct = data['detection_score'] * 100
                bar_length = int(data['detection_score'] * 20)
                bar = '█' * bar_length + '░' * (20 - bar_length)
                print(f"  {specialist:25s} [{bar}] {confidence_pct:5.1f}%")

        if len(result['specialist_translations']) > 1:
            print(f"\n{Fore.CYAN}Individual specialist translations:{Style.RESET_ALL}")
            for specialist, data in result['specialist_translations'].items():
                print(f"\n  {specialist}:")
                print(f"    Detection: {data['detection_score']:.2f}")
                print(f"    Translation: {data['translation']}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Corporate BS Email Translation System using Darwinian Evolution'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Train command
    train_parser = subparsers.add_parser('train', help='Train the system by evolving swarms')
    train_parser.add_argument(
        '--training-data',
        default='emails.json',
        help='Path to training data JSON file (default: emails.json)'
    )
    train_parser.add_argument(
        '--generations',
        type=int,
        default=10,
        help='Number of generations to evolve (default: 10)'
    )
    train_parser.add_argument(
        '--population-size',
        type=int,
        default=10,
        help='Population size per swarm (default: 10)'
    )
    train_parser.add_argument(
        '--output',
        default='evolved_swarms.json',
        help='Output file for evolved swarms (default: evolved_swarms.json)'
    )
    train_parser.add_argument(
        '--parallel',
        action='store_true',
        help='Evolve swarms in parallel (faster but more API intensive)'
    )

    # Translate command
    translate_parser = subparsers.add_parser('translate', help='Translate an email')
    translate_parser.add_argument(
        '--swarms',
        default='evolved_swarms.json',
        help='Path to evolved swarms file (default: evolved_swarms.json)'
    )
    translate_parser.add_argument(
        '--email-file',
        help='JSON file with email to translate (if not provided, will prompt interactively)'
    )

    # Test command
    test_parser = subparsers.add_parser('test', help='Test system on sample emails')
    test_parser.add_argument(
        '--swarms',
        default='evolved_swarms.json',
        help='Path to evolved swarms file (default: evolved_swarms.json)'
    )
    test_parser.add_argument(
        '--test-data',
        default='emails.json',
        help='Path to test data JSON file (default: emails.json)'
    )
    test_parser.add_argument(
        '--num-samples',
        type=int,
        default=5,
        help='Number of sample emails to test (default: 5)'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cli = BSTranslatorCLI()

    if args.command == 'train':
        cli.train(args)
    elif args.command == 'translate':
        cli.translate(args)
    elif args.command == 'test':
        cli.test(args)


if __name__ == '__main__':
    main()
