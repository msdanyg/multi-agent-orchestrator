#!/usr/bin/env python3
"""
Power Function Comprehensive Test Suite
Agent: tester
Task: Thorough validation of power() function implementation
"""
import unittest
import sys
import math
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from calculator import Calculator


class TestPowerBasicFunctionality(unittest.TestCase):
    """Test basic power function operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_power_positive_integers(self):
        """Test power with positive integers."""
        result = self.calc.power(2, 3)
        self.assertEqual(result, 8)

    def test_power_positive_base_higher_exponent(self):
        """Test power with larger exponent."""
        result = self.calc.power(2, 8)
        self.assertEqual(result, 256)

    def test_power_base_10(self):
        """Test power with base 10."""
        result = self.calc.power(10, 3)
        self.assertEqual(result, 1000)

    def test_power_float_base(self):
        """Test power with float base."""
        result = self.calc.power(2.5, 2)
        self.assertEqual(result, 6.25)

    def test_power_float_exponent(self):
        """Test power with float exponent."""
        result = self.calc.power(4, 0.5)
        self.assertEqual(result, 2.0)

    def test_power_both_floats(self):
        """Test power with both float arguments."""
        result = self.calc.power(2.5, 1.5)
        self.assertAlmostEqual(result, 3.952847075210474, places=10)


class TestPowerEdgeCases(unittest.TestCase):
    """Test edge cases for power function."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_power_zero_exponent(self):
        """Test any number to the power of 0 equals 1."""
        result = self.calc.power(5, 0)
        self.assertEqual(result, 1)

        result = self.calc.power(100, 0)
        self.assertEqual(result, 1)

        result = self.calc.power(-5, 0)
        self.assertEqual(result, 1)

    def test_power_one_exponent(self):
        """Test any number to the power of 1 equals itself."""
        result = self.calc.power(7, 1)
        self.assertEqual(result, 7)

        result = self.calc.power(-7, 1)
        self.assertEqual(result, -7)

    def test_power_one_base(self):
        """Test 1 to any power equals 1."""
        result = self.calc.power(1, 5)
        self.assertEqual(result, 1)

        result = self.calc.power(1, 100)
        self.assertEqual(result, 1)

    def test_power_negative_base_positive_exponent(self):
        """Test negative base with positive integer exponent."""
        result = self.calc.power(-2, 3)
        self.assertEqual(result, -8)

        result = self.calc.power(-2, 4)
        self.assertEqual(result, 16)

    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        result = self.calc.power(2, -1)
        self.assertEqual(result, 0.5)

        result = self.calc.power(2, -3)
        self.assertEqual(result, 0.125)

    def test_power_zero_base_positive_exponent(self):
        """Test 0 to a positive power equals 0."""
        result = self.calc.power(0, 5)
        self.assertEqual(result, 0)

        result = self.calc.power(0, 0.5)
        self.assertEqual(result, 0)

    def test_power_zero_base_negative_exponent(self):
        """Test 0 to a negative power raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.power(0, -1)

    def test_power_zero_to_zero_raises_error(self):
        """Test that 0^0 raises ValueError as it's mathematically undefined."""
        with self.assertRaises(ValueError) as context:
            self.calc.power(0, 0)
        self.assertIn("undefined", str(context.exception).lower())


class TestPowerSpecialCases(unittest.TestCase):
    """Test special mathematical cases for power function."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_power_negative_base_fractional_exponent(self):
        """Test negative base with fractional exponent results in complex number."""
        # Python's ** operator returns complex numbers for negative base with fractional exponent
        # This is expected behavior
        result = self.calc.power(-4, 0.5)
        # Result will be a complex number (1.2246467991473532e-16+2j)
        self.assertIsInstance(result, complex)

    def test_power_square_root_equivalence(self):
        """Test that x^0.5 equals square root of x."""
        result = self.calc.power(16, 0.5)
        self.assertEqual(result, 4.0)

        result = self.calc.power(25, 0.5)
        self.assertEqual(result, 5.0)

    def test_power_cube_root_equivalence(self):
        """Test that x^(1/3) equals cube root of x."""
        result = self.calc.power(27, 1/3)
        self.assertAlmostEqual(result, 3.0, places=10)

    def test_power_large_exponent(self):
        """Test power with large exponent."""
        result = self.calc.power(2, 20)
        self.assertEqual(result, 1048576)

    def test_power_very_small_result(self):
        """Test power resulting in very small number."""
        result = self.calc.power(10, -10)
        self.assertEqual(result, 1e-10)


class TestPowerErrorHandling(unittest.TestCase):
    """Test error handling for power function."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_power_invalid_base_string(self):
        """Test that string base raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.power("2", 3)

    def test_power_invalid_exponent_string(self):
        """Test that string exponent raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.power(2, "3")

    def test_power_invalid_base_list(self):
        """Test that list base raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.power([2], 3)

    def test_power_invalid_exponent_none(self):
        """Test that None exponent raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.power(2, None)

    def test_power_invalid_both_arguments(self):
        """Test that invalid arguments for both raise TypeError."""
        with self.assertRaises(TypeError):
            self.calc.power("2", "3")


