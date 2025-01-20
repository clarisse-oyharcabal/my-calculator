from functions import input_operation, input_validator, parse, calculate, print_results, save_to_history, view_history, clear_history, perform_calculation
from functions.perform_calculation import perform_calculation

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