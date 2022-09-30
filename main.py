import random
import math
import numpy as np
from scipy import special
import time

M = 2
E = 5

while True:
    try:
        ### VARIABLES DE CONTROL ###
        M = int(input("Cantidad de medicos (M): "))
        E = int(input("Cantidad de enfermeros (E): "))

        break
    except ValueError:
        print("\nError: Solo se permiten numeros enteros.\n")
        continue

HV = 6666666666666
iterationIndex = 0
EVENTO = "C.I."

i = -1
j = -1

### C.I. ###
T = 0

NSE = 0
NSP = 0
NT = 0

ITOE = [0] * E
ITOM = [0] * M

TPSE = [HV] * E
TPSM = [HV] * M

TPLL = 0
SLLE = [0] * E
SLLM = [0] * M

PPS = 0
PTOE = [0] * E
PTOM = [0] * M
PECP = 0
PECE = 0

STAE = [0] * E
STAM = [0] * M
SSE = [0] * E
SSM = [0] * M

STOE = [0] * E
STOM = [0] * M

TF = 500000  # 48 semanas (en minutos)


def obtener_primer_puesto_vacio(arreglo):
    for i in range(0, len(arreglo)):
        if arreglo[i] == HV:
            return i
    return -1


def obtener_TA():
    while True:
        R = random.uniform(0, 1)
        TA = 14.5 * math.sqrt(2) * math.sqrt(-math.log(1 - R)) + 5
        print(f"Se genero un TA: {TA}")
        return TA
 



def obtener_IA():
    R = random.uniform(0.0390502529816, 1)
    IA = -8.5 * math.log((-1) * math.log(R)) + 10
    print(f"Se genero un IA: {IA}")
    return  IA  + 5


def obtener_primer_puesto_vacio_medico():
    return obtener_primer_puesto_vacio(TPSM)


def obtener_primer_puesto_vacio_enfermero():
    return obtener_primer_puesto_vacio(TPSE)


def obtener_puesto_menor_tps_de_arreglo(arreglo):
    minTPSLista = HV
    minTPSListaIndex = 0

    for i in range(0, len(arreglo)):
        if arreglo[i] < minTPSLista:
            minTPSLista = arreglo[i]
            minTPSListaIndex = i

    return minTPSListaIndex


def obtener_puesto_menor_tps_medico():
    return obtener_puesto_menor_tps_de_arreglo(TPSM)


def obtener_puesto_menor_tps_enfermero():
    return obtener_puesto_menor_tps_de_arreglo(TPSE)


def llegada():
    global i, j
    global T, NSE, NSP, TPLL, SLLM, SSE, SSM, PPS, TF
    global STAM, STAE, STOE, STOM
    global ITOM
    global EVENTO
    global PECE, PECP
    global NT
    global NSP
    global NSE
    global TPSM
    global SLLE
    global TPSE

    T = TPLL
    IA = obtener_IA()
    TPLL = T + IA
    R = random.uniform(0, 1)

    if R <= 0.24: 
        print("Entre al if 24")
        NSP += 1
        if NSP <= M:
            x = obtener_primer_puesto_vacio_medico()
            print(f"el medico {x} va a atender CP")
            SLLM[x] = SLLM[x] + T
            STOM[x] = STOM[x] + (T - ITOM[x])
            TA = obtener_TA()
            TPSM[x] = T + TA
            STAM[x] = STAM[x] + TA
            print(f"el medico {x} ya atendio CP")
        else:
            if NSP == (M + 1) and NSE < E:
                x = obtener_primer_puesto_vacio_enfermero()
                print(f"el enfermero {x} va a atender CP")
                SLLE[x] = SLLE[x] + T
                NSE += 1
                NSP -= 1
                STOE[x] = STOE[x] + (T - ITOE[x])
                TA = obtener_TA()
                TPSE[x] = T + TA
                STAE[x] = STAE[x] + TA
                print(f"el enfermero {x} ya atendio CP")

    else:
        print("Else al if 24")
        NSE += 1
        if NSP < M and NSE <= E:
            x = obtener_primer_puesto_vacio_enfermero()
            print(f"el enfermero {x} va a atender CN")
            SLLE[x] = SLLE[x] + T
            STOE[x] = STOE[x] + (T - ITOE[x])
            TA = obtener_TA()
            TPSE[x] = T + TA
            STAE[x] = STAE[x] + TA
            print(f"el enfermero {x} ya atendio CN")
    
    NT += 1
    print("Termino la llegada / sali del if 24")



