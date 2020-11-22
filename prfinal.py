import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import re

pathStocks = 'currentStocks/'
nomAcciones = {}
accionesParaAnalizar = {}
accionesParaAnalizarNombre = []
cantidadMaximaDeAcciones = 2

rangoFechaDesde = 0
rangoFechaHasta = 0

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

def isValidFormatoFecha(fecha):
    return (re.match('\\d{4}-{1}\\d{2}-{1}\\d{2}', fecha) != None)

def isFechaMenorHoy(fecha):
    return (np.datetime64(fecha) <= np.datetime64('today'))

def ingresoFecha(tipo):
    formatoValido = False
    fechaMenorHoy = False

    print("Ingrese la fecha " + tipo + ": ", end = '')
    fecha = input()
    while (not formatoValido or not fechaMenorHoy):
        formatoValido = isValidFormatoFecha(fecha)
        while not formatoValido:
            print("Formato inválido!")
            print("Ingrese la fecha " + tipo + " nuevamente: ", end = '')
            fecha = input()
            formatoValido = isValidFormatoFecha(fecha)
        
        fechaMenorHoy = isFechaMenorHoy(fecha)
        if not fechaMenorHoy:
            print("La fecha ingresa no puede ser posterior a la de hoy!")
            print("Ingrese la fecha " + tipo + " nuevamente: ", end = '')
            fecha = input()
    
    return fecha

def ingresoDeRangoDeFechas():
    print('\n{:*^50}\n'.format("Ingreso de rango de fechas..."))
    print('\n{:^50}\n'.format("+++ Debe ingresar las fechas con el siguiente formato AAAA-MM-DD +++"))

    dateDesde = 0
    dateHasta = 0

    rangoCorrecto = False

    while not rangoCorrecto:
        fechaDesde = ingresoFecha('DESDE')
        fechaHasta = ingresoFecha('HASTA')
        
        dateDesde = np.datetime64(fechaDesde)
        dateHasta = np.datetime64(fechaHasta)

        if dateDesde <= dateHasta:
            rangoCorrecto = True
        else:
            print("La fecha DESDE del rango no puede ser mayor a la fecha HASTA!\n")
    
    return dateDesde, dateHasta

def getAccionesParaAnlizar():
    for unId in accionesParaAnalizar:
        accionesParaAnalizarNombre.append(nomAcciones[int(unId)])

def aperturaArchivoAcciones():
    print('\n{:*^50}\n'.format("Abriendo archivos de acciones..."))

    print('\n{:=>50}\n'.format("Abriendo archivo de " + accionesParaAnalizarNombre[0]))
    archivo1 = pd.read_csv(getNombreArchivoAccion(accionesParaAnalizarNombre[0]))
    #######
    archivo1FiltradoDesde = archivo1[archivo1.apply(lambda x: np.datetime64(x['Date']) >= rangoFechaDesde, axis = 1 )]
    archivo1FiltradoHasta = archivo1FiltradoDesde[archivo1FiltradoDesde.apply(lambda x: np.datetime64(x['Date']) <= rangoFechaHasta, axis = 1 )]
    data1 = archivo1FiltradoHasta.to_dict("list")
    #######
    # data1 = archivo1.to_dict("list")

    print('\n{:=>50}\n'.format("Abriendo archivo de " + accionesParaAnalizarNombre[1]))
    archivo2 = pd.read_csv(getNombreArchivoAccion(accionesParaAnalizarNombre[1]))
    #######
    archivo2FiltradoDesde = archivo2[archivo2.apply(lambda x: np.datetime64(x['Date']) >= rangoFechaDesde, axis = 1 )]
    archivo2FiltradoHasta = archivo2FiltradoDesde[archivo2FiltradoDesde.apply(lambda x: np.datetime64(x['Date']) <= rangoFechaHasta, axis = 1 )]
    data2 = archivo2FiltradoHasta.to_dict("list")
    #######
    # data2 = archivo2.to_dict("list")

    return data1, data2

