def input_validator(number_1, operator, number_2):

    valid_number_1 = True
    valid_operator = True
    valid_sqrt_operation = True
    valid_number_2 = True
    valid_division_operation = True
    
    
    while True:
        try: 
            number_1 = float(number_1)
            break
        except ValueError:
            print("Error: Please enter a valid number (first number).")
            valid_number_1 = False
            return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2
    

    while valid_operator:    
        operator = operator.lower()
        if operator not in ["+", "-", "*", "/", "r", "e"]:
            print("Invalid operator.")
            valid_operator = False
            return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2
        else:
            break


    while operator == "r":
        if number_1 < 0:
            print("Square root operation is valid only for positive numbers.")
            valid_sqrt_operation = False
            return number_1, operator, None, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2
        print("We are going to remove the second number, as we can only perform the square root operation that way, sorry.")
        #return number_1, operator, None, valid_sqrt_operation
        return number_1, operator, None, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2


    while valid_number_2:
        try:
            number_2 = float(number_2)
            #valid_division_operation = True
            if operator == "/" and number_2 == 0:
                print("It is not valid to divide by zero.")
                valid_number_2 = False
                valid_division_operation = False
                #return valid_number_2, valid_division_operation
                return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2
                #continue
            #elif operator == "r":
            #    print("We are going to remove the second number, as we can only perform the square root operation that way, sorry.")
            #break
        except ValueError:
            print("Error: Please enter a valid number (second number).")
            valid_number_2 = False
            valid_division_operation = True
            #return valid_number_2, valid_division_operation
            return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2
    
    return number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2
    #return number_1, operator, number_2, valid_number_1, valid_operator, valid_division_operation, valid_number_2


########

"""number_1 = "-23"
operator = "r"
number_2 = "0"
print(number_1, operator, number_2)
print(input_validator(number_1, operator, number_2))

number_1, operator, number_2, valid_number_1, valid_operator, valid_sqrt_operator, valid_division_operation, valid_number_2 = input_validator(number_1, operator, number_2)
#number_1, operator, number_2, valid_number_1, valid_operator, valid_division_operation, valid_number_2 = input_validator(number_1, operator, number_2)
print(f"valid_number_1: {valid_number_1}")
print(f"valid_operator: {valid_operator}")
print(f"valid_sqrt_operation: {valid_sqrt_operator}")
print(f"valid_division_operation: {valid_division_operation}")
print(f"valid_number_2: {valid_number_2}")"""