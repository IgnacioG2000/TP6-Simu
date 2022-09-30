import random
import math
import numpy as np
from scipy import special
import time

HV = 10000

def obtener_primer_puesto_vacio(arreglo):
    for i in range(0, len(arreglo)):
        if arreglo[i] == HV:
            return i
    return -1

def obtener_puesto_menor_tps_de_arreglo(arreglo):
    minTPSLista = HV
    minTPSListaIndex = 0

    for i in range(0, len(arreglo)):
        if arreglo[i] < minTPSLista:
            minTPSLista = arreglo[i]
            minTPSListaIndex = i

    return minTPSListaIndex

lista = [1000,1000,1000,1000]

print(obtener_puesto_menor_tps_de_arreglo(lista))

