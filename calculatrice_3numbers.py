history = []  # Stores the calculation history

def display_menu():
    print("\n📖 Main Menu 📖:")
    print("1. 🔢 Perform a calculation")
    print("2. 🌱 Calculate the square root of a number")
    print("3. 💭 Display history")
    print("4. ❌ Clear history")
    print("5. ⛷️ Exit\n")

def input_validator():
    # Input the first number and ensure it's valid
    while True:
        try:
            num1 = float(input("Enter the first number (integer or decimal): "))
            break
        except ValueError:
            print("Please enter a valid number (integer or decimal).")

    # Input the first operator and ensure it's valid
    while True:
        operator1 = input("Enter the first operator (+, -, *, /, ^): ").strip().lower()
        if operator1 not in ["+", "-", "*", "/", "^"]:
            print("Invalid operator.")
            continue
        else:
            break

    # Input the second number and check for division by zero
    while True:
        try:
            num2 = float(input("Enter the second number (integer or decimal): "))
            if operator1 == "/" and num2 == 0:
                print("Cannot divide by zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    return num1, operator1, num2

def perform_calculation(num1, operator, num2):
    # Perform the calculation based on the operator
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    elif operator == "^":
        return num1 ** num2

def perform_priority_calculation(num1, operator1, num2, operator2, num3):
    # Define operator precedence
    priorities = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}

    # Perform calculation based on operator precedence
    if priorities[operator1] > priorities[operator2]:
        result1 = perform_calculation(num1, operator1, num2)
        result2 = perform_calculation(result1, operator2, num3)
        return result2
    else:
        result1 = perform_calculation(num2, operator2, num3)
        result2 = perform_calculation(num1, operator1, result1)
        return result2

def print_result():
    num1, operator1, num2 = input_validator()  # Get valid inputs
    operator2 = input("Enter the second operator (+, -, *, /, ^): ").strip().lower()  # Input second operator

    while operator2 not in ["+", "-", "*", "/", "^"]:
        print("Invalid operator.")
        operator2 = input("Enter the second operator (+, -, *, /, ^): ").strip().lower()

    # Input the third number
    while True:
        try:
            num3 = float(input("Enter the third number: "))
            if (operator2 == "/" or operator1 == "/") and num3 == 0:
                print("Cannot divide by zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Perform calculation with priority
    result = perform_priority_calculation(num1, operator1, num2, operator2, num3)
    
    # Display the result and save it in history
    equation = f"{num1} {operator1} {num2} {operator2} {num3}"
    print(f"The result of {equation} is: {result}")
    history.append(f"{equation} = {result}")

def restart_calculation():
    while True:
        print_result()  # Perform and display calculation
        while True:
            restart = input("Would you like to perform another calculation? (y to repeat, n to return to the menu): ").strip().lower()
            if restart == 'y':
                break
            elif restart == 'n':
                return  # Return to the main menu
            else:
                print("Invalid input. Please enter 'y' to repeat or 'n' to return to the menu.")

def calculate_square_root():
    while True:
        try:
            num = float(input("Enter a number to calculate its square root: "))
            if num < 0:
                print("Cannot calculate the square root of a negative number.")
                continue
            square_root = num ** 0.5
            print(f"The square root of {num} is: {square_root}")
            history.append(f"√{num} = {square_root}")
            break
        except ValueError:
            print("Please enter a valid number.")

def restart_square_root():
    while True:
        calculate_square_root()  # Perform square root calculation
        while True:
            restart = input("Would you like to calculate another square root? (y to repeat, n to return to the menu): ").strip().lower()
            if restart == 'y':
                break
            elif restart == 'n':
                return  # Return to the main menu
            else:
                print("Invalid input. Please enter 'y' to repeat or 'n' to return to the menu.")

def print_history():
    if not history:
        print("No history to display because it is empty.")
    else:
        print("\n=== Calculation History: ===")
        for calc in history:
            print(calc)

def clear_history():
    if not history:
        print("No history to clear.")
    else:
        history.clear()
        print("History cleared.")

def main():
    print("🧮 Welcome to My Calculator! :")
    while True:
        display_menu()  # Display the menu
        choice = input("Choose an option (1-5): ").strip()
        if choice == '1':
            restart_calculation()  # Option to perform a calculation
        elif choice == '2':
            restart_square_root()  # Option to calculate a square root
        elif choice == '3':
            print_history()  # Option to view history
        elif choice == '4':
            clear_history()  # Option to clear history
        elif choice == '5':
            print("Thank you for using the calculator. See you soon! 👋")
            break  # Exit the program
        else:
            print("Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()  # Run the program
