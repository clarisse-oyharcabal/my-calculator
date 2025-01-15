import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from PIL import Image, ImageTk

# Configuration
HISTORY_FILE = "historique.json"
BACKGROUND_IMAGE = "background.png"
HISTORY_LIMIT = 12  # Change history limit to 12

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("800x600")
        self.root.minsize(600, 450)

        self.expression = ""
        self.letter_values = {}  # Dictionary to store letter:value mappings
        self.next_letter = 65  # ASCII for 'A'
        self.history = []
        self.history_visible = False  # Track visibility of history
        self.load_history()

        # Create main container
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill="both", expand=True)

        # Load and set up background
        self.bg_image = Image.open(BACKGROUND_IMAGE)
        self.bg_photo = None
        self.canvas = tk.Canvas(self.main_container)
        self.canvas.pack(fill="both", expand=True)

        # Create calculator container
        self.calc_container = tk.Frame(self.canvas, bg='#f5f5f5')
        
        # History display (initially hidden)
        self.history_display_frame = tk.Frame(self.calc_container)
        self.history_display_frame.pack(padx=15, pady=(15,5), fill="x")

        self.history_display = tk.Text(
            self.history_display_frame,
            height=6,  # Increased height to accommodate 12 records
            font=("Arial", 12),
            bg="white",
            state='disabled',
            wrap="word"
        )

        # Add vertical scrollbar to history display
        self.history_scrollbar = tk.Scrollbar(self.history_display_frame, command=self.history_display.yview)
        self.history_display.config(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.pack(side="right", fill="y")

        # Create main display
        self.display = tk.Entry(
            self.calc_container,
            font=("Arial", 20),
            justify="right",
            bd=3,
            relief="ridge",
            bg="white"
        )
        self.display.pack(padx=15, pady=(5,15), fill="x")

        # Buttons frame
        self.buttons_frame = tk.Frame(self.calc_container, bg="#f0f0f0")
        self.buttons_frame.pack(padx=15, pady=15, fill="both", expand=True)

        # Configure grid for number and operator buttons
        for i in range(9):  # Increased grid rows for all buttons
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 columns for number and operator buttons
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Number and operator buttons
        buttons = [
            ("(", 0, 0, "#e8e8e8"), (")", 0, 1, "#e8e8e8"), 
            ("CLR", 0, 2, "#ffb3b3"), ("⌫", 0, 3, "#ffb3b3"),
            ("7", 1, 0, "#ffffff"), ("8", 1, 1, "#ffffff"), 
            ("9", 1, 2, "#ffffff"), ("/", 1, 3, "#e8e8e8"),
            ("4", 2, 0, "#ffffff"), ("5", 2, 1, "#ffffff"), 
            ("6", 2, 2, "#ffffff"), ("*", 2, 3, "#e8e8e8"),
            ("1", 3, 0, "#ffffff"), ("2", 3, 1, "#ffffff"), 
            ("3", 3, 2, "#ffffff"), ("-", 3, 3, "#e8e8e8"),
            ("0", 4, 0, "#ffffff"), (".", 4, 1, "#ffffff"), 
            ("=", 4, 2, "#b3ffb3"), ("+", 4, 3, "#e8e8e8")
        ]

        # Create number and operator buttons
        for text, row, col, color in buttons:
            self.create_button(text, row, col, color)

        # Create letter buttons (A-L) below the number buttons
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        for i, letter in enumerate(letters):
            row = 5 + (i // 4)  # Distribute letters across two rows
            col = i % 4  # 4 columns for letters
            self.create_button(letter, row, col, "#b3d9ff")

        # History button (always visible at bottom of window)
        self.history_button = tk.Button(
            self.main_container,
            text="History",
            font=("Arial", 14),
            bg="#ffb3b3",
            fg="black",
            command=self.toggle_history,
            bd=2,
            relief="raised",
            padx=8,
            pady=6,
            cursor="hand2"
        )
        self.history_button.pack(side="bottom", pady=10)

        # History text box
        self.history_display.pack(padx=15, pady=(15,5), fill="x")

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)
        self.on_resize(None)
        self.update_history_display()

    def create_button(self, text, row, col, color):
        """Helper method to create buttons with consistent styling"""
        button = tk.Button(
            self.buttons_frame,
            text=text,
            font=("Arial", 14),
            command=lambda t=text: self.on_button_click(t),
            bg=color,
            fg="black",
            bd=2,
            relief="raised",
            padx=8,
            pady=6,
            cursor="hand2"
        )
        button.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
        
        # Add hover effect
        hover_color = self.get_darker_shade(color)
        button.bind("<Enter>", lambda e, btn=button, c=hover_color: btn.configure(bg=c))
        button.bind("<Leave>", lambda e, btn=button, c=color: btn.configure(bg=c))

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

        resized_image = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        calc_width = int(width * 0.6)
        calc_height = int(height * 0.8)
        x = (width - calc_width) // 2
        y = (height - calc_height) // 2

        self.calc_container.place(x=x, y=y, width=calc_width, height=calc_height)

    def load_history(self):
        """Load history and letter assignments from file"""
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):  # Check if data is a dictionary
                    self.history = data.get("history", [])
                    self.letter_values = data.get("letter_values", {})
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

    def evaluate_expression(self, expression):
        """Evaluate expression with letter substitution"""
        try:
            # Replace letters with their values
            for letter, value in self.letter_values.items():
                expression = expression.replace(letter, str(value))

            # Use eval safely with limited namespace
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters"
            
            result = eval(expression)
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
                if len(self.letter_values) < 12:
                    letter = chr(self.next_letter)
                    self.letter_values[letter] = result
                    # Find next available letter
                    for next_letter in range(self.next_letter + 1, ord('M')):  # Next letters after 'L'
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
        elif text == "⌫":  # Backspace
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        else:
            self.expression += text
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

    def toggle_history(self):
        """Toggle the visibility of the history"""
        if self.history_visible:
            self.history_display.pack_forget()
        else:
            self.history_display.pack(padx=15, pady=(15,5), fill="x")
        self.history_visible = not self.history_visible


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
