import tkinter as tk  # Importing the tkinter library for GUI creation
from tkinter import messagebox  # For displaying message boxes
import json  # For handling history storage in JSON format
import re  # Regular expressions for parsing mathematical expressions
from datetime import datetime  # To timestamp history entries

# File to save calculation history
HISTORY_FILE = "historique.json"

# Function to load history from a JSON file
def load_history():
    try:
        # Try to open the file and load its content as a JSON object
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file does not exist, return an empty list
        return []

# Function to save history to a JSON file
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        # Dump the history list into the JSON file
        json.dump(history, f)

def evaluate_expression(expression):
    try:
        # Tokenize the expression
        tokens = re.findall(r"\d+\.?\d*|[+\-*/()]", expression)

        # Handle negative numbers: Merge "-" with numbers when appropriate
        fixed_tokens = []
        for i, token in enumerate(tokens):
            if token == "-" and (i == 0 or tokens[i - 1] in "+-*/("):
                # Merge the '-' with the next number
                fixed_tokens.append(token + tokens[i + 1])
            elif i > 0 and tokens[i - 1] == "-" and tokens[i - 2] in "+-*/(":
                # Skip the number since it's already merged
                continue
            else:
                fixed_tokens.append(token)

        # Evaluate the corrected token list
        result = evaluate_tokens(fixed_tokens)
        return result
    except Exception as e:
        print(f"Error evaluating expression: {e}")  # Debug message
        return "Error"


# Function to evaluate tokens manually
def evaluate_tokens(tokens):
    def apply_operation(op, b, a):
        # Perform the operation based on the operator
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return a / b if b != 0 else "Error"  # Handle division by zero

    # Define operator priorities
    priorities = {"+": 1, "-": 1, "*": 2, "/": 2}
    values = []  # Stack to store numeric values
    operators = []  # Stack to store operators

    def resolve():
        # Apply the operator to the top two numbers on the stack
        b = values.pop()
        a = values.pop()
        op = operators.pop()
        values.append(apply_operation(op, b, a))

    for token in tokens:
        if token.isdigit():  # If the token is a number
            values.append(float(token))  # Convert to float and add to values stack
        elif token in priorities:  # If the token is an operator
            while operators and priorities.get(operators[-1], 0) >= priorities[token]:
                resolve()  # Resolve higher-priority operators first
            operators.append(token)
        elif token == "(":  # Handle opening parentheses
            operators.append(token)
        elif token == ")":  # Handle closing parentheses
            while operators and operators[-1] != "(":
                resolve()
            operators.pop()  # Remove the '('

    while operators:
        resolve()  # Resolve remaining operators

    return values[0]  # Return the final result

# Main application class
class CalculatorApp:
    def __init__(self, root):
        self.root = root  # Reference to the root window
        self.root.title("Advanced Calculator with Background")  # Set window title
        self.root.geometry("400x600")  # Set initial size of the window

        self.expression = ""  # Initialize the input expression
        self.history = load_history()  # Load calculation history

        # Add background image
        self.bg_image = tk.PhotoImage(file="background.png")  # Load the image file
        self.bg_label = tk.Label(root, image=self.bg_image)  # Create a label for the image
        self.bg_label.place(relwidth=1, relheight=1)  # Place it to fill the window

        # Entry widget for displaying expressions and results
        self.display = tk.Entry(root, font=("Arial", 24), justify="right")
        self.display.pack(pady=20, padx=10, fill="x")  # Pack the entry at the top

        # Frame to hold buttons
        self.buttons_frame = tk.Frame(root, bg="lightgray")  # Frame with a background color
        self.buttons_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Define buttons with text and their grid positions
        buttons = [
            ("(", 0, 0), (")", 0, 1), ("C", 0, 2), ("History", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("Quit", 5, 0, 4),  # Span across all columns for Quit button
        ]

        # Create and place buttons in the grid
        for btn in buttons:
            text, row, col = btn[:3]  # Get button text and position
            colspan = btn[3] if len(btn) > 3 else 1  # Check if column span is specified
            button = tk.Button(
                self.buttons_frame,
                text=text,
                font=("Arial", 18),
                command=lambda t=text: self.on_button_click(t),  # Bind button click event
                bg="white",  # Set button background color
                fg="black"  # Set button text color
            )
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        # Configure grid rows and columns to resize dynamically
        for i in range(6):  # 6 rows
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 columns
            self.buttons_frame.grid_columnconfigure(i, weight=1)

    # Handle button click events
    def on_button_click(self, text):
        if text == "=":  # If "=" is clicked
            result = evaluate_expression(self.expression)  # Evaluate the expression
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
            # Save the result in the history
            self.history.append(f"{timestamp} : {self.expression} = {result}")
            self.history = self.history[-10:]  # Keep only the last 10 entries
            save_history(self.history)  # Save history to file
            self.display.delete(0, tk.END)  # Clear the display
            self.display.insert(0, str(result))  # Show the result
            self.expression = ""  # Reset the expression
        elif text == "C":  # If "C" is clicked
            self.expression = ""  # Clear the current expression
            self.display.delete(0, tk.END)  # Clear the display
        elif text == "History":  # If "History" is clicked
            # Show the history in a message box
            messagebox.showinfo("History", "\n".join(self.history))
        elif text == "Quit":  # If "Quit" is clicked
            self.root.quit()  # Exit the application
        else:
            # Append the clicked button's text to the expression
            self.expression += text
            self.display.delete(0, tk.END)  # Clear the display
            self.display.insert(0, self.expression)  # Update the display with the new expression

# Run the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = CalculatorApp(root)  # Instantiate the calculator app
    root.mainloop()  # Run the Tkinter event loop
