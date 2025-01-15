historique = []

print ("🧮 Bienvenue sur My Calculator ! :")

def afficher_menu():
    print ("\n📖 Menu principal📖:")
    print ("1. 🔢 Effectuer un calcul")
    print ("2. 💭 Afficher l'historique")    
    print ("3. ❌ Effacer l'historique")
    print ("4. ⛷️  Quitter\n")


def input_validator():
    while True:
        try: 
            num1= float(input("Entrez un premier nombre (entier ou décimal) de votre choix : "))
            break
        except ValueError:
            print("Erreur: Veuillez entrer un nombre (entier ou décimal) valide")
        
            
    while True:    
        operator = input("Entrez un operateur (+,-,*,/) : ").strip()
        if operator not in ["+", "-", "*", "/"]:
            print("Error: opérateur non valide.")
        else:
            break

        
    while True:
        try:
            num2 = float(input("Entrez un deuxième nombre (entier ou decimal) de votre choix : "))
            if operator == '/' and num2 == 0:
                print("Erreur: Division par zéro impossible.")
                continue
            break
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide.")
    
    return num1, operator, num2
    

def effectuer_calcul():
    num1, operator, num2 = input_validator() #ou directement effectuer_calcul(num1,operator,num2)?
    # Effectuer le calcul
    if operator == '+':
        resultat = num1 + num2
    elif operator == '-':
        resultat = num1 - num2
    elif operator == '*':
        resultat = num1 * num2
    elif operator == '/':
        resultat = num1 / num2

    #Afficher le résultat
    print(f"Résultat : {resultat}")

    #Ajouter à l'historique
    historique.append(f"{num1} {operator} {num2} = {resultat}")

def recommencer_calcul():
    while True:
        effectuer_calcul()

    #Demande à l'utilisateur s'il veut recommencer un calcul.
        while True:
            recommencer = input("Voulez-vous effectuer un autre calcul ? (o pour refaore calcul, n pour retourner au menu) : ").strip().lower()
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
        for operation in historique:
            print(operation)

def effacer_historique():  #efface l'historique des calculs
    if not historique:
        print("Aucun historique à effacer")
    else:
        historique.clear() 
        # pour verifier: print(historique)
        print("Historique effacé")

#Boucle principal mainloop
def main():
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