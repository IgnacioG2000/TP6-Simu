
import random
import math

HV = 66666

def obtener_IA():
    R = random.uniform(0.0390502529816, 1)
    IA = -8.5 * math.log((-1) * math.log(R)) + 10

    return IA

def obtener_TA():
    while True:
        R = random.uniform(0, 1)
        TA = 14.5 * math.sqrt(2) * math.sqrt(-math.log(1 - R)) + 5
        return TA
      

while True:
    IA = obtener_IA()
    TA = obtener_TA()
    print(f"Se genero un IA: {IA}")
    print(f"Se genero un TA: {TA}") 
    print(f"RESTA: {IA-TA}")
   
