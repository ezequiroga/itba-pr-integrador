import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np

pathStocks = 'currentStocks/'
nomAcciones = {}
accionesParaAnalizar = {}
cantidadMaximaDeAcciones = 2

valoresInicioCierreMeses1 = []
valoresInicioCierreMeses2 = []

def getNomAcciones():
    """
        Recorre el directorio de acciones y obtiene los nombres a partir de los nombres de los archivos.
    """
    if (len(nomAcciones) == 0):
        arcAcciones = os.listdir(pathStocks)

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
    return pathStocks + nom + '.csv'

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

def getAccionesParaAnlizar():
    acciones = []
    for unId in accionesParaAnalizar:
        acciones.append(nomAcciones[int(unId)])
    return acciones

def aperturaArchivoAcciones():
    print('\n{:*^50}\n'.format("Abriendo archivos de acciones..."))
    acciones = getAccionesParaAnlizar()

    archivo1 = pd.read_csv(getNombreArchivoAccion(acciones[0]))
    data1 = archivo1.to_dict("list")

    archivo2 = pd.read_csv(getNombreArchivoAccion(acciones[1]))
    data2 = archivo2.to_dict("list")

    return data1, data2

def generarGraficoComparativo():
    print('\n{:*^50}\n'.format("Analizando acciones..."))

    # Inicializacion de variables
    acciones = getAccionesParaAnlizar()

    dateFinAgosto = np.datetime64('2020-09-30')
    dateFinSeptiembre = np.datetime64('2020-09-30')
    dateFinOctubre = np.datetime64('2020-10-31')

    ultimoDiaAgosto = True
    ultimoDiaSeptiembre = True
    ultimoDiaOctubre = True
    #############################

    data1, data2 = aperturaArchivoAcciones()

    # Info de Accion 1
    #archivo1 = pd.read_csv(getNombreArchivoAccion(acciones[0]))
    #data1 = archivo1.to_dict("list")
    cant1 = len(data1["Date"])
    dateReverse1 = data1["Date"][::-1]
    stocksReverse1 = data1["Open"][::-1]
    xAcc1 = []
    yAcc1 = []

    # Info de Accion 2
    #archivo2 = pd.read_csv(getNombreArchivoAccion(acciones[1]))
    #data2 = archivo2.to_dict("list")
    cant2 = len(data2["Date"])
    dateReverse2 = data2["Date"][::-1]
    stocksReverse2 = data2["Open"][::-1]
    xAcc2 = []
    yAcc2 = []

    cantAcciones = cant1
    minimoAcciones = cant2
    if cant1 < cant2 : cantAcciones = cant2
    if cant1 < cant2 : minimoAcciones = cant1

    #Recorro hasta el máximo numero máximo de datos entre ambas
    for i in range(cantAcciones):
        #Si no hay valor para el i, asumo que no hay mas datos para la accion
        #entonces en el except pongo la fecha de la otra acciones y valor 0
        try:
            xAcc1.append(dateReverse1[i])
            yAcc1.append(stocksReverse1[i])
        except:
            xAcc1.append(dateReverse2[i])
            yAcc1.append(0)
        
        try:
            xAcc2.append(dateReverse2[i])
            yAcc2.append(stocksReverse2[i])
        except:
            xAcc2.append(dateReverse1[i])
            yAcc2.append(0)

        if minimoAcciones > i > 0:
            try:
                date=np.datetime64(dateReverse1[i])

                if date <= dateFinOctubre and ultimoDiaOctubre:
                    valoresInicioCierreMeses1.append(stocksReverse1[i])
                    valoresInicioCierreMeses2.append(stocksReverse2[i])
                    ultimoDiaOctubre = False

                if date <= dateFinSeptiembre and ultimoDiaSeptiembre:
                    valoresInicioCierreMeses1.append(stocksReverse1[i-1])
                    valoresInicioCierreMeses2.append(stocksReverse2[i-1])
                    valoresInicioCierreMeses1.append(stocksReverse1[i])
                    valoresInicioCierreMeses2.append(stocksReverse2[i])
                    ultimoDiaSeptiembre = False
                
                if date <= dateFinAgosto and ultimoDiaAgosto:
                    valoresInicioCierreMeses1.append(stocksReverse1[i-1])
                    valoresInicioCierreMeses2.append(stocksReverse2[i-1])
                    ultimoDiaAgosto = False
            except:
                pass

    xAcc1.reverse()
    yAcc1.reverse()
    plt.plot(xAcc1, yAcc1, label = acciones[0])

    xAcc2.reverse()
    yAcc2.reverse()
    plt.plot(xAcc2, yAcc2, label = acciones[1])

    # Calculo de cruces entre las acciones
    print('\n{:*^50}\n'.format("Calculando cruces de valores..."))
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

    print('\n{:*^50}\n'.format("Generando excel de valores de cruce..."))
    df = pd.DataFrame({'Fechas de inversion de valores': crucex})
    df.to_excel("cruces.xlsx")

    # Impresion del grafico comparativo
    print('\n{:*^50}\n'.format("Generando gráfico comparativo..."))
    if cant1 >= cant2:
        plt.xticks(xAcc1[ : :500], rotation=45) # Mostrar una de cada 500 fechas
    else:
        plt.xticks(xAcc2[ : :500], rotation=45) # Mostrar una de cada 500 fechas

    plt.legend()

    plt.savefig('gen-comparativo-' + acciones[0] + '-' + acciones[1] + '.png')
    plt.show()

