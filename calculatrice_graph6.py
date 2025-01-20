import tkinter as tk  # Import the tkinter library for GUI
from tkinter import messagebox  # Import messagebox for displaying alerts
import json  # Import json for saving and loading history
from datetime import datetime  # Import datetime for timestamping history entries
from PIL import Image, ImageTk  # Import PIL for handling background images

# Configuration
HISTORY_FILE = "historique.json"  # File to store calculation history
BACKGROUND_IMAGE = "background.png"  # Path to the background image
HISTORY_LIMIT = 1000  # Maximum number of history entries to store (increased to 1000)

# Constants for UI (colors and font sizes)
BUTTON_COLORS = {
    "number": "#ffffff",  # White for number buttons
    "operator": "#e8e8e8",  # Light gray for operator buttons
    "clear": "#ffb3b3",  # Light red for clear/delete buttons
    "equals": "#b3ffb3",  # Light green for the equals button
    "letter": "#b3d9ff"  # Light blue for letter buttons (A-L)
}
FONT_SIZES = {
    "normal": 16,  # Normal font size for most buttons (increased)
    "large": 20,  # Larger font size for operator buttons (increased)
    "small": 12  # Smaller font size for letter buttons (reduced)
}

class CalculatorApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root  # Main application window
        self.root.title("Advanced Calculator")  # Set window title
        self.root.geometry("1000x600")  # Set initial window size
        self.root.minsize(800, 500)  # Set minimum window size

        # Initialize variables
        self.expression = ""  # Stores the current expression
        self.letter_values = {}  # Stores values assigned to letters (A-L)
        self.next_letter = 65  # ASCII code for 'A' (used for assigning letters)
        self.history = []  # Stores calculation history
        self.complex_mode = False  # Tracks whether advanced mode is active

        # Load background image
        self.bg_image = Image.open(BACKGROUND_IMAGE)  # Open the background image
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)  # Convert it to a Tkinter-compatible format

        # Create main container with background
        self.canvas = tk.Canvas(self.root)  # Create a canvas for the background
        self.canvas.pack(fill="both", expand=True)  # Make the canvas fill the window
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")  # Add the background image

        # Add explanatory text in the background
        self.canvas.create_text(
            500, 50,  # Position (x, y) of the text
            text="Priorités des opérations :\n"
                 "1. Multiplication (*) et Division (/) sont prioritaires.\n"
                 "2. Addition (+) et Soustraction (-) sont secondaires.\n"
                 "Utilisez des parenthèses () pour imposer vos priorités.",
            font=("Arial", 14, "bold"),  # Font style and size
            fill="white",  # Text color
            anchor="center"  # Center the text
        )

        # Calculator container (frame for calculator buttons and display)
        self.calc_container = tk.Frame(self.canvas, bg="#f5f5f5", bd=2, relief="ridge")
        self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=450, height=550)

        # History container (initially hidden, shown in advanced mode)
        self.history_container = tk.Frame(self.canvas, bg="#f5f5f5", bd=2, relief="ridge")
        self.history_container.place_forget()  # Hide the history container initially

        # Main display (entry widget for showing the expression and result)
        self.display = tk.Entry(
            self.calc_container,
            font=("Arial", 28),  # Larger font size for the display
            justify="right",  # Align text to the right
            bd=3,  # Border width
            relief="ridge",  # Border style
            bg="white"  # Background color
        )
        self.display.pack(padx=15, pady=(20, 15), fill="x")  # Add padding and make it fill horizontally

        # Buttons frame (container for all calculator buttons)
        self.buttons_frame = tk.Frame(self.calc_container, bg="#f0f0f0")
        self.buttons_frame.pack(padx=15, pady=10, fill="both", expand=True)

        # Configure grid for buttons (6 rows, 4 columns)
        for i in range(6):  # Configure rows
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):  # Configure columns
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Define buttons and their positions
        buttons = [
            ("(", 0, 0, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Open parenthesis
            (")", 0, 1, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Close parenthesis
            ("CLR", 0, 2, BUTTON_COLORS["clear"], FONT_SIZES["normal"]),  # Clear button
            ("⌫", 0, 3, BUTTON_COLORS["clear"], FONT_SIZES["normal"]),  # Backspace button
            ("7", 1, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 7
            ("8", 1, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 8
            ("9", 1, 2, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 9
            ("÷", 1, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Division
            ("4", 2, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 4
            ("5", 2, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 5
            ("6", 2, 2, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 6
            ("×", 2, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Multiplication
            ("1", 3, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 1
            ("2", 3, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 2
            ("3", 3, 2, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 3
            ("−", 3, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Subtraction
            ("0", 4, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Number 0
            (".", 4, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),  # Decimal point
            ("=", 4, 2, BUTTON_COLORS["equals"], FONT_SIZES["large"]),  # Equals button
            ("+", 4, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Addition
        ]

        # Create buttons and add them to the grid
        for text, row, col, color, size in buttons:
            self.create_button(text, row, col, color, size)

        # Advanced mode buttons (√, ^, exp, e)
        self.advanced_buttons = [
            ("√", 5, 0, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Square root
            ("^", 5, 1, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Power
            ("exp", 5, 2, BUTTON_COLORS["operator"], FONT_SIZES["large"]),  # Exponential
            ("e", 5, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"])  # Euler's number
        ]

        # Create advanced buttons and hide them initially
        self.advanced_button_widgets = []
        for text, row, col, color, size in self.advanced_buttons:
            btn = self.create_button(text, row, col, color, size)
            self.advanced_button_widgets.append(btn)
            btn.grid_remove()  # Hide advanced buttons initially

        # Letter buttons (A-L, used in advanced mode)
        self.letter_buttons = []
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        for i, letter in enumerate(letters):
            row = 6 + (i // 4)  # Distribute letters across two rows
            col = i % 4  # 4 columns for letters
            btn = self.create_button(letter, row, col, BUTTON_COLORS["letter"], FONT_SIZES["small"])
            self.letter_buttons.append(btn)
            btn.grid_remove()  # Hide letter buttons initially

        # History display (text widget for showing history)
        self.history_display = tk.Text(
            self.history_container,
            height=20,  # Height of the history display
            font=("Arial", 12),  # Font size
            bg="white",  # Background color
            state='disabled',  # Disable editing
            wrap="word"  # Wrap text by words
        )
        self.history_display.pack(padx=15, pady=15, fill="both", expand=True)

        # History scrollbar (for scrolling through history)
        self.history_scrollbar = tk.Scrollbar(
            self.history_container,
            command=self.history_display.yview
        )
        self.history_display.config(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.pack(side="right", fill="y")

        # Clear history button
        self.clear_history_btn = tk.Button(
            self.history_container,
            text="Clear History",
            font=("Arial", 12),
            bg=BUTTON_COLORS["clear"],
            command=self.clear_history,
            bd=2,
            relief="raised",
            padx=8,
            pady=4,
            cursor="hand2"
        )
        self.clear_history_btn.pack(side="bottom", pady=10)

        # Toggle button (switches between simple and advanced modes)
        self.toggle_button = tk.Button(
            self.canvas,
            text="Advanced Mode",
            font=("Arial", 14),
            bg="#b3d9ff",
            command=self.toggle_mode,
            bd=2,
            relief="raised",
            padx=8,
            pady=6,
            cursor="hand2"
        )
        self.toggle_button.place(relx=0.5, rely=0.9, anchor="center")  # Position the toggle button

        # Bind keyboard events
        self.root.bind("<Key>", self.on_key_press)

        # Bind resize event (to handle window resizing)
        self.root.bind("<Configure>", self.on_resize)

        # Load history from file
        self.load_history()

    def create_button(self, text, row, col, color, size):
        """Create a button with hover effect"""
        button = tk.Button(
            self.buttons_frame,
            text=text,
            font=("Arial", size),
            command=lambda t=text: self.on_button_click(t),
            bg=color,
            fg="black",
            bd=2,
            relief="raised",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        button.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        # Add hover effect (darker shade when mouse is over the button)
        hover_color = self.get_darker_shade(color)
        button.bind("<Enter>", lambda e, btn=button, c=hover_color: btn.configure(bg=c))
        button.bind("<Leave>", lambda e, btn=button, c=color: btn.configure(bg=c))

        return button

    def get_darker_shade(self, color):
        """Convert color to darker shade"""
        r = int(color[1:3], 16)  # Extract red component
        g = int(color[3:5], 16)  # Extract green component
        b = int(color[5:7], 16)  # Extract blue component
        factor = 0.8  # Darken the color by 20%
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"  # Return the darker color in hex format

    def on_resize(self, event):
        """Handle window resize"""
        width = self.root.winfo_width()  # Get current window width
        height = self.root.winfo_height()  # Get current window height

        # Resize background image to fit the window
        resized_image = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Adjust calculator and history container positions
        if self.complex_mode:
            self.calc_container.place(relx=0.3, rely=0.5, anchor="center", width=450, height=550)
            self.history_container.place(relx=0.7, rely=0.5, anchor="center", width=450, height=550)
        else:
            self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=450, height=550)

    def toggle_mode(self):
        """Toggle between simple and advanced modes"""
        self.complex_mode = not self.complex_mode

        if self.complex_mode:
            self.toggle_button.config(text="Simple Mode")  # Update toggle button text
            self.history_container.place(relx=0.7, rely=0.5, anchor="center", width=450, height=550)
            for btn in self.advanced_button_widgets:
                btn.grid()  # Show advanced buttons
            for btn in self.letter_buttons:
                btn.grid()  # Show letter buttons
        else:
            self.toggle_button.config(text="Advanced Mode")
            self.history_container.place_forget()  # Hide history container
            for btn in self.advanced_button_widgets:
                btn.grid_remove()  # Hide advanced buttons
            for btn in self.letter_buttons:
                btn.grid_remove()  # Hide letter buttons
            self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=450, height=550)

    def load_history(self):
        """Load history and letter assignments from file"""
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):  # Check if data is a dictionary
                    self.history = data.get("history", [])  # Load history
                    self.letter_values = data.get("letter_values", {})  # Load letter values
                elif isinstance(data, list):  # If data is a list, assign defaults
                    self.history = data
                    self.letter_values = {}
                else:
                    self.history = []
                    self.letter_values = {}

                # Find the next available letter
                used_letters = set(self.letter_values.keys())
                for letter in 'ABCDEFGHIJKL':
                    if letter not in used_letters:
                        self.next_letter = ord(letter)  # Set the next available letter
                        break
        except FileNotFoundError:
            self.history = []  # If file doesn't exist, initialize empty history
            self.letter_values = {}
            self.next_letter = 65  # Start with 'A'

    def save_history(self):
        """Save history and letter assignments to file"""
        data = {
            "history": self.history,
            "letter_values": self.letter_values
        }
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f)

    def update_history_display(self):
        """Update the history display with letter assignments"""
        self.history_display.config(state='normal')  # Enable editing
        self.history_display.delete(1.0, tk.END)  # Clear the display
        for record in self.history:
            self.history_display.insert(tk.END, f"{record}\n")  # Show history entries
        self.history_display.config(state='disabled')  # Disable editing

    def calculate(self, expression):
        """
        Safe calculator implementation without eval()
        Handles: +, -, *, /, (), ^, √, exp, e, and numbers
        """
        def tokenize(expr):
            """Convert expression into tokens (numbers and operators)"""
            tokens = []
            current_number = ''

            for char in expr:
                if char.isdigit() or char == '.':
                    current_number += char  # Build the current number
                else:
                    if current_number:
                        tokens.append(float(current_number))  # Add the number to tokens
                        current_number = ''
                    if char != ' ':
                        tokens.append(char)  # Add the operator to tokens

            if current_number:
                tokens.append(float(current_number))  # Add the last number

            return tokens

        def apply_operator(operators, values, current_operator):
            """Apply the current operator to the top two values in the stack"""
            if len(values) < 2:
                raise ValueError("Invalid expression")

            right = values.pop()  # Pop the right operand
            left = values.pop()  # Pop the left operand

            if current_operator == '+':
                values.append(left + right)  # Addition
            elif current_operator == '−':
                values.append(left - right)  # Subtraction
            elif current_operator == '×':
                values.append(left * right)  # Multiplication
            elif current_operator == '÷':
                if right == 0:
                    raise ValueError("Division by zero")  # Handle division by zero
                values.append(left / right)  # Division
            elif current_operator == '^':
                values.append(left ** right)  # Power
            elif current_operator == '√':
                if right < 0:
                    raise ValueError("Square root of negative number")  # Handle invalid input
                values.append(right ** 0.5)  # Square root
            elif current_operator == 'exp':
                values.append(2.71828 ** right)  # Exponential (approximation of e^x)
            elif current_operator == 'e':
                values.append(2.71828)  # Euler's number (approximation)

        def precedence(operator):
            """Return the precedence of the operator"""
            if operator in ('+', '−'):
                return 1  # Lower precedence for addition and subtraction
            if operator in ('×', '÷'):
                return 2  # Higher precedence for multiplication and division
            if operator in ('^', '√', 'exp', 'e'):
                return 3  # Highest precedence for power, sqrt, exp, and e
            return 0

        values = []  # Stack for numbers
        operators = []  # Stack for operators
        tokens = tokenize(expression)  # Tokenize the expression

        for token in tokens:
            if isinstance(token, (int, float)):
                values.append(token)  # Push numbers to the values stack
            elif token == '(':
                operators.append(token)  # Push '(' to the operators stack
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values, operators.pop())  # Apply operators until '('
                if operators:
                    operators.pop()  # Pop '('
                else:
                    raise ValueError("Mismatched parentheses")
            elif token in ('+', '−', '×', '÷', '^', '√', 'exp', 'e'):
                while (operators and operators[-1] != '(' and
                       precedence(operators[-1]) >= precedence(token)):
                    apply_operator(operators, values, operators.pop())  # Apply higher precedence operators
                operators.append(token)  # Push the current operator

        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            apply_operator(operators, values, operators.pop())  # Apply remaining operators

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]  # Return the final result

    def evaluate_expression(self, expression):
        """Evaluate expression with letter substitution"""
        try:
            # Replace letters with their values
            for letter, value in self.letter_values.items():
                expression = expression.replace(letter, str(value))

            # Verify only allowed characters are present
            allowed_chars = set("0123456789+−×÷().^√exp e")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters"

            result = self.calculate(expression)

            # Display integer results without decimal places
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            return result

        except Exception as e:
            return f"Error: {str(e)}"

    def on_button_click(self, text):
        """Handle button clicks"""
        if text == "=":
            try:
                result = self.evaluate_expression(self.expression)
                if isinstance(result, str) and result.startswith("Error"):
                    self.display.delete(0, tk.END)
                    self.display.insert(0, result)
                    return

                # Assign next available letter if within limit
                if self.complex_mode and len(self.letter_values) < 12:
                    letter = chr(self.next_letter)
                    self.letter_values[letter] = result
                    # Find next available letter
                    for next_letter in range(self.next_letter + 1, ord('M')):
                        if chr(next_letter) not in self.letter_values:
                            self.next_letter = next_letter
                            break

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history_entry = f"{letter} = {result} ({timestamp} : {self.expression} = {result})"
                if len(self.history) >= HISTORY_LIMIT:
                    self.history.pop(0)  # Remove the oldest entry if history is full
                self.history.append(history_entry)
                self.save_history()
                self.update_history_display()
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
                self.expression = str(result)

            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")

        elif text == "CLR":
            self.expression = ""
            self.display.delete(0, tk.END)
        elif text == "⌫":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        else:
            self.expression += text
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        if key in "0123456789":
            self.on_button_click(key)
        elif key in "+-*/":
            if key == "*":
                self.on_button_click("×")
            elif key == "/":
                self.on_button_click("÷")
            else:
                self.on_button_click(key)
        elif key == "\r":  # Enter key
            self.on_button_click("=")
        elif key == "\x08":  # Backspace key
            self.on_button_click("⌫")
        elif key == "(" or key == ")":
            self.on_button_click(key)
        elif key == ".":
            self.on_button_click(".")
        elif key == "c" or key == "C":  # Clear (CLR)
            self.on_button_click("CLR")
        elif key.lower() in "abcdefghijkl":  # Handle letter keys (A-L)
            self.on_button_click(key.upper())

    def clear_history(self):
        """Clear all history and letter assignments"""
        self.history = []
        self.letter_values = {}
        self.next_letter = 65  # Reset to 'A'
        self.save_history()
        self.update_history_display()


if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = CalculatorApp(root)  # Initialize the calculator app
    root.mainloop()  # Run the application