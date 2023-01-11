import random
import math
import numpy as np
import time

M = 0
E = 0

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
x = -1

### C.I. ###
T = 0

NSE = 0
NSP = 0
NTE = 0
NTP = 0

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
PECPS = 0
PECE = 0
PECES = 0
SPSM = 0
SPSE = 0

STTA = 0


STAE = [0] * E
STAM = [0] * M
SSE = [0] * E
SSM = [0] * M

STOE = [0] * E
STOM = [0] * M

TF = 8 * 365 * 2 * 60  # 2 años de turnos noche (en minutos)


def obtener_primer_puesto_vacio(arreglo):
    for i in range(0, len(arreglo)):
        if arreglo[i] == HV:
            return i
    return -1


def obtener_TA():
    while True:
        R = random.uniform(0, 1)
        TA = 14.5 * math.sqrt(2) * math.sqrt(-math.log(1 - R))
        return TA


def obtener_IA():
    R = random.uniform(0, 1)
    IA = -8.5 * math.log((-1) * math.log(R)) + 5
    return IA 


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

    global T, NSE, NSP, TPLL, SLLM, SSE, SSM, PPS, TF
    global STAM, STAE, STOE, STOM
    global ITOM, ITOE
    global EVENTO
    global PECE, PECP
    global NTP
    global NTE
    global NSP
    global NSE
    global TPSM
    global SLLE
    global TPSE
    global SPSE
    global SPSM
    global x, STTA

    SPSE = SPSE + (TPLL - T) * NSE
    SPSM = SPSM + (TPLL - T) * NSP
    T = TPLL
    IA = obtener_IA()
    TPLL = T + IA
    R = random.uniform(0, 1)

    if R <= 0.7:
        NSP += 1
        if NSP <= M:
            x = obtener_primer_puesto_vacio_medico()
            STOM[x] = STOM[x] + (T - ITOM[x])
            TA = obtener_TA()
            STTA += TA
            TPSM[x] = T + TA
            STAM[x] = STAM[x] + TA

        else:
            if NSP == (M + 1) and NSE < E:
                x = obtener_primer_puesto_vacio_enfermero()
                NSE += 1
                NSP -= 1
                STOE[x] = STOE[x] + (T - ITOE[x])
                TA = obtener_TA()
                STTA += TA
                TPSE[x] = T + TA
                STAE[x] = STAE[x] + TA

    else:
        NSE += 1
        if NSP <= M and NSE <= E:
            x = obtener_primer_puesto_vacio_enfermero()
            STOE[x] = STOE[x] + (T - ITOE[x])
            TA = obtener_TA()
            STTA += TA
            TPSE[x] = T + TA
            STAE[x] = STAE[x] + TA


def resultados():
    global SSM
    global SLLM
    global NTE, NTP
    global PTOE
    global PTOM
    global T
    global PECP
    global PECPS
    global STOM
    global STAM
    global PECE
    global PECES
    global STOE
    global STAE
    global SSE, STTA

    for i in range(0, M):
        PECPS = PECPS + (SPSM - STAM[i])
        PTOM[i] = (STOM[i] * 100) / T

    PECP = PECPS / NTP

    for j in range(0, E):
        PECES = PECES + (SPSE - STAE[j])
        PTOE[j] = (STOE[j] * 100) / T
    PECE = PECES / NTE

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
    global ITOE, ITOM
    global SPSM
    global SPSE
    global NTP
    global NTE, STTA

    while True:
        i = obtener_puesto_menor_tps_medico()
        j = obtener_puesto_menor_tps_enfermero()

        if TPSM[i] <= TPSE[j]:
            # Salida medico
            if TPSM[i] < TPLL:
                EVENTO = "Salida Medico"
                SPSM = SPSM + (TPSM[i] - T) * NSP
                SPSE = SPSE + (TPSM[i] - T) * NSE
                T = TPSM[i]
                NSP -= 1

                if NSP >= M:
                    # Generar TA
                    TA = obtener_TA()
                    STTA += TA
                    TPSM[i] = T + TA
                    STAM[i] = STAM[i] + TA
                else:
                    ITOM[i] = T
                    TPSM[i] = HV
                NTP += 1
            else:
                llegada()
        else:
            if TPSE[j] < TPLL:
                EVENTO = "Salida Enfermero"
                SPSE = SPSE + (TPSE[j] - T) * NSE
                SPSM = SPSM + (TPSE[j] - T) * NSP
                T = TPSE[j]
                NSE -= 1

                if NSP > M:
                    NSE += 1
                    NSP -= 1
                    TA = obtener_TA()
                    STTA += TA
                    TPSE[j] = T + TA
                    STAE[j] = STAE[j] + TA
                else:
                    if NSE >= E and NSP <= M:
                        TA = obtener_TA()
                        STTA += TA
                        TPSE[j] = T + TA
                        STAE[j] = STAE[j] + TA
                    else:
                        ITOE[j] = T
                        TPSE[j] = HV
                NTE += 1
            else:
                llegada()

        if T < TF:
            continue
        else:
            if NSP > 0 or NSE > 0:
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
