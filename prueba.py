from functions.intro import intro
from functions.input_operation import input_operation
from functions.parse import parse
from functions.input_validator import input_validator
from functions.sqrt import sqrt
from functions.exponentiation import exponentiation
from functions.multiplication import multiplication
from functions.division import division
from functions.addition import addition
from functions.subtraction import subtraction
from functions.calculate import calculate


def main():
    intro()
    
    while True:
        operation = input_operation()
        number_1, operator, number_2 = parse(operation)
        validated = input_validator(number_1, operator, number_2)

        print(validated)
        number_1 = validated[0]
        operator = validated[1]
        number_2 = validated[2]
        valid_number_1 = validated[3]
        valid_operator = validated[4]
        valid_sqrt_operation = validated[5]
        valid_division_operation = validated[6]
        valid_number_2 = validated[7]

        while not valid_number_1:
            operation = input_operation()
            number_1, operator, number_2 = parse(operation)
            validated = input_validator(number_1, operator, number_2)
        while not valid_number_2:
            operation = input_operation()
            number_1, operator, number_2 = parse(operation)
            validated = input_validator(number_1, operator, number_2)
        while not valid_operator:
            operation = input_operation()
            number_1, operator, number_2 = parse(operation)
            validated = input_validator(number_1, operator, number_2)
        while not valid_sqrt_operation:
            operation = input_operation()
            number_1, operator, number_2 = parse(operation)
            validated = input_validator(number_1, operator, number_2)
        while not valid_division_operation:
            operation = input_operation()
            number_1, operator, number_2 = parse(operation)
            validated = input_validator(number_1, operator, number_2)
        else:
            operation = number_1, operator, number_2
        return operation
    

main()
