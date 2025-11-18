/**
 * Simple Calculator Application
 * Handles basic arithmetic operations: addition, subtraction, multiplication, division, and modulo
 */

class Calculator {
    constructor(previousOperandElement, currentOperandElement) {
        this.previousOperandElement = previousOperandElement;
        this.currentOperandElement = currentOperandElement;
        this.clear();
    }

    /**
     * Clears all calculator state and resets display
     */
    clear() {
        this.currentOperand = '0';
        this.previousOperand = '';
        this.operation = undefined;
        this.shouldResetDisplay = false;
    }

    /**
     * Deletes the last digit from current operand
     */
    delete() {
        if (this.currentOperand === '0') return;

        if (this.currentOperand.length === 1) {
            this.currentOperand = '0';
        } else {
            this.currentOperand = this.currentOperand.slice(0, -1);
        }
    }

    /**
     * Appends a number or decimal point to the current operand
     * @param {string} number - The number or decimal point to append
     */
    appendNumber(number) {
        // Reset display if needed (after operation)
        if (this.shouldResetDisplay) {
            this.currentOperand = '0';
            this.shouldResetDisplay = false;
        }

        // Only allow one decimal point
        if (number === '.' && this.currentOperand.includes('.')) return;

        // Replace initial zero with number (unless adding decimal)
        if (this.currentOperand === '0' && number !== '.') {
            this.currentOperand = number;
        } else {
            this.currentOperand += number;
        }
    }

    /**
     * Selects an operation and stores the current operand
     * @param {string} operation - The operation to perform (+, -, *, /, %)
     */
    chooseOperation(operation) {
        // Don't allow operation if current operand is empty (except for negative numbers)
        if (this.currentOperand === '') return;

        // If there's already a previous operand, compute the result first
        if (this.previousOperand !== '') {
            this.compute();
        }

        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.currentOperand = '';
    }

    /**
     * Performs the arithmetic operation
     */
    compute() {
        let computation;
        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);

        // Validate that both operands are valid numbers
        if (isNaN(prev) || isNaN(current)) return;

        // Perform the appropriate operation
        switch (this.operation) {
            case '+':
                computation = prev + current;
                break;
            case '-':
                computation = prev - current;
                break;
            case '*':
                computation = prev * current;
                break;
            case '/':
                // Handle division by zero
                if (current === 0) {
                    alert('Cannot divide by zero');
                    this.clear();
                    return;
                }
                computation = prev / current;
                break;
            case '%':
                computation = prev % current;
                break;
            default:
                return;
        }

        // Update state with result
        this.currentOperand = this.roundResult(computation).toString();
        this.operation = undefined;
        this.previousOperand = '';
        this.shouldResetDisplay = true;
    }

    /**
     * Rounds result to avoid floating point precision issues
     * @param {number} number - The number to round
     * @returns {number} - Rounded number
     */
    roundResult(number) {
        // Round to 10 decimal places to avoid floating point errors
        return Math.round(number * 10000000000) / 10000000000;
    }

    /**
     * Formats number for display with proper comma separation
     * @param {string} number - The number to format
     * @returns {string} - Formatted number string
     */
    getDisplayNumber(number) {
        const stringNumber = number.toString();
        const integerDigits = parseFloat(stringNumber.split('.')[0]);
        const decimalDigits = stringNumber.split('.')[1];
        let integerDisplay;

        if (isNaN(integerDigits)) {
            integerDisplay = '';
        } else {
            // Add comma separators for thousands
            integerDisplay = integerDigits.toLocaleString('en', {
                maximumFractionDigits: 0
            });
        }

        if (decimalDigits != null) {
            return `${integerDisplay}.${decimalDigits}`;
        } else {
            return integerDisplay;
        }
    }

    /**
     * Updates the calculator display
     */
    updateDisplay() {
        this.currentOperandElement.textContent =
            this.getDisplayNumber(this.currentOperand);

        if (this.operation != null) {
            // Show previous operand with operation symbol
            const operationSymbols = {
                '+': '+',
                '-': '−',
                '*': '×',
                '/': '÷',
                '%': '%'
            };
            this.previousOperandElement.textContent =
                `${this.getDisplayNumber(this.previousOperand)} ${operationSymbols[this.operation]}`;
        } else {
            this.previousOperandElement.textContent = '';
        }
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const previousOperandElement = document.getElementById('previous-operand');
    const currentOperandElement = document.getElementById('current-operand');

    const calculator = new Calculator(previousOperandElement, currentOperandElement);

    // Number button event listeners
    document.querySelectorAll('[data-number]').forEach(button => {
        button.addEventListener('click', () => {
            calculator.appendNumber(button.dataset.number);
            calculator.updateDisplay();
        });
    });

    // Operator button event listeners
    document.querySelectorAll('[data-operator]').forEach(button => {
        button.addEventListener('click', () => {
            calculator.chooseOperation(button.dataset.operator);
            calculator.updateDisplay();
        });
    });

    // Action button event listeners
    document.querySelectorAll('[data-action]').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;

            if (action === 'clear') {
                calculator.clear();
            } else if (action === 'delete') {
                calculator.delete();
            } else if (action === 'equals') {
                calculator.compute();
            }

            calculator.updateDisplay();
        });
    });

    // Keyboard support
    document.addEventListener('keydown', (e) => {
        // Numbers and decimal
        if ((e.key >= '0' && e.key <= '9') || e.key === '.') {
            calculator.appendNumber(e.key);
            calculator.updateDisplay();
        }

        // Operators
        if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/' || e.key === '%') {
            calculator.chooseOperation(e.key);
            calculator.updateDisplay();
        }

        // Enter or equals
        if (e.key === 'Enter' || e.key === '=') {
            e.preventDefault();
            calculator.compute();
            calculator.updateDisplay();
        }

        // Backspace
        if (e.key === 'Backspace') {
            e.preventDefault();
            calculator.delete();
            calculator.updateDisplay();
        }

        // Escape or clear
        if (e.key === 'Escape') {
            calculator.clear();
            calculator.updateDisplay();
        }
    });

    // Initial display update
    calculator.updateDisplay();
});
