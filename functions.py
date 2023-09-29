import globals

def list_of_cart(name, quantity,var):
    globals.listCart.append((name, quantity, var))
    print(globals.listCart)

def get_len():
    length = 0
    for element in globals.listCart:
        length += 1
    return length