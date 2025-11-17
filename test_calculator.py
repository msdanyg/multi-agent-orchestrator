#!/usr/bin/env python3
"""
Calculator Unit Tests
Agent: tester
Task: Comprehensive testing of calculator functionality
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Test suite for Calculator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def tearDown(self):
        """Clean up after tests."""
        self.calc = None

    # Addition Tests
    def test_add_positive_numbers(self):
        """Test addition with positive numbers."""
        result = self.calc.add(5, 3)
        self.assertEqual(result, 8)

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        result = self.calc.add(-5, -3)
        self.assertEqual(result, -8)

    def test_add_mixed_numbers(self):
        """Test addition with mixed positive and negative."""
        result = self.calc.add(10, -3)
        self.assertEqual(result, 7)

    def test_add_floats(self):
        """Test addition with floating point numbers."""
        result = self.calc.add(2.5, 3.7)
        self.assertAlmostEqual(result, 6.2, places=1)

    def test_add_zero(self):
        """Test addition with zero."""
        result = self.calc.add(5, 0)
        self.assertEqual(result, 5)

    # Subtraction Tests
    def test_subtract_positive_numbers(self):
        """Test subtraction with positive numbers."""
        result = self.calc.subtract(10, 3)
        self.assertEqual(result, 7)

    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        result = self.calc.subtract(-5, -3)
        self.assertEqual(result, -2)

    def test_subtract_result_negative(self):
        """Test subtraction resulting in negative."""
        result = self.calc.subtract(3, 10)
        self.assertEqual(result, -7)

    def test_subtract_floats(self):
        """Test subtraction with floats."""
        result = self.calc.subtract(5.5, 2.3)
        self.assertAlmostEqual(result, 3.2, places=1)

    # Multiplication Tests
    def test_multiply_positive_numbers(self):
        """Test multiplication with positive numbers."""
        result = self.calc.multiply(4, 5)
        self.assertEqual(result, 20)

    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        result = self.calc.multiply(-3, -4)
        self.assertEqual(result, 12)

    def test_multiply_mixed_signs(self):
        """Test multiplication with mixed signs."""
        result = self.calc.multiply(-5, 3)
        self.assertEqual(result, -15)

    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        result = self.calc.multiply(5, 0)
        self.assertEqual(result, 0)

    def test_multiply_floats(self):
        """Test multiplication with floats."""
        result = self.calc.multiply(2.5, 4.0)
        self.assertEqual(result, 10.0)

    # Division Tests
    def test_divide_positive_numbers(self):
        """Test division with positive numbers."""
        result = self.calc.divide(20, 4)
        self.assertEqual(result, 5)

    def test_divide_negative_numbers(self):
        """Test division with negative numbers."""
        result = self.calc.divide(-20, -4)
        self.assertEqual(result, 5)

    def test_divide_mixed_signs(self):
        """Test division with mixed signs."""
        result = self.calc.divide(-20, 4)
        self.assertEqual(result, -5)

    def test_divide_floats(self):
        """Test division with floats."""
        result = self.calc.divide(7.5, 2.5)
        self.assertEqual(result, 3.0)

    def test_divide_by_zero_raises_error(self):
        """Test that division by zero raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_divide_zero_by_number(self):
        """Test dividing zero by a number."""
        result = self.calc.divide(0, 5)
        self.assertEqual(result, 0)

    # Input Validation Tests
    def test_add_invalid_first_argument(self):
        """Test that invalid first argument raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.add("5", 3)

    def test_add_invalid_second_argument(self):
        """Test that invalid second argument raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.add(5, "3")

    def test_multiply_invalid_arguments(self):
        """Test that invalid arguments raise TypeError."""
        with self.assertRaises(TypeError):
            self.calc.multiply([1, 2], 3)

    # State Management Tests
    def test_last_result_initially_none(self):
        """Test that last_result is None initially."""
        self.assertIsNone(self.calc.get_last_result())

    def test_last_result_updated(self):
        """Test that last_result is updated after operation."""
        self.calc.add(5, 3)
        self.assertEqual(self.calc.get_last_result(), 8)

    def test_operation_count_initially_zero(self):
        """Test that operation count starts at zero."""
        self.assertEqual(self.calc.get_operation_count(), 0)

    def test_operation_count_increments(self):
        """Test that operation count increments."""
        self.calc.add(1, 1)
        self.calc.subtract(5, 2)
        self.calc.multiply(3, 4)
        self.assertEqual(self.calc.get_operation_count(), 3)

    def test_reset_clears_state(self):
        """Test that reset clears calculator state."""
        self.calc.add(5, 3)
        self.calc.reset()
        self.assertIsNone(self.calc.get_last_result())
        self.assertEqual(self.calc.get_operation_count(), 0)

    # Edge Cases
    def test_very_large_numbers(self):
        """Test with very large numbers."""
        result = self.calc.add(1e15, 1e15)
        self.assertEqual(result, 2e15)

    def test_very_small_numbers(self):
        """Test with very small numbers."""
        result = self.calc.add(1e-15, 1e-15)
        self.assertAlmostEqual(result, 2e-15, places=20)


class TestCalculatorIntegration(unittest.TestCase):
    """Integration tests for Calculator."""

    def test_chained_operations(self):
        """Test chained operations using last result."""
        calc = Calculator()
        calc.add(5, 3)  # 8
        first = calc.get_last_result()

        calc.multiply(first, 2)  # 16
        second = calc.get_last_result()

        calc.divide(second, 4)  # 4
        final = calc.get_last_result()

        self.assertEqual(final, 4.0)
        self.assertEqual(calc.get_operation_count(), 3)


def run_tests():
    """Run the test suite and display results."""
    print("\n" + "="*70)
    print("CALCULATOR TEST SUITE")
    print("Agent: tester")
    print("="*70 + "\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorIntegration))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")

    print("="*70 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
