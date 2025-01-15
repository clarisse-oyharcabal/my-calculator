import tkinter as tk
from tkinter import messagebox
import json
import re
from datetime import datetime
from PIL import Image, ImageTk

# Configuration
HISTORY_FILE = "historique.json"
BACKGROUND_IMAGE = "background.png"
HISTORY_LIMIT = 10

# [Previous helper functions remain the same]
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def evaluate_expression(expression):
    try:
        tokens = re.findall(r"\d+\.?\d*|[+\-*/()]", expression)
        fixed_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == "-" and (i == 0 or tokens[i - 1] in "+-*/("):
                fixed_tokens.append(tokens[i] + tokens[i + 1])
                i += 2
            else:
                fixed_tokens.append(tokens[i])
                i += 1
        result = evaluate_tokens(fixed_tokens)
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {e}"

def evaluate_tokens(tokens):
    def apply_operation(op, b, a):
        if op == "+": return a + b
        elif op == "-": return a - b
        elif op == "*": return a * b
        elif op == "/": return a / b if b != 0 else "Error: Division by zero"

    priorities = {"+": 1, "-": 1, "*": 2, "/": 2}
    values = []
    operators = []

    def resolve():
        b = values.pop()
        a = values.pop()
        op = operators.pop()
        values.append(apply_operation(op, b, a))

    for token in tokens:
        if token.replace(".", "").isdigit():
            values.append(float(token))
        elif token in priorities:
            while operators and priorities.get(operators[-1], 0) >= priorities[token]:
                resolve()
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                resolve()
            operators.pop()

    while operators:
        resolve()

    return values[0]

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("800x600")  # Increased initial window size
        self.root.minsize(600, 450)    # Adjusted minimum size

        self.expression = ""
        self.history = load_history()

        # Create main container
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill="both", expand=True)

        # Load and set up background
        self.bg_image = Image.open(BACKGROUND_IMAGE)
        self.bg_photo = None
        self.canvas = tk.Canvas(self.main_container)
        self.canvas.pack(fill="both", expand=True)

        # Create centered container for calculator elements with light gray background
        self.calc_container = tk.Frame(self.canvas, bg='#f5f5f5')
        
        # Display with adjusted size
        self.display = tk.Entry(
            self.calc_container,
            font=("Arial", 20),  # Slightly smaller font
            justify="right",
            bd=3,
            relief="ridge",
            bg="white"
        )
        self.display.pack(padx=15, pady=15, fill="x")

        # Buttons frame with improved styling
        self.buttons_frame = tk.Frame(self.calc_container, bg="#f0f0f0")
        self.buttons_frame.pack(padx=15, pady=15, fill="both", expand=True)

        # Button configuration with updated colors
        buttons = [
            ("(", 0, 0, "#e8e8e8"), (")", 0, 1, "#e8e8e8"), 
            ("C", 0, 2, "#ffb3b3"), ("History", 0, 3, "#b3d9ff"),
            ("7", 1, 0, "#ffffff"), ("8", 1, 1, "#ffffff"), 
            ("9", 1, 2, "#ffffff"), ("/", 1, 3, "#e8e8e8"),
            ("4", 2, 0, "#ffffff"), ("5", 2, 1, "#ffffff"), 
            ("6", 2, 2, "#ffffff"), ("*", 2, 3, "#e8e8e8"),
            ("1", 3, 0, "#ffffff"), ("2", 3, 1, "#ffffff"), 
            ("3", 3, 2, "#ffffff"), ("-", 3, 3, "#e8e8e8"),
            ("0", 4, 0, "#ffffff"), (".", 4, 1, "#ffffff"), 
            ("=", 4, 2, "#b3ffb3"), ("+", 4, 3, "#e8e8e8"),
            ("Quit", 5, 0, "#ffb3b3", 4)
        ]

        # Configure grid with more spacing
        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Create buttons with smaller size
        for btn in buttons:
            text, row, col, bg_color = btn[:4]
            colspan = btn[4] if len(btn) > 4 else 1
            
            button = tk.Button(
                self.buttons_frame,
                text=text,
                font=("Arial", 14),  # Smaller font size
                command=lambda t=text: self.on_button_click(t),
                bg=bg_color,
                fg="black",
                bd=2,
                relief="raised",
                padx=8,
                pady=6,
                cursor="hand2"
            )
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)
            
            # Add hover effect with darker shade
            hover_color = self.get_darker_shade(bg_color)
            button.bind("<Enter>", lambda e, btn=button, color=hover_color: btn.configure(bg=color))
            button.bind("<Leave>", lambda e, btn=button, color=bg_color: btn.configure(bg=color))

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)
        
        # Initial layout
        self.on_resize(None)

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
        # Get window dimensions
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Resize background image
        resized_image = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Calculate calculator container size (60% of window size instead of 80%)
        calc_width = int(width * 0.6)
        calc_height = int(height * 0.7)

        # Center the calculator container
        x = (width - calc_width) // 2
        y = (height - calc_height) // 2

        # Update calculator container size and position
        self.calc_container.place(
            x=x,
            y=y,
            width=calc_width,
            height=calc_height
        )

    # [Previous methods remain the same]
    def update_display(self, text):
        self.display.delete(0, tk.END)
        self.display.insert(0, text)

    def clear_display(self):
        self.expression = ""
        self.update_display("")

    def on_button_click(self, text):
        if text == "=":
            result = evaluate_expression(self.expression)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append(f"{timestamp} : {self.expression} = {result}")
            self.history = self.history[-HISTORY_LIMIT:]
            save_history(self.history)
            self.update_display(str(result))
            self.expression = str(result)
        elif text == "C":
            self.clear_display()
        elif text == "History":
            if self.history:
                messagebox.showinfo("History", "\n".join(self.history))
            else:
                messagebox.showinfo("History", "No calculations in history")
        elif text == "Quit":
            save_history(self.history)
            self.root.quit()
        else:
            self.expression += text
            self.update_display(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()