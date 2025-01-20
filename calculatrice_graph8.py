import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from PIL import Image, ImageTk

# Configuration
HISTORY_FILE = "historique.json"
BACKGROUND_IMAGE = "background.png"
HISTORY_LIMIT = 12

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

        # Variables
        self.expression = ""
        self.letter_values = {chr(65 + i): None for i in range(HISTORY_LIMIT)}  # A-L cyclic storage
        self.history = []
        self.history_index = 0  # For cyclic history management
        self.complex_mode = False
        self.error_flag = False  # Tracks if the last calculation resulted in an error

        # Background setup
        self.bg_image = Image.open(BACKGROUND_IMAGE)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(
            500, 50,
            text="Priorités des opérations :\n1. Multiplication (*) et Division (/) sont prioritaires.\n2. Addition (+) et Soustraction (-) sont secondaires.\nUtilisez des parenthèses () pour imposer vos priorités.",
            font=("Arial", 14, "bold"),
            fill="white",
            anchor="center"
        )

        # Main containers
        self.calc_container = tk.Frame(self.canvas, bg="#f5f5f5", bd=2, relief="ridge")
        self.calc_container.place(relx=0.5, rely=0.5, anchor="center", width=450, height=550)

        self.display = tk.Entry(
            self.calc_container,
            font=("Arial", 28),
            justify="right",
            bd=3,
            relief="ridge",
            bg="white"
        )
        self.display.pack(padx=15, pady=(20, 15), fill="x")

        self.buttons_frame = tk.Frame(self.calc_container, bg="#f0f0f0")
        self.buttons_frame.pack(padx=15, pady=10, fill="both", expand=True)

        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

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

        for text, row, col, color, size in buttons:
            self.create_button(text, row, col, color, size)

        # Load history
        self.load_history()

    def create_button(self, text, row, col, color, size):
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

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                self.history = data.get("history", [])
                self.letter_values = data.get("letter_values", self.letter_values)
        except FileNotFoundError:
            self.history = []

    def save_history(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump({"history": self.history, "letter_values": self.letter_values}, f)

    def calculate(self, expression):
        try:
            result = eval(expression.replace("×", "*").replace("÷", "/").replace("−", "-"))
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.error_flag = False  # Clear error flag on success
            return result
        except Exception as e:
            self.error_flag = True
            return "Error"

    def update_history(self, value):
        letter = chr(65 + self.history_index)
        self.letter_values[letter] = value

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{letter} = {value} ({timestamp})"

        if len(self.history) >= HISTORY_LIMIT:
            self.history[self.history_index] = entry
        else:
            self.history.append(entry)

        self.history_index = (self.history_index + 1) % HISTORY_LIMIT
        self.save_history()

    def on_button_click(self, text):
        if text == "=":
            result = self.calculate(self.expression)
            if result != "Error":
                self.update_history(result)
                self.expression = str(result)
            else:
                messagebox.showerror("Calculation Error", "Invalid input or calculation error.")
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
        elif text == "CLR":
            self.expression = ""
            self.display.delete(0, tk.END)
        elif text == "⌫":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        else:
            if self.error_flag:  # Clear previous error when starting a new expression
                self.expression = ""
                self.error_flag = False
            self.expression += text
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
