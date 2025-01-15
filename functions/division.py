def division(number_1, number_2):
    if number_2 == 0:
        operation = "Zero is not a valid value in a division."
    else:
        result = number_1 / number_2
        operation = [number_1, '/', number_2, result]
    return operation