def generarGraficoComparativo():
    print('\n{:*^50}\n'.format("Analizando acciones..."))

    # Inicializacion de variables
    acciones = accionesParaAnalizarNombre

    dateFinAgosto = np.datetime64('2020-09-30')
    dateFinSeptiembre = np.datetime64('2020-09-30')
    dateFinOctubre = np.datetime64('2020-10-31')

    ultimoDiaAgosto = True
    ultimoDiaSeptiembre = True
    ultimoDiaOctubre = True
    #############################

    data1, data2 = aperturaArchivoAcciones()

    # Info de Accion 1
    cant1 = len(data1["Date"])
    dateReverse1 = data1["Date"][::-1]
    stocksReverse1 = data1["Open"][::-1]
    xAcc1 = []
    yAcc1 = []

    # Info de Accion 2
    cant2 = len(data2["Date"])
    dateReverse2 = data2["Date"][::-1]
    stocksReverse2 = data2["Open"][::-1]
    xAcc2 = []
    yAcc2 = []

    cantAcciones = cant1
    minimoAcciones = cant2
    if cant1 < cant2 : cantAcciones = cant2
    if cant1 < cant2 : minimoAcciones = cant1

    date01=np.datetime64(dateReverse1[0])
    date02=np.datetime64(dateReverse2[0])
    diaUnoAnio1 = 0
    diaUnoAnio2 = 0
    #Recorro hasta el numero máximo de datos entre ambas
    difAnio = np.timedelta64(365, 'D')
    for i in range(cantAcciones):
        #Si no hay valor para el i, asumo que no hay mas datos para la accion
        #entonces en el except pongo la fecha de la otra acciones y valor 0
        try:
            xAcc1.append(dateReverse1[i])
            yAcc1.append(stocksReverse1[i])

            date = np.datetime64(dateReverse1[i])
            if (date01 - date) >= difAnio and diaUnoAnio1 == 0:
                diaUnoAnio1 = i
        except:
            xAcc1.append(dateReverse2[i])
            yAcc1.append(0)
        
        try:
            xAcc2.append(dateReverse2[i])
            yAcc2.append(stocksReverse2[i])

            date = np.datetime64(dateReverse2[i])
            if (date02 - date) >= difAnio and diaUnoAnio2 == 0:
                diaUnoAnio2 = i
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

    valoresInicioCierreMeses1.append(stocksReverse1[0])
    valoresInicioCierreMeses1.append(stocksReverse1[diaUnoAnio1])
    valoresInicioCierreMeses2.append(stocksReverse2[0])
    valoresInicioCierreMeses2.append(stocksReverse2[diaUnoAnio2])

    xAcc1.reverse()
    yAcc1.reverse()
    plt.plot(xAcc1, yAcc1, label = accionesParaAnalizarNombre[0])

    xAcc2.reverse()
    yAcc2.reverse()
    plt.plot(xAcc2, yAcc2, label = accionesParaAnalizarNombre[1])

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
    if len(crucex) == 0:
        mensaje = 'Las cotizaciones de las acciones no se cruzaron en el periodo seleccionado'
        df = pd.DataFrame.from_dict({'Fechas de inversion de valores': mensaje}, orient='index')
    else:
        df = pd.DataFrame({'Fechas de inversion de valores': crucex})
    df.to_excel("cruces.xlsx")

    # Impresion del grafico comparativo
    print('\n{:*^50}\n'.format("Generando gráfico comparativo..."))
    if cant1 >= cant2:
        plt.xticks(xAcc1[ : :500], rotation=45) # Mostrar una de cada 500 fechas
    else:
        plt.xticks(xAcc2[ : :500], rotation=45) # Mostrar una de cada 500 fechas

    plt.legend()

    plt.savefig('gen-comparativo-' + accionesParaAnalizarNombre[0] + '-' + accionesParaAnalizarNombre[1] + '.png')
    plt.show()