def resultados():
    global PPS
    global SSM
    global SLLM
    global NT
    global PTOE
    global PTOM
    global T

    for i in range(0, M):
        sumatoria_permamencia_medico = SSM[i] - SLLM[i]
        PECP = (SSM[i] - SLLM[i] - STAM[i]) / NT
        PTOM[i] = (STOM[i] * 100) / T
        print(f"SSM {i} = {SSM[i]} / SLLM {i} = {SLLM[i]} / STAM {i} ={STAM[i]} / {SSM[i]-SLLM[i]-STAM[i]}")

    for j in range(0, E):
        sumatoria_permamencia_enfermero = SSE[j] - SLLE[j]
        PECE = (SSE[j] - SLLE[j] - STAE[j]) / NT
        PTOE[j] = (STOE[j] * 100) / T
        print(f"SSE {j} = {SSE[j]} / SLLE {j} = {SLLE[j]} / STAE {j} ={STAE[j]} / {SSE[i]-SLLE[i]-STAE[i]}")

    #PPS = (sumatoria_permamencia_enfermero + sumatoria_permamencia_medico) / NT

    #print(f"Promedio de permanencia en el sistema: {PPS}")
    print(f"Promedio de espera en cola de medicos: {PECP}")
    print(f"Promedio de espera en cola de enfermeros: {PECE}")

    for i in range(0, M):
        print(f"porcentaje de tiempo ocioso del medico {i} es: {PTOM[i]}")

    for j in range(0, E):
        print(f"porcentaje de tiempo ocioso del enfermero {j} es: {PTOE[j]}")


def realizar_simulacion():
    global i, j
    global T, NSE, NSP, TPLL, SLL, SSE, SSM, PPS, TF
    global STAM, STAE, STOE, STOM
    global EVENTO
    global PECE, PECP
    global TPSM
    global TPSE

    while True:
        i = obtener_puesto_menor_tps_medico()
        j = obtener_puesto_menor_tps_enfermero()

        if TPSM[i] <= TPSE[j]:
            # Salida medico
            if TPSM[i] < TPLL:
                EVENTO = "Salida Medico"
                T = TPSM[i]
                print(f"El medico {i} tuvo una salida")
                NSP -= 1

                if NSP >= M:
                    # Generar TA
                    TA = obtener_TA()
                    TPSM[i] = T + TA
                    STAM[i] = STAM[i] + TA
                else:
                    ITOM[i] = T
                    print(f"El medico {i} esta ocioso")
                    TPSM[i] = HV

                SSM[i] = SSM[i] + T
            else:
                print(f"TPSM {i}: {TPSM[i]} / TPSE {j} {TPSE[j]} / TPLL {TPLL} ")
                llegada()
        else:
            if TPSE[j] < TPLL:
                EVENTO = "Salida Enfermero"
                T = TPSE[j]
                print(f"HAY NSE: {NSE}")
                NSE -= 1
                print(f"El enfermero {j} tuvo una salida, quedan en NSE: {NSE}")

                if NSP > M:
                    NSE += 1
                    NSP -= 1
                    TA = obtener_TA()
                    TPSE[j] = T + TA
                    STAE[j] = STAE[j] + TA
                else:
                    if NSE >= E:
                        TA = obtener_TA()
                        TPSE[j] = T + TA
                        STAE[j] = STAE[j] + TA
                    else:
                        ITOE[j] = T
                        print(f"El enfermero {j} se esta rascando :s")
                        TPSE[j] = HV

                SSE[j] = SSE[j] + T
            else:
                llegada()

        if T < TF:
            continue
        else:
            print("Entre AL VACIAMIENTO")
            if NSP > 0 or NSE > 0:
                print(f"NSE {NSE} / NSP {NSP}")
                TPLL = HV
                continue
            else:
                break

    resultados()


def main():
    print("\n\n### Comenzando simulacion ###\n\n")
    realizar_simulacion()
    print("\nFinalizando simulacion...")


# Cosa de python que no importa
if __name__ == "__main__":
    main()
