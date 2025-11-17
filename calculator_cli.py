#!/usr/bin/env python3
"""
Calculator CLI Interface
Agent: code_writer
Task: Create user-friendly command-line interface
"""
import sys
from calculator import Calculator


class CalculatorCLI:
    """Command-line interface for the Calculator."""

    def __init__(self):
        """Initialize the CLI with a Calculator instance."""
        self.calc = Calculator()
        self.running = True

    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("          SIMPLE CALCULATOR")
        print("="*50)
        print("Operations:")
        print("  1. Add")
        print("  2. Subtract")
        print("  3. Multiply")
        print("  4. Divide")
        print("  5. View last result")
        print("  6. View operation count")
        print("  7. Reset calculator")
        print("  8. Exit")
        print("="*50)

    def get_number_input(self, prompt: str) -> float:
        """
        Get numeric input from user with validation.

        Args:
            prompt: Prompt to display to user

        Returns:
            Numeric value entered by user
        """
        while True:
            try:
                value = input(prompt)
                return float(value)
            except ValueError:
                print("❌ Error: Please enter a valid number")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)

    def perform_operation(self, operation: str):
        """
        Perform a calculation operation.

        Args:
            operation: The operation to perform
        """
        print(f"\n--- {operation.upper()} ---")
        a = self.get_number_input("Enter first number: ")
        b = self.get_number_input("Enter second number: ")

        try:
            if operation == "add":
                result = self.calc.add(a, b)
                print(f"✅ Result: {a} + {b} = {result}")
            elif operation == "subtract":
                result = self.calc.subtract(a, b)
                print(f"✅ Result: {a} - {b} = {result}")
            elif operation == "multiply":
                result = self.calc.multiply(a, b)
                print(f"✅ Result: {a} × {b} = {result}")
            elif operation == "divide":
                result = self.calc.divide(a, b)
                print(f"✅ Result: {a} ÷ {b} = {result}")

        except ZeroDivisionError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def run(self):
        """Run the calculator CLI main loop."""
        print("\n👋 Welcome to Simple Calculator!")

        while self.running:
            self.display_menu()

            try:
                choice = input("\nSelect operation (1-8): ").strip()

                if choice == "1":
                    self.perform_operation("add")
                elif choice == "2":
                    self.perform_operation("subtract")
                elif choice == "3":
                    self.perform_operation("multiply")
                elif choice == "4":
                    self.perform_operation("divide")
                elif choice == "5":
                    last = self.calc.get_last_result()
                    if last is not None:
                        print(f"\n📊 Last result: {last}")
                    else:
                        print("\n📊 No operations performed yet")
                elif choice == "6":
                    count = self.calc.get_operation_count()
                    print(f"\n📊 Total operations: {count}")
                elif choice == "7":
                    self.calc.reset()
                    print("\n🔄 Calculator reset")
                elif choice == "8":
                    print("\n👋 Thank you for using Simple Calculator!")
                    self.running = False
                else:
                    print("\n❌ Invalid choice. Please select 1-8")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                print(f"\n❌ Error: {e}")

        print("Exiting...\n")


def main():
    """Main entry point for the calculator CLI."""
    cli = CalculatorCLI()
    cli.run()


if __name__ == "__main__":
    main()
