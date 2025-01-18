def sqrt(number_1, number_2=None):
    if number_2 is None:
        result = number_1 ** 0.5
        return (number_1, "r", None, result)
    else:
        try:
            number_2 = float(number_2)
            result = (number_1 ** 0.5) * number_2
            return (number_1, "r", number_2, result)
        except ValueError:
            return "Invalid operation (detected in sqrt.py)"