class TestPowerStateManagement(unittest.TestCase):
    """Test state management integration for power function."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_power_updates_last_result(self):
        """Test that power operation updates last_result."""
        result = self.calc.power(3, 4)
        self.assertEqual(self.calc.get_last_result(), 81)

    def test_power_increments_operation_count(self):
        """Test that power operation increments operation count."""
        initial_count = self.calc.get_operation_count()
        self.calc.power(2, 5)
        self.assertEqual(self.calc.get_operation_count(), initial_count + 1)

    def test_power_multiple_operations_count(self):
        """Test operation count with multiple power operations."""
        self.calc.power(2, 2)
        self.calc.power(3, 3)
        self.calc.power(4, 4)
        self.assertEqual(self.calc.get_operation_count(), 3)

    def test_power_with_other_operations(self):
        """Test power operation mixed with other operations."""
        self.calc.add(5, 5)
        self.calc.power(2, 3)
        self.calc.multiply(3, 4)

        self.assertEqual(self.calc.get_operation_count(), 3)
        self.assertEqual(self.calc.get_last_result(), 12)

    def test_power_chained_with_last_result(self):
        """Test using power with last_result from previous operation."""
        self.calc.add(2, 2)  # 4
        last = self.calc.get_last_result()

        self.calc.power(last, 3)  # 4^3 = 64
        self.assertEqual(self.calc.get_last_result(), 64)

    def test_power_reset_clears_state(self):
        """Test that reset clears state after power operation."""
        self.calc.power(5, 2)
        self.calc.reset()

        self.assertIsNone(self.calc.get_last_result())
        self.assertEqual(self.calc.get_operation_count(), 0)


class TestPowerIntegration(unittest.TestCase):
    """Integration tests for power function with other calculator operations."""

    def test_power_in_complex_calculation(self):
        """Test power as part of complex calculation."""
        calc = Calculator()

        # Calculate: (2^3 + 5) * 2 = (8 + 5) * 2 = 26
        result1 = calc.power(2, 3)  # 8
        result2 = calc.add(result1, 5)  # 13
        result3 = calc.multiply(result2, 2)  # 26

        self.assertEqual(result3, 26)
        self.assertEqual(calc.get_operation_count(), 3)

    def test_power_with_division(self):
        """Test power combined with division."""
        calc = Calculator()

        # Calculate: 2^10 / 2^5 = 1024 / 32 = 32
        result1 = calc.power(2, 10)  # 1024
        result2 = calc.power(2, 5)  # 32
        result3 = calc.divide(result1, result2)  # 32

        self.assertEqual(result3, 32)


def run_power_tests():
    """Run the power function test suite and display results."""
    print("\n" + "="*70)
    print("POWER FUNCTION COMPREHENSIVE TEST SUITE")
    print("Agent: tester")
    print("Task: Thorough validation of power() function implementation")
    print("="*70 + "\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPowerBasicFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestPowerEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPowerSpecialCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPowerErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestPowerStateManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestPowerIntegration))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("POWER FUNCTION TEST SUMMARY")
    print("="*70)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    # Show failures and errors
    if result.failures:
        print("\n" + "-"*70)
        print("FAILURES:")
        print("-"*70)
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)

    if result.errors:
        print("\n" + "-"*70)
        print("ERRORS:")
        print("-"*70)
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback)

    if result.wasSuccessful():
        print("\nStatus: ALL TESTS PASSED")
    else:
        print("\nStatus: SOME TESTS FAILED")

    print("="*70 + "\n")

    return result


if __name__ == "__main__":
    result = run_power_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
