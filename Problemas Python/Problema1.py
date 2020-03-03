torni = 5
tuerc = 3
aran = 1
tor = int (input ("Introduce número de tornillos: "))
tuer = int (input ("Introduce número de tuercas: "))
ar = int (input ("Introduce número de arandeles: "))
suma = tor * torni + tuer * tuerc + ar * aran
if tor > tuer:
    print("Verifica el pedido")
    print("Costo Total: ",suma)
else:
    print("Costo Total: ",suma)
