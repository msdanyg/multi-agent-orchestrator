# Simple Calculator Application

**Built by Multi-Agent System**
- 🤖 **code_analyst**: Architecture design
- 🤖 **code_writer**: Implementation
- 🤖 **tester**: Testing and validation
- 🤖 **docs_writer**: Documentation

## Overview

A clean, well-tested Python calculator with basic arithmetic operations (addition, subtraction, multiplication, division). Features comprehensive error handling, input validation, and a user-friendly CLI interface.

## Features

✅ **Four Basic Operations**: Add, subtract, multiply, divide
✅ **Type Safety**: Full type hints and validation
✅ **Error Handling**: Division by zero protection
✅ **State Tracking**: Last result and operation count
✅ **31 Unit Tests**: 100% test coverage
✅ **CLI Interface**: Interactive command-line interface

## Quick Start

### Run the Calculator

```bash
python3 calculator_cli.py
```

### Use as a Library

```python
from calculator import Calculator

calc = Calculator()

result = calc.add(5, 3)        # 8
result = calc.subtract(10, 4)  # 6
result = calc.multiply(6, 7)   # 42
result = calc.divide(20, 4)    # 5.0

print(calc.get_last_result())     # 5.0
print(calc.get_operation_count()) # 4
```

### Run Tests

```bash
python3 test_calculator.py
```

## File Structure

```
├── calculator.py           # Core Calculator class
├── calculator_cli.py       # Command-line interface
├── test_calculator.py      # Unit tests (31 tests)
├── calculator_design.md    # Architecture documentation
└── README_CALCULATOR.md    # This file
```

## API Reference

### Calculator Class

#### Methods

**`add(a, b)`**
- Adds two numbers
- Returns: Sum of a and b
- Raises: TypeError if inputs are not numeric

**`subtract(a, b)`**
- Subtracts b from a
- Returns: Difference of a and b
- Raises: TypeError if inputs are not numeric

**`multiply(a, b)`**
- Multiplies two numbers
- Returns: Product of a and b
- Raises: TypeError if inputs are not numeric

**`divide(a, b)`**
- Divides a by b
- Returns: Quotient of a and b
- Raises: TypeError if inputs are not numeric, ZeroDivisionError if b is zero

**`get_last_result()`**
- Returns: Result of the last operation, or None

**`get_operation_count()`**
- Returns: Total number of operations performed

**`reset()`**
- Resets calculator state (last result and operation count)

## Usage Examples

### Basic Operations

```python
calc = Calculator()

# Addition
result = calc.add(10, 5)
print(result)  # 15

# Subtraction
result = calc.subtract(10, 5)
print(result)  # 5

# Multiplication
result = calc.multiply(10, 5)
print(result)  # 50

# Division
result = calc.divide(10, 5)
print(result)  # 2.0
```

### Working with Floats

```python
calc = Calculator()

result = calc.add(2.5, 3.7)      # 6.2
result = calc.multiply(2.5, 4.0) # 10.0
result = calc.divide(7.5, 2.5)   # 3.0
```

### Error Handling

```python
calc = Calculator()

# Division by zero
try:
    calc.divide(10, 0)
except ZeroDivisionError as e:
    print(f"Error: {e}")  # Error: Cannot divide by zero

# Invalid input
try:
    calc.add("5", 3)
except TypeError as e:
    print(f"Error: {e}")  # Error: First argument must be numeric...
```

### Tracking State

```python
calc = Calculator()

calc.add(5, 3)
calc.multiply(10, 2)
calc.subtract(15, 5)

print(f"Last result: {calc.get_last_result()}")     # 10
print(f"Operations: {calc.get_operation_count()}")  # 3

calc.reset()
print(f"After reset: {calc.get_last_result()}")     # None
```

### Chained Operations

```python
calc = Calculator()

# Use last result for calculations
calc.add(5, 3)              # 8
last = calc.get_last_result()

calc.multiply(last, 2)      # 16
last = calc.get_last_result()

calc.divide(last, 4)        # 4
print(calc.get_last_result())  # 4.0
```

## CLI Interface

### Menu Options

1. **Add** - Add two numbers
2. **Subtract** - Subtract two numbers
3. **Multiply** - Multiply two numbers
4. **Divide** - Divide two numbers
5. **View last result** - Show result of last operation
6. **View operation count** - Show total operations performed
7. **Reset calculator** - Clear state
8. **Exit** - Quit the application

### Example Session

```
          SIMPLE CALCULATOR
==================================================
Operations:
  1. Add
  2. Subtract
  3. Multiply
  4. Divide
  5. View last result
  6. View operation count
  7. Reset calculator
  8. Exit
==================================================

Select operation (1-8): 1

--- ADD ---
Enter first number: 15
Enter second number: 27
✅ Result: 15.0 + 27.0 = 42.0

Select operation (1-8): 5
📊 Last result: 42.0
```

## Test Coverage

### Test Suite Statistics

- **Total Tests**: 31
- **Success Rate**: 100%
- **Categories**:
  - Addition tests: 5
  - Subtraction tests: 4
  - Multiplication tests: 5
  - Division tests: 6
  - Input validation tests: 4
  - State management tests: 5
  - Edge cases: 2

### Run Tests

```bash
# Run with verbose output
python3 test_calculator.py

# Run specific test
python3 -m unittest test_calculator.TestCalculator.test_add_positive_numbers
```

## Architecture

### Design Principles

1. **Separation of Concerns**: Calculator logic separate from UI
2. **Type Safety**: Full type hints for better IDE support
3. **Error Handling**: Comprehensive validation and error messages
4. **Testability**: Clean interfaces for easy testing
5. **Extensibility**: Easy to add new operations

### Class Structure

```
Calculator
├── Core Operations
│   ├── add(a, b)
│   ├── subtract(a, b)
│   ├── multiply(a, b)
│   └── divide(a, b)
├── State Management
│   ├── get_last_result()
│   ├── get_operation_count()
│   └── reset()
└── Internal Methods
    ├── _validate_input(a, b)
    └── _update_state(result)
```

## Development

### Adding New Operations

To add a new operation:

1. Add method to Calculator class
2. Use `_validate_input()` for validation
3. Use `_update_state()` to track result
4. Add tests in test_calculator.py
5. Update CLI menu and handling

Example:

```python
def power(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Raise a to the power of b."""
    self._validate_input(a, b)
    result = a ** b
    self._update_state(result)
    return result
```

### Code Style

- Follows PEP 8 guidelines
- Type hints for all methods
- Comprehensive docstrings
- Clear error messages

## Troubleshooting

### Common Issues

**Import Error**
```bash
# Make sure you're in the correct directory
cd /path/to/Multi-agent
python3 calculator_cli.py
```

**Test Failures**
```bash
# Ensure calculator.py is in the same directory
ls calculator.py
python3 test_calculator.py
```

## Multi-Agent Development Process

This calculator was built using a multi-agent approach:

1. **code_analyst** analyzed requirements and designed architecture
2. **code_writer** implemented the core Calculator class
3. **code_writer** created the CLI interface
4. **tester** wrote comprehensive unit tests
5. **docs_writer** created documentation

Each agent specialized in their domain, resulting in:
- Clean, maintainable code
- Comprehensive test coverage
- Clear documentation
- Proper error handling

## License

MIT License - Feel free to use and modify

## Credits

**Built by Multi-Agent System**
- Architecture: code_analyst agent
- Implementation: code_writer agent
- Testing: tester agent (31 tests, 100% pass rate)
- Documentation: docs_writer agent

---

**Simple, tested, documented. Ready to use!** ✅
