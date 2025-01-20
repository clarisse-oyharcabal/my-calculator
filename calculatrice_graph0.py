import re  # For tokenizing the input expression

# Define operator precedence
OPERATORS = {'+', '-', '*', '/', '^'}
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

def tokenize(expression):
    """Tokenize input expression into numbers and operators."""
    expression = expression.replace(" ", "")  # Remove extra spaces
    # Match numbers (including floating-point) and operators
    tokens = re.findall(r'\d+\.?\d*|[+\-*/^()]', expression)
    return tokens

def shunting_yard(tokens):
    """Convert infix tokens to postfix using the Shunting Yard algorithm."""
    output, stack = [], []
    for token in tokens:
        if re.match(r'^\d+\.?\d*$', token):  # Numbers go directly to output
            output.append(float(token))
        elif token in OPERATORS:
            while (stack and stack[-1] != '(' and 
                   PRECEDENCE.get(stack[-1], 0) >= PRECEDENCE[token]):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Mismatched parentheses.")
            stack.pop()  # Remove '('
    while stack:
        if stack[-1] in "()":
            raise ValueError("Mismatched parentheses.")
        output.append(stack.pop())
    return output

def evaluate_postfix(postfix):
    """Evaluate a postfix expression."""
    stack = []
    for token in postfix:
        if isinstance(token, float):  # Numbers
            stack.append(token)
        elif token in OPERATORS:  # Operators
            if len(stack) < 2:
                raise ValueError("Insufficient operands.")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero is not allowed.")
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)
    if len(stack) != 1:
        raise ValueError("Malformed expression.")
    return stack[0]

def calculate(expression):
    """Evaluate a mathematical expression."""
    try:
        # Validate input before processing
        if not expression or any(c not in "0123456789+-*/^(). " for c in expression):
            return "Error: Invalid characters in expression."
        
        tokens = tokenize(expression)  # Tokenize the input
        if len(tokens) == 0:
            return "Error: Empty expression."

        postfix = shunting_yard(tokens)  # Convert to postfix
        return evaluate_postfix(postfix)  # Evaluate postfix
    except Exception as e:
        return f"Error: {e}"

def main():
    """Main interactive loop."""
    while True:
        # Print instructions after every calculation and before each input
        print("\nWelcome to the Calculator!")
        print("Allowed operations: +, -, *, /, ^ (exponentiation).")
        print("You can use parentheses for grouping, e.g., (2+3)*4.")
        print("Type 'x' to exit the program.")

        expression = input("\nEnter an expression or next operation (x to exit): ").strip()

        if expression.lower() == 'x':  # Exit if user enters 'x'
            print("Goodbye!")
            break
        
        result = calculate(expression)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()