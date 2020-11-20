import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates

nomAcciones = {}
accionesParaAnalizar = {}
cantidadMaximaDeAcciones = 2

def getNomAcciones():
    """
        Recorre el directorio de acciones y obtiene los nombres a partir de los nombres de los archivos.
    """
    if (len(nomAcciones) == 0):
        arcAcciones = os.listdir('stocks/')

        for i, unaAcc in enumerate(arcAcciones):
            nomAcciones[i+1] = unaAcc.split('.')[0]

    return nomAcciones

def isIdAccionIngresadoValido(id):
    """
        Verifica que id ingresado se corresponda con una accion elegible.
    """
    max = len(nomAcciones)
    try:
        id = int(id)
    except:
        return False
    return (1 <= id <= max)

def isIdYaIngresado(idAccion):
    """
        Verifica si el ID ingresado ya fue ingresado.
    """
    try:
        idA = accionesParaAnalizar[idAccion]
        return True
    except:
        return False

def isTrueOrFalse(txt):
    """
        Verifica que los valores associados a 'si' y 'no' sean correctos.
    """
    return (txt == 'S' or txt == 's' or txt == 'N' or txt == 'n')

def ingresoUnIdAccion():
    """
        Solicita al usuario el ingreso del ID de una acciones.
    """
    print("\nIngrese el ID de una accion:", end=' ')
    idAccion = input()
    while (not isIdAccionIngresadoValido(idAccion)):
        print('{:-^30}'.format("Id inválido. Intente nuevamente:"), end =' ')
        idAccion = input()
    if (isIdYaIngresado(idAccion)):
        print('{:-^30}'.format("El id " + idAccion + " ya fue ingresado."))
    else:
        accionesParaAnalizar[idAccion] = 1

def preguntarSeguirIngresando():
    """
        Pregunta al usuario si desea seguir ingresando acciones para analizar.
    """
    print("Desea analizar otra acción s/n:", end = ' ')
    tof = input()
    while(not isTrueOrFalse(tof)):
        print('{:-^30}'.format("Respuesta incorrecta. Intente nuevamente:"), end =' ')
        tof = input()
    return tof

def getNombreArchivoAccion(nom):
    return 'stocks/' + nom + '.csv'

def ingresoDeAccionesAAnalizar():
    """
        Inicia el proceso de ingreso de acciones por analizar
    """
    print("{:*^50}".format("Acciones dispobles de ser analizadas"))
    acciones = getNomAcciones()
    
    for unaAccion in acciones:
        print(unaAccion, ':', nomAcciones[unaAccion])

    seguirIngresando = True
    while (seguirIngresando and len(accionesParaAnalizar) < cantidadMaximaDeAcciones):
        ingresoUnIdAccion()
        #tof = preguntarSeguirIngresando()
        #seguirIngresando = (tof == 's' or tof == 'S')

ingresoDeAccionesAAnalizar()

print('\n{:*^50}\n'.format("Generado grafico..."))

acciones = []

for unId in accionesParaAnalizar:
    acciones.append(nomAcciones[int(unId)])

archivo1 = pd.read_csv(getNombreArchivoAccion(acciones[0]))
data1 = archivo1.to_dict("list")
cant1 = len(data1["date"])

xAcc1 = []
yAcc1 = []
xDer1 = []
yDer1 = []
for i in range(cant1):
    xAcc1.append(data1["date"][i])
    yAcc1.append(data1["open"][i])
    if i > 0:
        xDer1.append(data1["date"][i])
        yDer1.append(data1["open"][i] - data1["open"][i-1])

plt.plot(xAcc1, yAcc1, label = acciones[0])
#plt.plot(xDer1, yDer1, 'm:', label = 'Derivadas ' + acciones[0])

archivo2 = pd.read_csv(getNombreArchivoAccion(acciones[1]))
data2 = archivo2.to_dict("list")
cant2 = len(data2["date"])

xAcc2 = []
yAcc2 = []
xDer2 = []
yDer2 = []
for i in range(cant2):
    xAcc2.append(data2["date"][i])
    yAcc2.append(data2["open"][i])
    if i > 0:
        xDer2.append(data2["date"][i])
        yDer2.append(data2["open"][i] - data2["open"][i-1])

plt.plot(xAcc2, yAcc2, label = acciones[1])
#plt.plot(xDer2, yDer2, 'r--', label = 'Derivadas ' + acciones[1])

crucex = []
crucey = []
fechasCruce = []
for i in range(cant1):
    if i > 0 and ((yAcc1[i] == yAcc2[i]) or (yAcc1[i] > yAcc2[i] and yAcc1[i-1] < yAcc2[i-1]) or (yAcc1[i] < yAcc2[i] and yAcc1[i-1] > yAcc2[i-1])):
        if yAcc2[i] >= yAcc1[i]:
            crucex.append(xAcc2[i])
            crucey.append(yAcc2[i])
        else:
            crucex.append(xAcc1[i])
            crucey.append(yAcc1[i])

plt.plot(crucex, crucey, 'k.')

df = pd.DataFrame({'Fechas de inversion de valores': crucex})
df.to_excel("cruces.xlsx")

plt.xticks(xAcc1[ : :200]) # Mostrar una de cada 200 fechas
plt.legend()
plt.show()


plt.plot(xDer1, yDer1, 'm:', label = 'Derivadas ' + acciones[0])
plt.plot(xDer2, yDer2, 'r--', label = 'Derivadas ' + acciones[1])
plt.xticks(xAcc1[ : :200]) # Mostrar una de cada 200 fechas
plt.legend()
plt.show()

print('\n{:*^50}\n'.format("Fin de la ejecución"))
