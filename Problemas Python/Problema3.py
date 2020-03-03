a1 = float (input ("Precio por libra paquete A: "))
a2 = float (input ("Porcentaje magro del paquete A: "))
b1 = float (input ("Precio por libra paquete B: "))
b2 = float (input ("Porcentaje magro del paquete B: "))
cla = a1/a2
clb = b1/b2
print("Costo de carne Paquete A: ",cla)
print("Costo de carne Paquete B: ",clb)
if cla > clb:
    print("El paquete B es el mejor")
else:
    print("El paquete A es el mejor")
