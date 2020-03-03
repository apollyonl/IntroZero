import math

v = float (input ("Introduce la velocidad del viento: "))
print("La temperatura es en grados Fahrenheit")
t = float (input ("Introduce la temperatura: "))
if (0 <= v <= 4):
    si = t
    print("Índice de sensación térmica: ",si)
elif (v >= 45):
    si = 1.6 * t - 55
    print("Índice de sensación térmica: ",si)
else:
    si = 91.4 + (91.4 - t)*(0.0203 * (math.sqrt (v) - 0.474))
    print("Índice de sensación térmica: ",si)
