historique = []

def afficher_menu():
    print("\n📖 Menu principal📖:")
    print("1. 🔢 Effectuer un calcul")
    print("2. 💭 Afficher l'historique")
    print("3. ❌ Effacer l'historique")
    print("4. ⛷️  Quitter\n")

def afficher_erreur(message):
    print(f"Erreur : {message}")

def afficher_resultat_intermediaire(operation, resultat):
    print(f"Résultat intermédiaire : {operation} = {resultat}")

def input_validator():
    # Saisie du premier nombre
    while True:
        try:
            num1 = float(input("Entrez le premier nombre : "))
            break
        except ValueError:
            afficher_erreur("Veuillez entrer un nombre valide.")

    # Saisie du premier opérateur
    while True:
        operator1 = input("Entrez le premier opérateur (+, -, *, /, r, ^) : ").strip().lower()
        if operator1 not in ["+", "-", "*", "/", "r", "^"]:
            afficher_erreur("Opérateur non valide.")
        elif operator1 == "r" and num1 < 0:
            afficher_erreur("Impossible de calculer la racine carrée d'un nombre négatif.")
        else:
            break

    # Cas où l'opérateur 1 est "r"
    if operator1 == "r":
        num_additional = num1 ** 0.5
        afficher_resultat_intermediaire(f"√{num1}", num_additional)
        while True:
            operator_additional = input("Entrez un opérateur supplémentaire après 'r' (+, -, *, /, ^) : ").strip().lower()
            if operator_additional in ["+", "-", "*", "/", "^"]:
                break
            else:
                afficher_erreur("Opérateur non valide.")
    else:
        operator_additional = None

    # Saisie du deuxième nombre
    while True:
        try:
            num2 = float(input("Entrez le deuxième nombre : "))
            if (operator1 == "/" or (operator_additional == "/" if operator_additional else False)) and num2 == 0:
                afficher_erreur("Division par zéro impossible.")
            else:
                break
        except ValueError:
            afficher_erreur("Veuillez entrer un nombre valide.")

    # Affichage des résultats intermédiaires pour "^"
    if operator1 == "^":
        result_exp = num1 ** num2
        afficher_resultat_intermediaire(f"{num1} ^ {num2}", result_exp)

    # Saisie du deuxième opérateur
    while True:
        operator2 = input("Entrez le deuxième opérateur (+, -, *, /, r, ^) : ").strip().lower()
        if operator2 not in ["+", "-", "*", "/", "r", "^"]:
            afficher_erreur("Opérateur non valide.")
        elif operator2 == "r" and operator1 == "r":
            afficher_erreur("Deux opérateurs 'r' consécutifs ne sont pas autorisés.")
        elif operator2 == "^" and operator1 == "^":
            afficher_erreur("Deux opérateurs '^' consécutifs ne sont pas autorisés.")
        else:
            break

    
    # Affichage des résultats intermédiaires pour "^"
    if operator2 == "^":
        result_exp = num2 ** num3
        afficher_resultat_intermediaire(f"{num2} ^ {num3}", result_exp)

    # Cas où l'opérateur 2 est "r"
    if operator2 == "r":
        if operator1 == "^":  # Cas où operator1 est "^"
            result_exp = num1 ** num2
            num_additional = result_exp ** 0.5
            afficher_resultat_intermediaire(f"√{result_exp}", num_additional)
        else:
            num_additional = num2 ** 0.5
            afficher_resultat_intermediaire(f"√{num2}", num_additional)
        while True:
            operator_additional = input("Entrez un opérateur supplémentaire après 'r' (+, -, *, /, ^) : ").strip().lower()
            if operator_additional in ["+", "-", "*", "/", "^"]:
                break
            else:
                afficher_erreur("Opérateur non valide.")
    else:
        operator_additional = None

    # Saisie du troisième nombre
    while True:
        try:
            num3 = float(input("Entrez le troisième nombre : "))
            if operator2 == "/" and num3 == 0:
                afficher_erreur("Division par zéro impossible.")
            else:
                break
        except ValueError:
            afficher_erreur("Veuillez entrer un nombre valide.")

    return num1, operator1, operator_additional, num2, operator2, num3

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
    elif operator == "r":
        return num1 ** 0.5

def effectuer_calcul_prioritaire(num1, operator1, operator_additional, num2, operator2, num3):
    # Priorités des opérateurs
    priorites = {"r": 3, "^": 3, "*": 2, "/": 2, "+": 1, "-": 1}
    
    # Cas où operator1 est "r"
    if operator1 == "r":
        num_additional = num1 ** 0.5
        afficher_resultat_intermediaire(f"√{num1}", num_additional)
        
        # Si operator_additional est présent, appliquer les priorités correctement
        if operator_additional:
            # Priorité de operator_additional par rapport à operator2
            if priorites[operator_additional] >= priorites[operator2]:
                intermediaire = effectuer_calcul(num_additional, operator_additional, num2)
                afficher_resultat_intermediaire(f"{num_additional} {operator_additional} {num2}", intermediaire)
                resultat = effectuer_calcul(intermediaire, operator2, num3)
            else:
                intermediaire = effectuer_calcul(num2, operator2, num3)
                afficher_resultat_intermediaire(f"{num2} {operator2} {num3}", intermediaire)
                resultat = effectuer_calcul(num_additional, operator_additional, intermediaire)
        else:
            resultat = effectuer_calcul(num_additional, operator2, num3)
        return resultat

    # Cas où operator1 est "^"
    if operator1 == "^":
        result_exp = num1 ** num2
        afficher_resultat_intermediaire(f"{num1} ^ {num2}", result_exp)
        
        # Si operator2 est "r", appliquer la racine carrée sur result_exp
        if operator2 == "r":
            result_sqrt = result_exp ** 0.5
            afficher_resultat_intermediaire(f"√{result_exp}", result_sqrt)
            resultat = result_sqrt + num3
        else:
            resultat = effectuer_calcul(result_exp, operator2, num3)
        return resultat

    # Cas général (appliquer d'abord operator1 puis operator2 si nécessaire)
    if priorites[operator1] > priorites[operator2] or (priorites[operator1] == priorites[operator2] and operator1 in ["r", "^"]):
        intermediaire = effectuer_calcul(num1, operator1, num2)
        afficher_resultat_intermediaire(f"{num1} {operator1} {num2}", intermediaire)
        resultat = effectuer_calcul(intermediaire, operator2, num3)
    else:
        intermediaire = effectuer_calcul(num2, operator2, num3)
        afficher_resultat_intermediaire(f"{num2} {operator2} {num3}", intermediaire)
        resultat = effectuer_calcul(num1, operator1, intermediaire)

    return resultat

def print_resultat():
    num1, operator1, operator_additional, num2, operator2, num3 = input_validator()
    resultat = effectuer_calcul_prioritaire(num1, operator1, operator_additional, num2, operator2, num3)
    
    # Construction de l'équation en fonction de operator_additional
    if operator_additional:
        equation = f"{num1} {operator1} {operator_additional} {num2} {operator2} {num3}"
    else:
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
        choix = input("Choisissez une option (1-4) : ").strip()
        if choix == '1':
            recommencer_calcul()
        elif choix == '2':
            print_historique()
        elif choix == '3':
            effacer_historique()
        elif choix == '4':
            print("Merci d'avoir utilisé la calculatrice. À bientôt ! 👋")
            break
        else:
            print("Option non valide. Veuillez entrer un numéro entre 1 et 4.")

if __name__ == "__main__":
    main()