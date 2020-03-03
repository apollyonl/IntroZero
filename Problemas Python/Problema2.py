t = int (input ("Capacidad del tanque: "))
print("Porcentaje del medidor de gas: ")

m = int (input ("Lectura del Medidor: "))
mi = int (input ("Millas por galon: "))
g = t * (m/100) * mi
if g > 200:
    print("¡Procede!")
else:
    print("¡Consigue gasolina ya!")
