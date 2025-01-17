historique = []

def afficher_menu():
    print ("\n📖 Menu principal📖:")
    print ("1. 🔢 Effectuer un calcul")
    print ("2. 💭 Afficher l'historique")    
    print ("3. ❌ Effacer l'historique")
    print ("4. ⛷️  Quitter\n")

def afficher_erreur(message): #Affiche un message d'erreur 
    print(f'Erreur : {message}')

def input_validator():
    while True:
        try:
            num1 = float(input("Entrez le premier nombre : "))
            break
        except ValueError:
            afficher_erreur("Veuillez entrer un nombre valide.")

    while True:
        operator1 = input("Entrez le premier opérateur (+, -, *, /, sqrt, e) : ").strip().lower()
        if operator1 not in ["+", "-", "*", "/", "sqrt", "e"]:
            afficher_erreur("Opérateur non valide.")
        elif operator1 =="sqrt" and num1 < 0 : 
            afficher_erreur("Impossible de calculer la racine carrée d'un nombre négatif.")
        else:
            break

    while True:
        try:
            num2 = float(input("Entrez le deuxième nombre : "))
            if operator1 == "/" and num2 == 0 :
                afficher_erreur("Division par zéro impossible.")      
            else:
                break
        except ValueError:
            afficher_erreur("Veuillez entrer un nombre valide.")


    while True:
        operator2 = input("Entrez le deuxième opérateur (+, -, *, /, sqrt, e) : ").strip().lower()
        if operator2 not in ["+", "-", "*", "/", "sqrt", "e"]:
            afficher_erreur("Opérateur non valide.")
        else:
            break

    while True:
        try:
            num3 = float(input("Entrez le troisième nombre : "))
            if operator2 == "/" and num3 == 0:
                afficher_erreur("Division par zéro impossible.")
            else:
                break
        except ValueError:
            afficher_erreur("Veuillez entrer un nombre valide.")

    return num1, operator1, num2, operator2, num3


def effectuer_calcul(num1, operator, num2):
    # Effectuer le calcul
    if operator == '+':
        resultat = num1 + num2
    elif operator == '-':
        resultat = num1 - num2
    elif operator == '*':
        resultat = num1 * num2
    elif operator == '/':
        resultat = num1 / num2
    elif operator == "sqrt":
        resultat = num1 ** 0.5  #Calcul de la racine carrée en utilisant l'exponentiel
    elif operator == "e" : 
        resultat = num1 ** num2 
    return resultat

def effectuer_calcul_prioritaire(num1, operator1, num2, operator2, num3):
    # dico des opérateurs par priorité
    priorites = {"*": 2, "/": 2, "+": 1, "-": 1, "e": 2, "sqrt": 2}

    # Calcul intermédiaire pour respecter la priorité
    if priorites[operator1] >= priorites[operator2]:        
        # Calculer num1 operator1 num2 en premier
        intermediaire = effectuer_calcul(num1, operator1, num2)
        resultat = effectuer_calcul(intermediaire, operator2, num3)
    else:
        # Calculer num2 operator2 num3 en premier
        intermediaire = effectuer_calcul(num2, operator2, num3)
        resultat = effectuer_calcul(num1, operator1, intermediaire)

    return resultat

def print_resultat():
    num1, operator1, num2, operator2, num3 = input_validator()  

    if num1 is None:
        print("Erreur: il n'est pas possible de calculer la racine carrée d'un nombre négatif")
        return
    
    resultat = effectuer_calcul_prioritaire(num1, operator1, num2, operator2, num3)
    print(f"Le résultat de {num1} {operator1} {num2} {operator2} {num3} est : {resultat}")
    historique.append(f"{num1} {operator1} {num2} {operator2} {num3} = {resultat}")

def recommencer_calcul():
    while True:
        print_resultat()

    #Demande à l'utilisateur s'il veut recommencer un calcul.
        while True:
            recommencer = input("Voulez-vous effectuer un autre calcul ? (o pour refaire calcul, n pour retourner au menu) : ").strip().lower()
            if recommencer == 'o':
                break  # Recommence un autre calcul
            elif recommencer == 'n':
                return  # Retourne au menu principal
            else:
                print("Entrée invalide. Veuillez saisir 'o' pour refaire un calcul ou 'n' pour retourner au menu.")

def print_historique():
    if not historique: 
        print(" Nous ne pouvons pas afficher l'historique car il est vide.")
    else:
        print("\n===Historique des calculs : ===")
        for calculs in historique: 
            print(calculs)

def effacer_historique():  #efface l'historique des calculs
    if not historique:
        print("Aucun historique à effacer")
    else:
        historique.clear() 
        # pour verifier: print(historique)
        print("Historique effacé")

#Boucle principal mainloop
def main():
    print ("🧮 Bienvenue sur My Calculator ! :")

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