def generarExcelDiferencias():
    print('\n{:*^50}\n'.format("Analizando alzas y bajas..."))

    # Calculo de que accion crecio mas en diferentes periodos
    difAcc1Oct = valoresInicioCierreMeses1[1] - valoresInicioCierreMeses1[0]
    difAcc1Sep = valoresInicioCierreMeses1[3] - valoresInicioCierreMeses1[2]
    difAcc1Anual = valoresInicioCierreMeses1[4] - valoresInicioCierreMeses1[5]
    
    difAcc2Oct = valoresInicioCierreMeses2[1] - valoresInicioCierreMeses2[0]
    difAcc2Sep = valoresInicioCierreMeses2[3] - valoresInicioCierreMeses2[2]
    difAcc2Anual = valoresInicioCierreMeses2[4] - valoresInicioCierreMeses2[5]

    textoCrecimientoSep = ''
    if difAcc1Sep > difAcc2Sep:
        tendencia = 'crecio'
        indice = 0
        if difAcc1Sep < 0:
            tendencia = 'bajo'
            indice = 1
        textoCrecimientoSep = 'En Septiembre ' + tendencia + ' mas la accion: ' + accionesParaAnalizarNombre[indice]
    elif difAcc1Sep < difAcc2Sep:
        tendencia = 'crecio'
        indice = 1
        if difAcc2Sep < 0:
            tendencia = 'bajo'
            indice = 0
        textoCrecimientoSep = 'En Septiembre ' + tendencia + ' mas la accion: ' + accionesParaAnalizarNombre[indice]
    else:
        textoCrecimientoSep = 'Ambas acciones variaron lo mismo en Septiembre.'

    textoCrecimientoOct = ''
    if difAcc1Oct > difAcc2Oct:
        tendencia = 'crecio'
        indice = 0
        if difAcc1Oct < 0:
            tendencia = 'bajo'
            indice = 1
        textoCrecimientoOct = 'En Octubre ' + tendencia + ' mas la accion: ' + accionesParaAnalizarNombre[indice]
    elif difAcc1Oct < difAcc2Oct:
        tendencia = 'crecio'
        indice = 1
        if difAcc2Oct < 0:
            tendencia = 'bajo'
            indice = 0
        textoCrecimientoOct = 'En Octubre ' + tendencia + ' mas la accion: ' + accionesParaAnalizarNombre[indice]
    else:
        textoCrecimientoOct = 'Ambas acciones variaron lo mismo en Octubre.'

    textoCrecimientoAnual = ''
    if difAcc1Anual > difAcc2Anual:
        tendencia = 'crecio'
        indice = 0
        if difAcc1Anual < 0:
            tendencia = 'bajo'
            indice = 1
        textoCrecimientoAnual = 'En los últimos 12 mese ' + tendencia + ' mas la accion: ' + accionesParaAnalizarNombre[indice]
    elif difAcc1Anual < difAcc2Anual:
        tendencia = 'crecio'
        indice = 1
        if difAcc2Anual < 0:
            tendencia = 'bajo'
            indice = 0
        textoCrecimientoAnual = 'En los últimos 12 mese ' + tendencia + ' mas la accion: ' + accionesParaAnalizarNombre[indice]
    else:
        textoCrecimientoAnual = 'En los últimos 12 mese ambas acciones variaron lo mismo.'

    infoVariaciones = {
        'Precio inicio Septiembre de ' + accionesParaAnalizarNombre[0]: valoresInicioCierreMeses1[0],
        'Precio fin Septiembre de ' + accionesParaAnalizarNombre[0]: valoresInicioCierreMeses1[1],
        'Precio inicio Octubre de ' + accionesParaAnalizarNombre[0]: valoresInicioCierreMeses1[2],
        'Precio fin Octubre de ' + accionesParaAnalizarNombre[0]: valoresInicioCierreMeses1[3],
        'Precio hace un año ' + accionesParaAnalizarNombre[0]: valoresInicioCierreMeses1[5],
        'Ultimo precio ' + accionesParaAnalizarNombre[0]: valoresInicioCierreMeses1[4],

        'Precio inicio Septiembre de ' + accionesParaAnalizarNombre[1]: valoresInicioCierreMeses2[0],
        'Precio fin Septiembre de ' + accionesParaAnalizarNombre[1]: valoresInicioCierreMeses2[1],
        'Precio inicio Octubre de ' + accionesParaAnalizarNombre[1]: valoresInicioCierreMeses2[2],
        'Precio fin Octubre de ' + accionesParaAnalizarNombre[1]: valoresInicioCierreMeses2[3],
        'Precio hace un año ' + accionesParaAnalizarNombre[1]: valoresInicioCierreMeses2[5],
        'Ultimo precio ' + accionesParaAnalizarNombre[1]: valoresInicioCierreMeses2[4],

        'Variacion Septiembre': textoCrecimientoSep,
        'Variacion Octubre': textoCrecimientoOct,
        'Variacion en los ultimos 12 meses': textoCrecimientoAnual
    }

    print('\n{:*^50}\n'.format("Generando excel de alzas y bajas..."))
    df = pd.DataFrame.from_dict(infoVariaciones, orient='index')
    df.to_excel("variaciones.xlsx")

