#!/usr/bin/env python3
"""
Simple Calculator Application
Agent: code_writer
Task: Core implementation based on code_analyst design
"""
from typing import Union


class Calculator:
    """
    A simple calculator with basic arithmetic operations.

    Supports addition, subtraction, multiplication, and division
    with comprehensive error handling and input validation.
    """

    def __init__(self):
        """Initialize the calculator."""
        self.last_result = None
        self.operation_count = 0

    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b

        Raises:
            TypeError: If inputs are not numeric
        """
        self._validate_input(a, b)
        result = a + b
        self._update_state(result)
        return result

    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Subtract b from a.

        Args:
            a: First number
            b: Second number

        Returns:
            Difference of a and b

        Raises:
            TypeError: If inputs are not numeric
        """
        self._validate_input(a, b)
        result = a - b
        self._update_state(result)
        return result

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Product of a and b

        Raises:
            TypeError: If inputs are not numeric
        """
        self._validate_input(a, b)
        result = a * b
        self._update_state(result)
        return result

    def divide(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Divide a by b.

        Args:
            a: Numerator
            b: Denominator

        Returns:
            Quotient of a and b

        Raises:
            TypeError: If inputs are not numeric
            ZeroDivisionError: If b is zero
        """
        self._validate_input(a, b)

        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        result = a / b
        self._update_state(result)
        return result

    def _validate_input(self, a: Union[int, float], b: Union[int, float]) -> None:
        """
        Validate that inputs are numeric.

        Args:
            a: First input
            b: Second input

        Raises:
            TypeError: If either input is not numeric
        """
        if not isinstance(a, (int, float)):
            raise TypeError(f"First argument must be numeric, got {type(a).__name__}")
        if not isinstance(b, (int, float)):
            raise TypeError(f"Second argument must be numeric, got {type(b).__name__}")

    def _update_state(self, result: Union[int, float]) -> None:
        """Update calculator state after operation."""
        self.last_result = result
        self.operation_count += 1

    def get_last_result(self) -> Union[int, float, None]:
        """Get the result of the last operation."""
        return self.last_result

    def get_operation_count(self) -> int:
        """Get the total number of operations performed."""
        return self.operation_count

    def reset(self) -> None:
        """Reset calculator state."""
        self.last_result = None
        self.operation_count = 0


if __name__ == "__main__":
    # Quick test
    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"20 / 4 = {calc.divide(20, 4)}")
    print(f"Operations performed: {calc.get_operation_count()}")
