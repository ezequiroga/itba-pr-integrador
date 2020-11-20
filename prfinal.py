import os

nomAcciones = {}
accionesParaAnalizar = {}

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

def ingresoDeAccionesAAnalizar():
    """
        Inicia el proceso de ingreso de acciones por analizar
    """
    print("{:*^50}".format("Acciones dispobles de ser analizadas"))
    acciones = getNomAcciones()
    
    for unaAccion in acciones:
        print(unaAccion, ':', nomAcciones[unaAccion])

    seguirIngresando = True
    while (seguirIngresando):
        ingresoUnIdAccion()
        tof = preguntarSeguirIngresando()
        seguirIngresando = (tof == 's' or tof == 'S')



ingresoDeAccionesAAnalizar()