def calcularDerivadasDiscretas():
    data1, data2 = aperturaArchivoAcciones()
    
    print('\n{:*^50}\n'.format("Calculando derivadas de " + accionesParaAnalizarNombre[0] + "..."))
    xDer1 = []
    yDer1 = []
    for i in range(1,len(data1["Date"])):
        xDer1.append(data1["Date"][i])
        yDer1.append(data1["Open"][i-1] - data1["Open"][i])
    
    
    plt.plot(xDer1, yDer1, 'm:', label = 'Derivadas ' + accionesParaAnalizarNombre[0])
    plt.xticks(xDer1[ : :500], rotation=45) # Mostrar una de cada 500 fechas
    plt.legend()
    print('\n{:*^50}\n'.format("Guardando gráfico de derivadas de " + accionesParaAnalizarNombre[0] + "..."))
    plt.savefig('gen-derivadas-' + accionesParaAnalizarNombre[0] + '.png')
    print('\n{:*^50}\n'.format("Graficando derivadas de " + accionesParaAnalizarNombre[0] + "..."))
    plt.show()

    print('\n{:*^50}\n'.format("Calculando derivadas de " + accionesParaAnalizarNombre[1] + "..."))
    xDer2 = []
    yDer2 = []
    for i in range(1,len(data2["Date"])):
        xDer2.append(data2["Date"][i])
        yDer2.append(data2["Open"][i-1] - data2["Open"][i])
    
    plt.plot(xDer2, yDer2, 'm:', label = 'Derivadas ' + accionesParaAnalizarNombre[1])
    plt.xticks(xDer2[ : :500], rotation=45) # Mostrar una de cada 500 fechas
    plt.legend()
    print('\n{:*^50}\n'.format("Guardando grafico de derivadas de " + accionesParaAnalizarNombre[1] + "..."))
    plt.savefig('gen-derivadas-' + accionesParaAnalizarNombre[1] + '.png')
    print('\n{:*^50}\n'.format("Graficando derivadas de " + accionesParaAnalizarNombre[1] + "..."))
    plt.show()

print('\n{:*^50}\n'.format("Inicio de la ejecución..."))

print("----- Ingrese una opcion -----")
print("1: Comparación entre Amazon y Google")
print("2: Comparar 2 acciones a eleccion")
ingreso = 0
while ingreso != '1' and ingreso != '2':
    print("Ingrese una opción: ", end= ' ')
    ingreso = input()

if ingreso == '1':
    accionesParaAnalizarNombre.append('AMZN')
    accionesParaAnalizarNombre.append('GOOG')

    rangoFechaDesde, rangoFechaHasta = ingresoDeRangoDeFechas()

    generarGraficoComparativo()

else:
    ingresoDeAccionesAAnalizar()

    rangoFechaDesde = np.datetime64('1960-01-01')
    rangoFechaHasta = np.datetime64('today')

    getAccionesParaAnlizar()

    generarGraficoComparativo()

    generarExcelDiferencias()

    calcularDerivadasDiscretas()

print('\n{:*^50}\n'.format("Fin de la ejecución"))
