def sqrt(number_1, number_2):
    if number_2 is None:
        result = number_1 ** 0.5
        operation = ["sqrt de ", number_1, result]
    elif isinstance(number_2, float):
        result = (number_1 ** 0.5) * number_2
        operation = ["sqrt de ", number_1, '*', number_2, result]
    return operation

"""number_1 = 16.0
number_2 = None
print(sqrt(number_1, number_2))
"""