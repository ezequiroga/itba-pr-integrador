import os

def getNomAcciones():
    arcAcciones = os.listdir('stocks/')
    nomAcciones = []

    for unaAcc in arcAcciones:
        nomAcciones.append(unaAcc.split('.')[0])

    return nomAcciones

print(getNomAcciones())
