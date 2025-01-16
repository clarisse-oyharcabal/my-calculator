from functions.intro import intro
from functions.input_operation import input_operation
from functions.parse import parse
from functions.input_validator import input_validator
from functions.exponentiation import exponentiation
from functions.multiplication import multiplication
from functions.division import division
from functions.addition import addition
from functions.subtraction import subtraction


def main():
    intro()
    operation = input_operation()
    number_1, operator, number_2 = parse(operation)
    input_validator(number_1, operator, number_2)

main()