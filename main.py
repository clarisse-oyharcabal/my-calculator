from functions import intro, input_operation, input_validator, parse, calculate, print_results


def main():
    intro()
    
    while True:
        operation = input_operation()
        number_1, operator, number_2 = parse(operation)
        
        validated = input_validator(number_1, operator, number_2)
        
        number_1, operator, number_2 = validated[:3]
        valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2 = validated[3:]
        
        if valid_number_1 and valid_number_2 and valid_operator and valid_sqrt_operation and valid_division_operation:
            result = calculate((number_1, operator, number_2))
            print_results((result))
        else:
            print("Please, try again.")

main()