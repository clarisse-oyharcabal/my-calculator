def print_results(result):
    # Ensure the result is a list or tuple with four elements
    if isinstance(result, (list, tuple)) and len(result) == 4:
        number_1, operator, number_2, output = result

        if operator == "+":
            print(f"The sum of {number_1} and {number_2} is {output}.")
        elif operator == "-":
            print(f"The difference between {number_1} and {number_2} is {output}.")
        elif operator == "*":
            print(f"The product of {number_1} and {number_2} is {output}.")
        elif operator == "/":
            print(f"The division of {number_1} by {number_2} is {output}.")
        elif operator == "e":
            print(f"{number_1} raised to the power of {number_2} is {output}.")
        elif operator == "r":
            if number_2 is None:
                print(f"The square root of {number_1} is {output}.")
            else:
                print(f"The square root of {number_1} is {number_1**0.5}, multiplied by {number_2}, is {output}.")
        else:
            print("Invalid operator. Please try again. (detected in print_results.py)")
    else:
        print("Invalid result. Verify that the operation was performed correctly. (detected in print_results.py)")