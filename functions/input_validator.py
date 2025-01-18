def input_validator(number_1, operator, number_2=None):
    valid_number_1 = True
    valid_operator = True
    valid_sqrt_operation = True
    valid_number_2 = True
    valid_division_operation = True

    try: 
        number_1 = float(number_1)
    except ValueError:
        print("Error: Please enter a valid number (first number).")
        return number_1, operator, number_2, False, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2

    operator = operator.lower()

    if operator == "r":
        if number_2 is None or number_2.strip() == "":
            if number_1 < 0:
                print("Square root operation is valid only for positive numbers.")
                return number_1, operator, number_2, valid_number_1, valid_operator, False, valid_division_operation, valid_number_2
            print("We are going to calculate the square root of the first number.")
            return number_1, operator, None, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2
        else:
            try:
                number_2 = float(number_2)
            except ValueError:
                print("Error: Please enter a valid number (second number).")
                return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, False
            
            if number_1 < 0:
                print("Square root operation is valid only for positive numbers.")
                return number_1, operator, number_2, valid_number_1, valid_operator, False, valid_division_operation, valid_number_2
            
            print("We are going to calculate the square root of the first number and multiply it by the second number.")
            return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2

    try:
        number_2 = float(number_2)
        if operator == "/" and number_2 == 0:
            print("It is not valid to divide by zero.")
            return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, False, False
    except ValueError:
        print("Error: Please enter a valid number (second number).")
        return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, False

    if operator not in ["+", "-", "*", "/", "r", "e"]:
        print("Invalid operator.")
        return number_1, operator, number_2, valid_number_1, False, valid_sqrt_operation, valid_division_operation, valid_number_2

    return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2