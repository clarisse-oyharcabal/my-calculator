#In this version, I will define only one function in which I will use numpy operators for addition, multiplication .....
#import the necessary libraries :
import numpy as np
import matplotlib.pyplot as plt

#######################################################################
#define the functions :
# - Define a scientific calculator due to the library numpy :
def calculator_science(a, b, operator) : 
    operators = {
        #the trigonometrical functions
        'cos' : lambda: np.cos(a), 
        'sin' : lambda: np.sin(a),
        'tan' : lambda: np.tan(a),
        #the trigonometrical inverse functions
        'arccos' : lambda: np.arccos(a) if -1 <= a <= 1 else "Input out of range [-1, 1]",
        'arcsin' : lambda: np.arcsin(a) if -1 <= a <= 1 else "Input out of range [-1, 1]",
        'arctan' : lambda: np.arctan(a),
        #the hyperbolic functions
        'cosh' : lambda: np.cosh(a),
        'sinh' : lambda: np.sinh(a),
        'tanh' : lambda: np.tanh(a),
        #the hyperbolic inverse functions
        'arccosh' : lambda: np.arccosh(a) if a >= 1 else "Input must be >= 1",
        'arcsinh' : lambda: np.arcsinh(a),
        'arctanh' : lambda: np.arctanh(a) if -1 < a < 1 else "Input out of range (-1, 1)",
        #other functions
        'log' : lambda: np.log10(a) if a >= 0 else 'Error: Negative value',
        'ln' : lambda: np.log(a) if a >= 0 else 'Error: Negative value',
        'exp' : lambda: np.exp(a),
        'abs' : lambda: np.abs(a),
        'root' : lambda: np.sqrt(a) if a >= 0 else 'Error: Negative value below the root',
    }

    #If we create the dictionnary in this way : dict ={'cos' : np.cos(a)}, that means that this operation is done before we call it in the input bloc
    #The solution is to make these functions (operators) as a lambda function or like a reference, then at the end we put it like an arguments in operators.get()
    result = operators.get(operator, lambda:  "Unfound operation")()  #execute the lambda function
    return result #it return a numerical variable, that I can use in the condition down (to round the result if necessary)
     #the programm recuperate the key : operator from the dictionnary operators, if the operator doen't exist, the function return : Unfound operation

def calculator_two(a, b, operator) : 
    if operator == '+' :
        result = a + b

    elif operator == '-' :
        result = a - b

    elif operator == 'x' :
        result = a * b

    elif operator == '/' :
        if b != 0 :
            result = a / b
        else :
            result = "Zero Division Error ! Enter another number b " 

    elif operator == '//' :
        if b != 0 :
            result = a // b
        else :
            result = "Zero Division Error ! Enter another number b "
    elif operator == '%' :
        if b != 0 : 
            result = a % b
        else :
            result = "Zero Division Error ! Enter another number b " 

    return result

def calculator_three(a, b, c, operator1, operator2) : 
    if operator1 == '+' and operator2 == '+' :
         result = a + b + c
    elif operator1 == '-' and operator2 == '-' :
         result = a - b - c
    elif operator1 == '+' and operator2 == '-' :
         result = a + b - c
    elif operator1 == '-' and operator2 == '+' :
         result = a - b + c
    elif operator1 == '+' and operator2 == 'x' :
         result_ = b * c
         result = a + result_
    elif operator1 == '-' and operator2 == 'x' :
         result_ = b * c
         result = a - result
    elif operator1 == 'x' and operator2 == '+' :
         result_ = a * b
         result = result_ + c 
    elif operator1 == 'x' and operator2 == '-' :
         result_ = a * b 
         result = result_ - c
    elif operator1 == 'x' and operator2 == 'x' :
         result = a * b * c
    elif operator1 == '+' and operator2 == '/' :
         result_ = b / c
         result = a + result_
    elif operator1 == '-' and operator2 == '/' :
         result = b / c
         result = a - result_
    elif operator1 == '/' and operator2 == '+' :
         result_ = a / b 
         result = result_ + c
    elif operator1 == '/' and operator2 == '-' :
         result_ = a / b 
         result = result_ - c
    elif operator1 == '/' and operator2 == '/' :
         result = a / b / c
    elif operator1 == 'x' and operator2 == '/' :
         result = a * b / c
    elif operator1 == '/' and operator2 == 'x' :
         result = a / b * c

    return result 
#def advanced calculator () : in construction
    

###########################################################################################################""

#Ask the user the enter the values
  
