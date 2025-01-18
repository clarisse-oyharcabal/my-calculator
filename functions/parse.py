def parse(operation):
    operation = operation.strip().lower()
    
    number_1 = ""
    operator = ""
    number_2 = ""
    operator_found = False
    
    if operation[0] == "-":
        number_1 = operation[0]
        operation = operation[1:]

    for char in operation:
        if char in "+-*/er" and not operator_found:
            operator = char
            operator_found = True
        elif not operator_found:
            number_1 += char
        else:
            number_2 += char
    
    return number_1, operator, number_2