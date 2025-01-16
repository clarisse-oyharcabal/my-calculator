def parse(operation):
    operation = operation.strip()
    
    number_1 = ""
    operator = ""
    number_2 = ""
    operator_found = False
    
    for char in operation:
        if char in "+-*/e" and not operator_found:
            operator = char
            operator_found = True
        elif not operator_found:
            number_1 += char
        else:
            number_2 += char
    
    #number_1 = float(number_1)
    #number_2 = float(number_2)
    
    return number_1, operator, number_2


"""operation = "365e 5"
number_1, operator, number_2 = parse(operation)

print("number_1:", number_1)
print("operator:", operator)
print("number_2:", number_2)"""