print(f"\n--------------------------- Welcome to our calculator !-------------------------------\n")
print(f"\n**************************************************************************\n")
try :
    while True :

        choice0 = input(f"If you want to active the basic calculator write 'b' and if you want the scientific one write 's'").strip().lower()
        
        #######################################################
        
        if choice0 == 'b' :
            while True :
                choice1 = input(f"\nDo you want to operate with 2 or 3 variables ?").strip()
                if choice1 == '2' :
                    print(f"\nWelcome to the : 2-variables basic calculator : ")
                    operate = input(f"- Enter the operation symbol '+'  '-'  'x'  '/'  '//'  '%'   : ").strip()
                    if operate not in ['+', '-', 'x', '/', '//', '%'] :
                        print(f"Invalide choice, please try again")
                    else : 
                        try :
                            number1 = float(input(f"- Enter a first number a : "))
                            number2 = float(input(f"- Enter a second number b : "))
                            result1 = calculator_two(number1, number2, operate)
                            print(f"The result of the operation : {number1} {operate} {number2} = {result1}")
                        except ValueError :
                            print(f"Enter a numeric value")

                elif choice1 == '3' :
                    print(f"Welcome to the : 3-variables basic calculator : ")
                    operate1 = input(f"- Enter the first operation symbol '+'  '-'  'x'  '/'   : ").strip()
                    if operate1 not in ['+', '-', 'x', '/'] :
                        print(f"Invalide choice, please enter one of these symbols : '+'  '-'  'x'  '/' ")
                    else :
                        operate2 = input(f"- Enter the second operation symbol '+'  '-'  'x'  '/'   : ").strip()
                        if operate2 not in ['+', '-', 'x', '/'] :
                            print(f"Invalide choice, please enter one of these symbols : '+'  '-'  'x'  '/' ")
                        else :
                            try :
                                number1 = float(input(f"- Enter a first number a : "))
                                number2 = float(input(f"- Enter a second number b : "))
                                number3 = float(input(f"- Enter a first number a : "))
                                result5 = calculator_three(number1, number2, number3, operate1, operate2)
                                print(f"The result of the operation : {number1}{operate1}{number2}{operate2}{number2} = {result5}")
                            except ValueError :
                                print(f"Enter a numeric value")

                else :
                    print(f" --!-- Invalide choice. Please enter '2' or '3' ")


                retry = input(f"Do you want to execute another basic calculation (Yes / No)? ").strip().lower()
                if retry != 'yes' :
                    print(f"Thank you. Good Bye !")
                    exit()
                
                
                ##################################################

        if choice0 =='s' :
            print(f"2 - Choose Trigo to operate with trigonometrical")
            print(f"3 - Choose other for other scientific operations")

            while True : #when the entered value or symbol is not valid, there is a printed message but I want that my programme is executed again to allow the user to enter the values or the symbols again
            #I add while True before each input, in order to ask the user to try again, if the entered value is not valid

                choice2 = input(f"\n- Do you want to operate with 'Trigo' or 'other' ? ").strip().lower()
                if choice2 == 'trigo' : 
                    print(f"\nYou are operating with trigonometrical functions")
                    print(f"\n5 - Choose 'TF' if you want to operate with trigonometrical functions")
                    print(f"6 - Choose 'TIF' if you want to operate with trigonometrical inverse functions")
                    choice3 = input(f" Do you want 'TF' or 'TIF' ? ").strip().upper()

                    if choice3 == 'TF' :
                        operate = input(f"\n- Enter the operation symbol 'cos'  'sin'  'tan'   'cosh'  'sinh'  'tanh' : ").strip()
                        number = float(input(f"- Enter a number of your choice n : "))
                        result2 = calculator_science(np.radians(number), operate)
                        if np.abs(result2) < 1e-10 :
                            result2 = 0.0  #because in python for example cos(pi/2) != 0 exactly
                        print(f"The result of the operation : {operate}({number}) = {result2}")

                    elif choice3 == 'TIF' :
                        operate = input(f"\n- Enter the operation symbol 'arccos'  'arcsin'  'arctan'  'arccosh' 'arcsinh'  'arctanh' : ").strip()
                        number = float(input(f"- Enter a number of your choice n : "))
                        result3 = calculator_science(number, operate)
                        print(f"The result of the operation : {operate}({number}) = {np.radians(result3)}")

                    else :
                        print(f"\n --!-- Invalide choice. Please enter 'TF' or 'TIF' ")

                                    

                elif choice2 == 'other' :
                    operate = input(f"\n- Enter the operation symbol 'log'  'ln'  'exp'  'abs'  'root' : ").strip()
                    number = float(input(f"- Enter a number of your choice n : "))
                    result4 = calculator_science(number, operate)
                    print(f"The result of the operation : {operate}({number}) = {result4}")

                else :
                    print(f" --!-- Invalide choice. Please enter 'trigo' or 'other' ")


                retry = input(f"Do you want to run again this calculator (Yes / No)? ").strip().lower()
                if retry != 'yes' :
                    print(f"Thank you. Good Bye !")
                    exit()

        retry = input(f"Do you want to execute another calculation (Yes / No)? ").strip().lower()
        if retry != 'yes' :
            print(f"Thank you. Good Bye !")
            exit()    
                
            
except KeyboardInterrupt :
        print(f"\nExiting ......")