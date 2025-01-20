import re

# Step 1: Validate the elements in the string
def validate_expression(expression):
    valid_chars = "0123456789+-*/() "
    for char in expression:
        if char not in valid_chars:
            raise ValueError(f"Invalid character found: {char}")
    return expression

# Step 2: Convert the string to a list
def convert_to_list(expression):
    elements = re.findall(r'\d+|\+|\-|\*|\/|\(|\)', expression)
    if elements[0] == '-':
        elements[1] = '-' + elements[1]
        elements.pop(0)
    return elements

# Step 3-7: Evaluate the expression step by step
def evaluate_expression(elements):
    def apply_operation(operands, operator):
        b = operands.pop()
        a = operands.pop()
        if operator == '+':
            operands.append(a + b)
        elif operator == '-':
            operands.append(a - b)
        elif operator == '*':
            operands.append(a * b)
        elif operator == '/':
            operands.append(a / b)

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    operators = []
    operands = []

    #print("Steps:")
    i = 0
    while i < len(elements):
        if elements[i].isdigit():
            operands.append(int(elements[i]))
        elif elements[i] in precedence:
            while (operators and operators[-1] in precedence and 
                   precedence[operators[-1]] >= precedence[elements[i]]):
                apply_operation(operands, operators.pop())
            operators.append(elements[i])
        i += 1

    while operators:
        apply_operation(operands, operators.pop())

    #print(f"Result: {operands[0]}")
    return operands[0]

def custom_calculator(expression):
    expression = validate_expression(expression)
    elements = convert_to_list(expression)
    result = evaluate_expression(elements)
    return result
