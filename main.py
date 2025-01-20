from functions import intro, input_operation, input_validator, parse, calculate, print_results, save_to_history, view_history, clear_history

def menu():
    while True:
        print("\nMenu:")
        print("1. Perform a calculation")
        print("2. View history")
        print("3. Clear history")
        print("4. Exit")
        
        choice = input("Please choose an option (1-4): ")
        
        if choice == "1":
            perform_calculation()
        elif choice == "2":
            view_history()
        elif choice == "3":
            clear_history()
            print("History cleared.")
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Invalid choice. Please choose a valid option (1-4).")

def perform_calculation():
    while True:
        operation = input_operation()
        number_1, operator, number_2 = parse(operation)
        
        validated = input_validator(number_1, operator, number_2)
        
        number_1, operator, number_2 = validated[:3]
        valid_number_1, valid_operator, valid_sqrt_operation, valid_division_operation, valid_number_2 = validated[3:]
        
        if valid_number_1 and valid_number_2 and valid_operator and valid_sqrt_operation and valid_division_operation:
            result = calculate((number_1, operator, number_2))
            print_results((result))
            save_to_history(operation, result)
            
            again = input("Would you like to perform another calculation? (yes/no): ").strip().lower()
            if again != "yes":
                break
        else:
            print("Please, try again.")

# Call the menu function to start the program
intro()
menu()
