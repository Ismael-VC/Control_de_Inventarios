#!/usr/bin/env python3


'''
Programa para administrar inventarios.
'''


import pandas as pd
import subprocess as sp
import sys
import time


__author__ = 'Ismael Venegas Castelló'
__email__ = 'ismael.vc1337@gmail.com'
__contributors__ = ['Javier Cardenas - Jdash99']
__copyright__ = 'Copyright 2014, {0}'.format(__author__)
__date__ = '01/07/2014'
__licence__ = 'GPL v2'
__version__ = '0.2.0'
__status__ = 'Inestable'


def limpia():
    ''' Limpia la pantalla.'''
    plataforma = sys.platform
    if plataforma.startswith('linux'):
        sp.call('clear')
    elif plataforma.startswith('win'):
        sp.call('cls', shell=True)


def pausa():
    '''Permite realizar pausas dentro de un bucle.'''
    input("\n\nPresione enter para continuar. ")


def generar_tabla():
    columnas = ['ENTRADA',
                'SALIDA',
                'EXISTENCIA',
                'UNITARIO',
                'MEDIO',
                'DEBE',
                'HABER',
                'SALDO']
    tabla = pd.DataFrame(columns=columnas)
    return tabla


def pedir_datos(tabla, cantidad=0.0, unitario=0.0):
    opcion = input('CONTROL DE INVENTARIO\n\n'
                   'Seleccione una opción:\n'
                   '  c: Compras\n'
                   '  v: Ventas\n'
                   '  m: Movimientos\n'
                   '  s: Salir\n\n'
                   '=> ').lower()
    opciones_permitidas = ['c', 'v', 'm', 's']

    if opcion in opciones_permitidas:
        if opcion == 'c':
            cantidad = float(input('\n\nCantidad de unidades: '))
            unitario = float(input('Precio unitario: '.rjust(22)))

        elif opcion == 'v' and not tabla.empty:
            cantidad = float(input('\n\nCantidad de unidades: '))

        elif opcion == 'm':
            if not tabla.empty:
                imprimir_inventario(tabla)
            else:
                print('\n\n[!] Debe hacer algun movimiento primero.')

        elif opcion == 's':
            sys.exit(0)

        return opcion, cantidad, unitario


def ingresar_datos(datos, tabla, indice):
    '''Ingresa una nueva fila de datos a la tabla del inventario.'''
    opcion, cantidad, unitario = datos

    if opcion == 'c':
        entrada = cantidad
        salida = 0.0
        medio = 0.0
        debe = cantidad * unitario
        haber = 0.0

        if indice == 0: # Si es la primera compra.
            existencia = entrada
            saldo = debe
        else:
            existencia = tabla['EXISTENCIA'][indice-1] + cantidad
            saldo = tabla['SALDO'][indice-1] + debe

    elif opcion == 'v' and not tabla.empty:
        entrada = 0.0
        salida = cantidad
        existencia = tabla['EXISTENCIA'][indice-1] - cantidad
        debe = 0.0
        medio = tabla['DEBE'][indice-1] / tabla['EXISTENCIA'][indice-1]

        if medio == 0.0: # Por que hubo una venta anterior.
            # Buscar el ultimo valor de "medio", que no sea 0.
            indice_2 = indice
            while tabla['MEDIO'][indice_2-1] == 0.0:
                indice_2 -= 1
            medio = tabla['MEDIO'][indice_2-1]

        haber = cantidad * medio
        saldo = tabla['SALDO'][indice-1] - haber

    elif opcion == 'v':
        print('\n\n[!] Inventario vacio.')

    if opcion == 'c' or (opcion == 'v' and not tabla.empty):
        hora = time.strftime("%H:%M:%S")
        tabla.loc[hora, :] = [entrada,
                              salida,
                              existencia,
                              unitario,
                              medio,
                              debe,
                              haber,
                              saldo]
        imprimir_inventario(tabla)


def imprimir_inventario(tabla):
    fecha = time.strftime("%d/%m/%Y")
    print('\n\n' + fecha, end ='\n\n')
    print(tabla, end='\n')


def main():
    tabla = generar_tabla()
    indice = 0

    while True:
        try:
            limpia()
            datos = pedir_datos(tabla)
            opcion = datos[0]
            ingresar_datos(datos, tabla, indice)

            if opcion == 'c' or (opcion == 'v' and not tabla.empty):
                indice += 1
            pausa()

        except (ValueError, TypeError):
            print('\n\n[!] Intente de nuevo.')
            pausa()


if __name__ == '__main__':
    main()
