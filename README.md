# Proyecto integrador

Para ejecutar el proyecto, descargar este repositorio y ejecutar el archivo final.py.

El programa tiene dos modos de funcionamiento:
1. Comparación entre Amazon y Google, dando la posibilidad al usuario de ingresra un rango de fechas
2. Comparación entre dos acciones elegidas por el usuario

El programa permite seguir operando hasta que el usuario escriba el codigo de salida.

`Todos los archivos son generados en la carpeta raiz del proyecto.`

En la carpeta **currentStocks** están las acciones utilizadas para el ejercicio. Cada CSV contiene el historial completo hasta el 20/11/2020 de las cotizaciones repectivas. Todos los CSV furon descargados de la página de [Yahoo Finance](https://finance.yahoo.com/)

El archivos **grafico_comparativo_google_amazon.png** es el gráfico requerido y se realizó con el histórico completo de las cotizaciones de Amazon y Google hasta el 20/11/2020.

> *NOTA: En la carpeta Stocks hay archivos usados para las pruebas. Datos obtenidos desde [acá](https://github.com/scikit-learn/examples-data/tree/master/financial-data).*

## Modo 1:
1. Se eligen de forma autmática las acciones de Google y Amazon
2. Se le solicita al usuario ingresar el rango de fechas a ser analizado.

Los pasos siguientes se ejecutan sobre el rango seleccionado:

3. Se calculan las intersecciones entre las cotizaciones de ambas acciones.
4. Se guarda un excel con el listado de las fechas en las que ocurrieron las intersecciones.
5. Se guarda y muestra en pantalla el gráfico comparativo de ambas acciones, marcando los puntos de intersección.


## Modo 2
1. Al ejecutar el programa el sistema solicita el ingreso de las 2 acciones a ser analizadas.
2. Se setean de forma automatica el rango desde con fecha 1960-01-01 y rango hasta con fecha 'hoy'
3. Se calculan las intersecciones entre las cotizaciones de ambas acciones.
4. Se guarda un excel con el listado de las fechas en las que ocurrieron las intersecciones.
5. Se guarda y muestra en pantalla el gráfico comparativo de ambas acciones, marcando los puntos de intersección.
6. Se genera un excel con la informacion de que accion crecio/bajo mas en Septiembre, Octubre y los últimos 12 meses.
7. Se calculan las derivadas discretas de cada acción.
8. Se guardan y muestran en pantalla los gráficos de cada una de las derivadas calculadas.

