import tkinter as tk
from tkinter import messagebox
import json
import re

# Fichier pour sauvegarder l'historique
HISTORY_FILE = "historique.json"

# Charger l'historique depuis un fichier JSON
def charger_historique():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Sauvegarder l'historique dans un fichier JSON
def sauvegarder_historique(historique):
    with open(HISTORY_FILE, "w") as f:
        json.dump(historique, f)

# Calculer une expression mathématique sans eval()
def calculer_expression(expression):
    try:
        # Gérer les priorités (parenthèses, *, /, +, -)
        tokens = re.findall(r"\d+|[+\-*/()]", expression)
        result = evaluer(tokens)
        return result
    except Exception:
        return "Erreur"

# Évaluation manuelle d'une liste de tokens (implémentation simplifiée)
def evaluer(tokens):
    def appliquer_operation(op, b, a):
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return a / b if b != 0 else "Erreur"

    priorites = {"+": 1, "-": 1, "*": 2, "/": 2}
    valeurs = []
    operateurs = []

    def resoudre():
        b = valeurs.pop()
        a = valeurs.pop()
        op = operateurs.pop()
        valeurs.append(appliquer_operation(op, b, a))

    for token in tokens:
        if token.isdigit():
            valeurs.append(float(token))
        elif token in priorites:
            while (operateurs and priorites.get(operateurs[-1], 0) >= priorites[token]):
                resoudre()
            operateurs.append(token)
        elif token == "(":
            operateurs.append(token)
        elif token == ")":
            while operateurs and operateurs[-1] != "(":
                resoudre()
            operateurs.pop()

    while operateurs:
        resoudre()

    return valeurs[0]

# Initialiser l'application principale
class CalculatriceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculatrice Avancée")

        self.expression = ""
        self.historique = charger_historique()

        # Champs d'affichage
        self.affichage = tk.Entry(root, font=("Arial", 24), justify="right")
        self.affichage.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Boutons
        boutons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0), ("Historique", 5, 1), ("Priorités", 5, 2), ("Quitter", 5, 3),
        ]

        for (text, row, col) in boutons:
            bouton = tk.Button(root, text=text, font=("Arial", 18), command=lambda t=text: self.on_click(t))
            bouton.grid(row=row, column=col, sticky="nsew")

        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def on_click(self, text):
        if text == "=":
            resultat = calculer_expression(self.expression)
            self.historique.append(self.expression + " = " + str(resultat))
            self.historique = self.historique[-10:]  # Garder les 10 derniers
            sauvegarder_historique(self.historique)
            self.affichage.delete(0, tk.END)
            self.affichage.insert(0, str(resultat))
            self.expression = ""
        elif text == "C":
            self.expression = ""
            self.affichage.delete(0, tk.END)
        elif text == "Historique":
            messagebox.showinfo("Historique", "\n".join(self.historique))
        elif text == "Priorités":
            messagebox.showinfo("Priorités", "Les priorités sont: ( ) > * / > + -")
        elif text == "Quitter":
            self.root.quit()
        else:
            self.expression += text
            self.affichage.delete(0, tk.END)
            self.affichage.insert(0, self.expression)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatriceApp(root)
    root.mainloop()
