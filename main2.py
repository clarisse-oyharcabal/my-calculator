from functions import custom_calculator, menu

def main():
    while True:
        expression = input("Enter an expression: ")
        try:
            result = custom_calculator(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(e)
        again = input("Would you like to perform another calculation? (yes/no): ").strip().lower()
        if again != "yes":
            break

if __name__ == "__main__":
    main()
    