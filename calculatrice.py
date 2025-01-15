# Méthode des variables intermédiaires 
def calcule(num1, operator, num2):

    result = "Opérateur invalide"  # Valeur par défaut si l'opérateur est incorrect

    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = num1 / num2 if num2 != 0 else "Division par zéro impossible"
    elif operator == '%':
        result = num1 % num2

    return result

try:
    m = int(input('Veuillez entrer un nombre entier : '))
    
    while True:
        n = input('Veuillez entrer un opérateur (+, -, *, /, %) : ')
        if n in ['+', '-', '*', '/', '%']:
            break
        else:
            print("Vous n'avez pas rentré un opérateur valide. Réessayez.")
    
    o = int(input('Veuillez entrer un autre nombre entier : '))
    
    resultat = calcule(m, n, o)
    print(f"Résultat : {resultat}")
except ValueError:
    print("Attention ! Ce n'est pas un nombre entier.")