def generarExcelDiferencias():
    print('\n{:*^50}\n'.format("Analizando alzas y bajas..."))
    acciones = getAccionesParaAnlizar()

    # Calculo de que accion crecio mas en diferentes periodos
    difAcc1Sep = valoresInicioCierreMeses1[2] - valoresInicioCierreMeses1[3]
    difAcc1Oct = valoresInicioCierreMeses1[0] - valoresInicioCierreMeses1[1]

    difAcc2Sep = valoresInicioCierreMeses2[2] - valoresInicioCierreMeses2[3]
    difAcc2Oct = valoresInicioCierreMeses2[0] - valoresInicioCierreMeses2[1]

    textoCrecimientoSep = ''
    if difAcc1Sep > difAcc2Sep:
        tendencia = 'crecio'
        indice = 0
        if difAcc1Sep < 0:
            tendencia = 'bajo'
            indice = 1
        textoCrecimientoSep = 'En Septiembre ' + tendencia + ' mas la accion: ' + acciones[indice]
    elif difAcc1Sep < difAcc2Sep:
        tendencia = 'crecio'
        indice = 1
        if difAcc2Sep < 0:
            tendencia = 'bajo'
            indice = 0
        textoCrecimientoSep = 'En Septiembre ' + tendencia + ' mas la accion: ' + acciones[indice]
    else:
        textoCrecimientoSep = 'Ambas acciones variaron lo mismo en Septiembre.'

    textoCrecimientoOct = ''
    if difAcc1Oct > difAcc2Oct:
        tendencia = 'crecio'
        indice = 0
        if difAcc1Oct < 0:
            tendencia = 'bajo'
            indice = 1
        textoCrecimientoOct = 'En Octubre ' + tendencia + ' mas la accion: ' + acciones[indice]
    elif difAcc1Oct < difAcc2Oct:
        tendencia = 'crecio'
        indice = 1
        if difAcc2Oct < 0:
            tendencia = 'bajo'
            indice = 0
        textoCrecimientoOct = 'En Octubre ' + tendencia + ' mas la accion: ' + acciones[indice]
    else:
        textoCrecimientoOct = 'Ambas acciones variaron lo mismo en Octubre.'

    infoVariaciones = {
        'Precio inicio Septiembre de ' + acciones[0]: valoresInicioCierreMeses1[0],
        'Precio fin Septiembre de ' + acciones[0]: valoresInicioCierreMeses1[1],
        'Precio inicio Octubre de ' + acciones[0]: valoresInicioCierreMeses1[2],
        'Precio fin Octubre de ' + acciones[0]: valoresInicioCierreMeses1[3],
        'Precio inicio Septiembre de ' + acciones[1]: valoresInicioCierreMeses2[0],
        'Precio fin Septiembre de ' + acciones[1]: valoresInicioCierreMeses2[1],
        'Precio inicio Octubre de ' + acciones[1]: valoresInicioCierreMeses2[2],
        'Precio fin Octubre de ' + acciones[1]: valoresInicioCierreMeses2[3],
        'Variacion Septiembre': textoCrecimientoSep,
        'Variacion Octubre': textoCrecimientoOct
    }
    print('\n{:*^50}\n'.format("Generando excel de alzas y bajas..."))
    df = pd.DataFrame.from_dict(infoVariaciones, orient='index')
    df.to_excel("variaciones.xlsx")

def calcularDerivadasDiscretas():
    data1, data2 = aperturaArchivoAcciones()
    acciones = getAccionesParaAnlizar()
    
    print('\n{:*^50}\n'.format("Calculando derivadas de " + acciones[0] + "..."))
    xDer1 = []
    yDer1 = []
    for i in range(1,len(data1["Date"])):
        xDer1.append(data1["Date"][i])
        yDer1.append(data1["Open"][i-1] - data1["Open"][i])
    
    
    plt.plot(xDer1, yDer1, 'm:', label = 'Derivadas ' + acciones[0])
    plt.xticks(xDer1[ : :500], rotation=45) # Mostrar una de cada 500 fechas
    plt.legend()
    print('\n{:*^50}\n'.format("Guardando gráfico de derivadas de " + acciones[0] + "..."))
    plt.savefig('gen-derivadas-' + acciones[0] + '.png')
    print('\n{:*^50}\n'.format("Graficando derivadas de " + acciones[0] + "..."))
    plt.show()

    print('\n{:*^50}\n'.format("Calculando derivadas de " + acciones[1] + "..."))
    xDer2 = []
    yDer2 = []
    for i in range(1,len(data2["Date"])):
        xDer2.append(data2["Date"][i])
        yDer2.append(data2["Open"][i-1] - data2["Open"][i])
    
    plt.plot(xDer2, yDer2, 'm:', label = 'Derivadas ' + acciones[1])
    plt.xticks(xDer2[ : :500], rotation=45) # Mostrar una de cada 500 fechas
    plt.legend()
    print('\n{:*^50}\n'.format("Guardando grafico de derivadas de " + acciones[1] + "..."))
    plt.savefig('gen-derivadas-' + acciones[1] + '.png')
    print('\n{:*^50}\n'.format("Graficando derivadas de " + acciones[1] + "..."))
    plt.show()

print('\n{:*^50}\n'.format("Inicio de la ejecución..."))

ingresoDeAccionesAAnalizar()

generarGraficoComparativo()

generarExcelDiferencias()

calcularDerivadasDiscretas()

print('\n{:*^50}\n'.format("Fin de la ejecución"))
