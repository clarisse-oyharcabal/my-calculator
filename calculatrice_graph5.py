import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from PIL import Image, ImageTk

# Configuration
HISTORY_FILE = "historique.json"
BACKGROUND_IMAGE = "background.png"  # Path to your background image
HISTORY_LIMIT = 12

# Constants for UI
BUTTON_COLORS = {
    "number": "#ffffff",
    "operator": "#e8e8e8",
    "clear": "#ffb3b3",
    "equals": "#b3ffb3",
    "letter": "#b3d9ff"
}
FONT_SIZES = {
    "normal": 14,
    "large": 18
}

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        self.expression = ""
        self.letter_values = {}
        self.next_letter = 65  # ASCII for 'A'
        self.history = []
        self.complex_mode = False  # Track mode (simple or complex)

        # Load background image
        self.bg_image = Image.open(BACKGROUND_IMAGE)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create main container with background
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Calculator container
        self.calc_container = tk.Frame(self.canvas, bg="#f5f5f5", bd=2, relief="ridge")
        self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        # History container (initially hidden)
        self.history_container = tk.Frame(self.canvas, bg="#f5f5f5", bd=2, relief="ridge")
        self.history_container.place_forget()

        # Main display
        self.display = tk.Entry(
            self.calc_container,
            font=("Arial", 24),
            justify="right",
            bd=3,
            relief="ridge",
            bg="white"
        )
        self.display.pack(padx=15, pady=(15, 10), fill="x")

        # Buttons frame
        self.buttons_frame = tk.Frame(self.calc_container, bg="#f0f0f0")
        self.buttons_frame.pack(padx=15, pady=10, fill="both", expand=True)

        # Configure grid for buttons
        for i in range(5):  # 5 rows for number and operator buttons
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 columns
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Number and operator buttons
        buttons = [
            ("(", 0, 0, BUTTON_COLORS["operator"], FONT_SIZES["normal"]),
            (")", 0, 1, BUTTON_COLORS["operator"], FONT_SIZES["normal"]),
            ("CLR", 0, 2, BUTTON_COLORS["clear"], FONT_SIZES["normal"]),
            ("⌫", 0, 3, BUTTON_COLORS["clear"], FONT_SIZES["normal"]),
            ("7", 1, 0, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("8", 1, 1, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("9", 1, 2, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("÷", 1, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("4", 2, 0, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("5", 2, 1, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("6", 2, 2, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("×", 2, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("1", 3, 0, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("2", 3, 1, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("3", 3, 2, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("−", 3, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("0", 4, 0, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            (".", 4, 1, BUTTON_COLORS["number"], FONT_SIZES["normal"]),
            ("=", 4, 2, BUTTON_COLORS["equals"], FONT_SIZES["normal"]),
            ("+", 4, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"])
        ]

        for text, row, col, color, size in buttons:
            self.create_button(text, row, col, color, size)

        # Letter buttons (A-L)
        self.letter_buttons = []
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        for i, letter in enumerate(letters):
            row = 5 + (i // 4)
            col = i % 4
            btn = self.create_button(letter, row, col, BUTTON_COLORS["letter"], FONT_SIZES["normal"])
            self.letter_buttons.append(btn)
            btn.grid_remove()  # Initially hidden

        # History display
        self.history_display = tk.Text(
            self.history_container,
            height=20,
            font=("Arial", 12),
            bg="white",
            state='disabled',
            wrap="word"
        )
        self.history_display.pack(padx=15, pady=15, fill="both", expand=True)

        # History scrollbar
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

        # Toggle button (simple/complex mode)
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
        self.toggle_button.place(relx=0.5, rely=0.9, anchor="center")

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

        # Load history
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

        # Add hover effect
        hover_color = self.get_darker_shade(color)
        button.bind("<Enter>", lambda e, btn=button, c=hover_color: btn.configure(bg=c))
        button.bind("<Leave>", lambda e, btn=button, c=color: btn.configure(bg=c))

        return button

    def get_darker_shade(self, color):
        """Convert color to darker shade"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        factor = 0.8
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def on_resize(self, event):
        """Handle window resize"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Resize background image
        resized_image = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Adjust calculator and history container positions
        if self.complex_mode:
            self.calc_container.place(relx=0.3, rely=0.5, anchor="center", width=400, height=500)
            self.history_container.place(relx=0.7, rely=0.5, anchor="center", width=400, height=500)
        else:
            self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

    def toggle_mode(self):
        """Toggle between simple and complex modes"""
        self.complex_mode = not self.complex_mode

        if self.complex_mode:
            self.toggle_button.config(text="Simple Mode")
            self.history_container.place(relx=0.7, rely=0.5, anchor="center", width=400, height=500)
            for btn in self.letter_buttons:
                btn.grid()
        else:
            self.toggle_button.config(text="Advanced Mode")
            self.history_container.place_forget()
            for btn in self.letter_buttons:
                btn.grid_remove()
            self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

    def load_history(self):
        """Load history and letter assignments from file"""
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.history = data.get("history", [])
                    self.letter_values = data.get("letter_values", {})
                elif isinstance(data, list):
                    self.history = data
                    self.letter_values = {}
                else:
                    self.history = []
                    self.letter_values = {}

                # Find the next available letter
                used_letters = set(self.letter_values.keys())
                for letter in 'ABCDEFGHIJKL':
                    if letter not in used_letters:
                        self.next_letter = ord(letter)
                        break
        except FileNotFoundError:
            self.history = []
            self.letter_values = {}
            self.next_letter = 65  # 'A'

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
        self.history_display.config(state='normal')
        self.history_display.delete(1.0, tk.END)
        for letter, value in self.letter_values.items():
            self.history_display.insert(tk.END, f"{letter} = {value}\n")
        for record in self.history:
            self.history_display.insert(tk.END, f"{record}\n")
        self.history_display.config(state='disabled')

    def calculate(self, expression):
        """
        Safe calculator implementation without eval()
        Handles: +, -, *, /, (), and numbers
        """
        def tokenize(expr):
            tokens = []
            current_number = ''

            for char in expr:
                if char.isdigit() or char == '.':
                    current_number += char
                else:
                    if current_number:
                        tokens.append(float(current_number))
                        current_number = ''
                    if char != ' ':
                        tokens.append(char)

            if current_number:
                tokens.append(float(current_number))

            return tokens

        def apply_operator(operators, values, current_operator):
            if len(values) < 2:
                raise ValueError("Invalid expression")

            right = values.pop()
            left = values.pop()

            if current_operator == '+':
                values.append(left + right)
            elif current_operator == '−':
                values.append(left - right)
            elif current_operator == '×':
                values.append(left * right)
            elif current_operator == '÷':
                if right == 0:
                    raise ValueError("Division by zero")
                values.append(left / right)

        def precedence(operator):
            if operator in ('+', '−'):
                return 1
            if operator in ('×', '÷'):
                return 2
            return 0

        values = []
        operators = []
        tokens = tokenize(expression)

        for token in tokens:
            if isinstance(token, (int, float)):
                values.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values, operators.pop())
                if operators:
                    operators.pop()  # Remove '('
                else:
                    raise ValueError("Mismatched parentheses")
            elif token in ('+', '−', '×', '÷'):
                while (operators and operators[-1] != '(' and
                       precedence(operators[-1]) >= precedence(token)):
                    apply_operator(operators, values, operators.pop())
                operators.append(token)

        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            apply_operator(operators, values, operators.pop())

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]

    def evaluate_expression(self, expression):
        """Evaluate expression with letter substitution"""
        try:
            # Replace letters with their values
            for letter, value in self.letter_values.items():
                expression = expression.replace(letter, str(value))

            # Verify only allowed characters are present
            allowed_chars = set("0123456789+−×÷(). ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters"

            result = self.calculate(expression)
            return result

        except Exception as e:
            return f"Error: Invalid expression"

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
                self.history.append(f"{timestamp} : {self.expression} = {result}")
                self.history = self.history[-HISTORY_LIMIT:]  # Keep only the last 12 items
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

    def clear_history(self):
        """Clear all history and letter assignments"""
        self.history = []
        self.letter_values = {}
        self.next_letter = 65  # Reset to 'A'
        self.save_history()
        self.update_history_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()