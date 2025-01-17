from multiplication import multiplication
from division import division
from exponentiation import exponentiation
from sqrt import sqrt


from subtraction import subtraction
from addition import addition

def calculate(operation):
    
    print(operation)
    print(operator)
    
    match operator:
        case "r":
            operation = sqrt(number_1, number_2)
            return operation
        case "e":
            operation = exponentiation(number_1, number_2)
            return operation
        case "/":
            operation = division(number_1, number_2)
            return operation
        case "*":
            operation = multiplication(number_1, number_2)
            return operation
        case "-":
            operation = subtraction(number_1, number_2)
            return operation
        case "+":
            operation = addition(number_1, number_2)
            return operation
        
    return


"""number_1 = 10.0
operator = "r"
number_2 = None
operation = (number_1, operator, number_2)
print(calculate(operation))"""