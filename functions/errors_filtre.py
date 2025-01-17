def errors_filtre(validated):
    if valid_number_1:
        print("valid_number_1 is True")




# number_1, operator, number_2, 
# valid_number_1,
# valid_operator, valid_sqrt_operation, valid_division_operation,
# valid_number_2

"""number_1 = 23.0
operator = "/"
number_2 = 10.0
valid_number_1 = True
valid_operator = True
valid_sqrt_operation = True
valid_division_operation = True
valid_number_2 = True"""

validated = (23.0, '/', 3.0, True, True, True, True, True)

print(errors_filtre(validated))