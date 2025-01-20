import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr  # Import the speech recognition library

# Configuration
HISTORY_FILE = "history.json"
BACKGROUND_IMAGE = "background.png"  # Ensure you have this image in the same directory
HISTORY_LIMIT = 1000

# Constants for UI (colors and font sizes)
BUTTON_COLORS = {
    "number": "#ffffff",
    "operator": "#e8e8e8",
    "clear": "#ffb3b3",
    "equals": "#b3ffb3",
    "letter": "#b3d9ff"
}
FONT_SIZES = {
    "normal": 16,
    "large": 20,
    "small": 12
}

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        # Initialize variables
        self.expression = ""
        self.letter_values = {}
        self.next_letter = 65
        self.history = []
        self.complex_mode = False
        self.voice_enabled = False

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()

        # Load background image
        try:
            self.bg_image = Image.open(BACKGROUND_IMAGE)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            self.bg_photo = None  # Handle missing background image

        # Create main container with background
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Add explanatory text in the background
        self.canvas.create_text(
            500, 50,
            text="Operation Priorities:\n"
                 "1. Multiplication (*) and Division (/) have higher priority.\n"
                 "2. Addition (+) and Subtraction (-) have lower priority.\n"
                 "Use parentheses () to set your own priorities.",
            font=("Arial", 14, "bold"),
            fill="white",
            anchor="center"
        )

        # Calculator container
        self.calc_container = tk.Frame(self.canvas, bg="#f5f5f5", bd=2, relief="ridge")
        self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=450, height=550)

        # History container
        self.history_container = tk.Frame(self.canvas, bg="#f5f5f5", bd=2, relief="ridge")
        self.history_container.place_forget()

        # Main display
        self.display = tk.Entry(
            self.calc_container,
            font=("Arial", 28),
            justify="right",
            bd=3,
            relief="ridge",
            bg="white"
        )
        self.display.pack(padx=15, pady=(20, 15), fill="x")

        # Buttons frame
        self.buttons_frame = tk.Frame(self.calc_container, bg="#f0f0f0")
        self.buttons_frame.pack(padx=15, pady=10, fill="both", expand=True)

        # Configure grid for buttons
        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Define buttons and their positions
        buttons = [
            ("(", 0, 0, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            (")", 0, 1, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("CLR", 0, 2, BUTTON_COLORS["clear"], FONT_SIZES["normal"]),
            ("⌫", 0, 3, BUTTON_COLORS["clear"], FONT_SIZES["normal"]),
            ("7", 1, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("8", 1, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("9", 1, 2, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("÷", 1, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("4", 2, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("5", 2, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("6", 2, 2, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("×", 2, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("1", 3, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("2", 3, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("3", 3, 2, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("−", 3, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("0", 4, 0, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            (".", 4, 1, BUTTON_COLORS["number"], FONT_SIZES["large"]),
            ("=", 4, 2, BUTTON_COLORS["equals"], FONT_SIZES["large"]),
            ("+", 4, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
        ]

        # Create buttons
        for text, row, col, color, size in buttons:
            self.create_button(text, row, col, color, size)

        # Advanced mode buttons
        self.advanced_buttons = [
            ("√", 5, 0, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("^", 5, 1, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("exp", 5, 2, BUTTON_COLORS["operator"], FONT_SIZES["large"]),
            ("e", 5, 3, BUTTON_COLORS["operator"], FONT_SIZES["large"])
        ]

        # Create advanced buttons and hide them initially
        self.advanced_button_widgets = []
        for text, row, col, color, size in self.advanced_buttons:
            btn = self.create_button(text, row, col, color, size)
            self.advanced_button_widgets.append(btn)
            btn.grid_remove()

        # Letter buttons
        self.letter_buttons = []
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        for i, letter in enumerate(letters):
            row = 6 + (i // 4)
            col = i % 4
            btn = self.create_button(letter, row, col, BUTTON_COLORS["letter"], FONT_SIZES["small"])
            self.letter_buttons.append(btn)
            btn.grid_remove()

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

        # Toggle button
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

        # Voice toggle button
        self.voice_toggle_btn = tk.Button(
            self.canvas,
            text="Voice Off",
            font=("Arial", 14),
            bg="#b3ffb3",
            command=self.toggle_voice,
            bd=2,
            relief="raised",
            padx=8,
            pady=6,
            cursor="hand2"
        )
        self.voice_toggle_btn.place(relx=0.5, rely=0.95, anchor="center")

        # Add a new button for voice input
        self.voice_input_btn = tk.Button(
            self.canvas,
            text="Voice Input",
            font=("Arial", 14),
            bg="#ffcccb",
            command=self.voice_input,
            bd=2,
            relief="raised",
            padx=8,
            pady=6,
            cursor="hand2"
        )
        self.voice_input_btn.place(relx=0.5, rely=0.85, anchor="center")

        # Bind keyboard events
        self.root.bind("<Key>", self.on_key_press)

        # Bind resize event
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

        # Resize background image to fit the window
        if self.bg_photo:
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
            self.toggle_button.config(text="Simple Mode")
            self.history_container.place(relx=0.7, rely=0.5, anchor="center", width=450, height=550)
            for btn in self.advanced_button_widgets:
                btn.grid()
            for btn in self.letter_buttons:
                btn.grid()
        else:
            self.toggle_button.config(text="Advanced Mode")
            self.history_container.place_forget()
            for btn in self.advanced_button_widgets:
                btn.grid_remove()
            for btn in self.letter_buttons:
                btn.grid_remove()
            self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=450, height=550)

    def toggle_voice(self):
        """Toggle voice functionality on and off"""
        self.voice_enabled = not self.voice_enabled
        if self.voice_enabled:
            self.voice_toggle_btn.config(text="Voice On")
        else:
            self.voice_toggle_btn.config(text="Voice Off")

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
            self.next_letter = 65

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
        for record in self.history:
            self.history_display.insert(tk.END, f"{record}\n")
        self.history_display.config(state='disabled')

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
            """Apply the current operator to the top two values in the stack"""
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
            elif current_operator == '^':
                values.append(left ** right)
            elif current_operator == '√':
                if right < 0:
                    raise ValueError("Square root of negative number")
                values.append(right ** 0.5)
            elif current_operator == 'exp':
                values.append(2.71828 ** right)
            elif current_operator == 'e':
                values.append(2.71828)

        def precedence(operator):
            """Return the precedence of the operator"""
            if operator in ('+', '−'):
                return 1
            if operator in ('×', '÷'):
                return 2
            if operator in ('^', '√', 'exp', 'e'):
                return 3
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
                    operators.pop()
                else:
                    raise ValueError("Mismatched parentheses")
            elif token in ('+', '−', '×', '÷', '^', '√', 'exp', 'e'):
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
        if self.voice_enabled:
            self.engine.say(text)
            self.engine.runAndWait()
        if text == "=":
            try:
                result = self.evaluate_expression(self.expression)
                if isinstance(result, str) and result.startswith("Error"):
                    self.display.delete(0, tk.END)
                    self.display.insert(0, result)
                    if self.voice_enabled:
                        self.engine.say(result)
                        self.engine.runAndWait()
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
                    self.history.pop(0)
                self.history.append(history_entry)
                self.save_history()
                self.update_history_display()
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
                self.expression = str(result)
                if self.voice_enabled:
                    self.engine.say(f"Result is {result}")
                    self.engine.runAndWait()

            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
                if self.voice_enabled:
                    self.engine.say("Error")
                    self.engine.runAndWait()

        elif text == "CLR":
            self.expression = ""
            self.display.delete(0, tk.END)
            if self.voice_enabled:
                self.engine.say("Cleared")
                self.engine.runAndWait()
        elif text == "⌫":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
            if self.voice_enabled:
                self.engine.say("Deleted")
                self.engine.runAndWait()
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
        self.next_letter = 65
        self.save_history()
        self.update_history_display()

    def voice_input(self):
        """Capture voice input and process it"""
        try:
            # List available microphones
            print("Available microphones:")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"{index}: {name}")

            # Use the default microphone (index 0) or specify another index
            with sr.Microphone(device_index=0) as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)  # Calibrate for background noise
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Add timeout and phrase limit
                print("Processing...")
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                self.process_voice_input(text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results from Google Speech Recognition")
        except sr.WaitTimeoutError:
            messagebox.showerror("Error", "No speech detected within the timeout period")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_voice_input(self, text):
        """Process the recognized text as calculator input"""
        if self.voice_enabled:
            self.engine.say(f"You said: {text}")
            self.engine.runAndWait()

        # Replace spoken words with corresponding symbols
        text = text.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
        text = text.replace("equals", "=").replace("clear", "CLR").replace("delete", "⌫")

        # Display the recognized text in the calculator display
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.expression = text

        # Simulate button clicks based on the recognized text
        for char in text:
            if char in "0123456789+-*/=()":
                self.on_button_click(char)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()