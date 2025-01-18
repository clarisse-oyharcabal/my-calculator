from functions import addition, division, multiplication, subtraction, sqrt, exponentiation

def calculate(operation):
    number_1, operator, number_2 = operation
    if operator == "+":
        return addition(number_1, number_2)
    elif operator == "-":
        return subtraction(number_1, number_2)
    elif operator == "*":
        return multiplication(number_1, number_2)
    elif operator == "/":
        return division(number_1, number_2)
    elif operator == "e":
        return exponentiation(number_1, number_2)
    elif operator == "r":
        return sqrt(number_1, number_2)
    else:
        return "Invalid operator. (detected in calculate.py)"