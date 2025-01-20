historique = []

def afficher_menu():
    print("\n📖 Menu principal📖 :")
    print("1. 🔢 Effectuer un calcul")
    print("2. 🌱 Calculer une racine carrée d'un nombre")
    print("3. 💭 Afficher l'historique")
    print("4. ❌ Effacer l'historique")
    print("5. ⛷️ Quitter\n")


def input_validator():
    # Saisie du premier nombre
    while True:
        try:
            num1 = float(input("Entrez le premier nombre : "))
            break
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Saisie du premier opérateur
    while True:
        operator1 = input("Entrez le premier opérateur (+, -, *, /, ^) : ").strip().lower()
        if operator1 not in ["+", "-", "*", "/", "^"]:
            print("Opérateur non valide.")
            continue
        else:
            break

    # Saisie du deuxième nombre
    while True:
        try:
            num2 = float(input("Entrez le deuxième nombre : "))
            if operator1 == "/" and num2 == 0:
                print("Division par zéro impossible.")
                continue
            break
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    
    return num1, operator1, num2

def effectuer_calcul(num1, operator, num2):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    elif operator == "^":
        return num1 ** num2

def effectuer_calcul_prioritaire(num1, operator1, num2, operator2, num3):
    # Priorités des opérateurs
    priorites = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}

    # Si operator1 a une priorité plus élevée, on le calcule en premier
    if priorites[operator1] > priorites[operator2]:
        result1 = effectuer_calcul(num1, operator1, num2)
        result2 = effectuer_calcul(result1, operator2, num3)
        return result2
    else:
        result1 = effectuer_calcul(num2, operator2, num3)
        result2 = effectuer_calcul(num1, operator1, result1)
        return result2

def calcul_racine_carre():
    while True:
        try:
            num = float(input("Entrez un nombre pour calculer sa racine carrée : "))
            if num < 0:
                print("Impossible de calculer la racine carrée d'un nombre négatif.")
                continue
            racine = num ** 0.5
            print(f"La racine carrée de {num} est : {racine}")
            historique.append(f"√{num} = {racine}")
            break
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def print_resultat():
    num1, operator1, num2 = input_validator()
    operator2 = input("Entrez le deuxième opérateur (+, -, *, /, ^) : ").strip().lower()

    while operator2 not in ["+", "-", "*", "/", "^"]:
        print("Opérateur non valide.")
        operator2 = input("Entrez le deuxième opérateur (+, -, *, /, ^) : ").strip().lower()

    while True:
        try:
            num3 = float(input("Entrez le troisième nombre : "))
            if (operator2 == "/" or operator1 == "/") and num3 == 0:
                print("Division par zéro impossible.")
                continue
            break
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    
    resultat = effectuer_calcul_prioritaire(num1, operator1, num2, operator2, num3)
    
    # Construction de l'équation
    equation = f"{num1} {operator1} {num2} {operator2} {num3}"
    print(f"Le résultat de {equation} est : {resultat}")
    historique.append(f"{equation} = {resultat}")

def recommencer_calcul():
    while True:
        print_resultat()
        while True:
            recommencer = input("Voulez-vous effectuer un autre calcul ? (o pour refaire calcul, n pour retourner au menu) : ").strip().lower()
            if recommencer == 'o':
                break
            elif recommencer == 'n':
                return
            else:
                print("Entrée invalide. Veuillez saisir 'o' pour refaire un calcul ou 'n' pour retourner au menu.")

def recommencer_racine():
    while True:
        calcul_racine_carre()
        while True:
            recommencer = input("Voulez-vous calculer une autre racine carrée ? (o pour refaire, n pour retourner au menu) : ").strip().lower()
            if recommencer == 'o':
                break
            elif recommencer == 'n':
                return
            else:
                print("Entrée invalide. Veuillez saisir 'o' pour refaire ou 'n' pour retourner au menu.")

def print_historique():
    if not historique:
        print("Nous ne pouvons pas afficher l'historique car il est vide.")
    else:
        print("\n=== Historique des calculs : ===")
        for calcul in historique:
            print(calcul)

def effacer_historique():
    if not historique:
        print("Aucun historique à effacer.")
    else:
        historique.clear()
        print("Historique effacé.")

def main():
    print("🧮 Bienvenue sur My Calculator ! :")
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ").strip()
        if choix == '1':
            recommencer_calcul()
        elif choix == '2':
            recommencer_racine()
        elif choix == '3':
            print_historique()
        elif choix == '4':
            effacer_historique()
        elif choix == '5':
            print("Merci d'avoir utilisé la calculatrice. À bientôt ! 👋")
            break
        else:
            print("Option non valide. Veuillez entrer un numéro entre 1 et 5.")

if __name__ == "__main__":
    main()
