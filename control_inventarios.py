#!/usr/bin/env python3


'''
Por hacer:

  · Checar que no se retire mas de lo que hay disponible en inventario.
  · Usar decimal.Decimal en vez de floats.
  · Implementar métodos: PEPS, UEPS y PPP.
'''


from sys import exit, platform
from pandas import DataFrame
from subprocess import call, check_output
from time import strftime


__author__ = 'Ismael Venegas Castelló'
__email__ = 'ismael.vc1337@gmail.com'
__copyright__ = 'Copyright 2014, {0}'.format(__author__)
__date__ = '01/07/2014'
__licence__ = 'GPLv2'
__version__ = '0.1.0'
__status__ = 'Inestable'


def limpia():
  ''' Limpia la pantalla.'''
  plataforma = platform

  if plataforma.startswith('linux'):
    call('clear')

  elif plataforma.startswith('win'):
    call('cls', shell=True)


def pausa():
  '''Permite realizar pausas dentro de un bucle.'''
  input("\n\nPresione enter para continuar. ")


def reiniciar():
  pausa()
  limpia()
  main()


def generar_tabla():
  columnas = ['ENTRADA',
              'SALIDA',
              'EXISTENCIA',
              'UNITARIO',
              'MEDIO',
              'DEBE',
              'HABER',
              'SALDO']

  tabla = DataFrame(columns=columnas)
  return tabla


def pedir_datos(tabla, cantidad=0.0, unitario=0.0):
  opciones_permitidas = ['c', 'v', 'm', 's']
  opcion = input('CONTROL DE INVENTARIO\n\n'
                 'Seleccione una opción:\n'
                 '  c: Compras\n'
                 '  v: Ventas\n'
                 '  m: Movimientos\n'
                 '  s: Salir\n\n'
                 '=> ').lower()

  if opcion in opciones_permitidas:
    if opcion == 'c' or (opcion == 'v' and not tabla.empty):
        cantidad = float(input('\nCantidad de unidades: '))

    if opcion == 'v' and not tabla.empty:
      print()

    if opcion == 'c':
      unitario = float(input('Precio unitario: '.rjust(22)))
      print()

    elif opcion == 's':
      exit(0)

    return opcion, cantidad, unitario

  else:
    print('\n\n[!] Opción invalida: "{0}"'.format(opcion))
    reiniciar()


def ingresar_datos(datos, tabla, indice):
  '''Ingresa una nueva fila de datos a la tabla del inventario.'''
  opcion, cantidad, unitario = datos

  if opcion == 'c' and indice != 0:
    entrada    = cantidad
    salida     = tabla['SALIDA'][indice-1]
    existencia = tabla['EXISTENCIA'][indice-1] + cantidad
    medio      = 0.0
    debe       = cantidad * unitario
    haber      = tabla['HABER'][indice-1]
    saldo      = tabla['SALDO'][indice-1] + debe

  elif opcion == 'c':
    entrada    = cantidad
    salida     = 0.0
    existencia = entrada
    medio      = 0.0
    debe       = cantidad * unitario
    haber      = 0.0
    saldo      = debe

  elif opcion == 'v' and indice != 0:
    entrada    = 0.0
    salida     = cantidad
    existencia = tabla['EXISTENCIA'][indice-1] - cantidad
    debe       = 0.0
    medio      = tabla['DEBE'][indice-1] / tabla['EXISTENCIA'][indice-1]
    haber      = cantidad * medio
    saldo      = tabla['SALDO'][indice-1] - haber

  elif opcion == 'v':
    print('\n\n[!] Inventario vacio.')
    reiniciar()

  elif opcion == 'm' and tabla.empty:
    print('\n\n[!] Debe hacer algun movimiento primero.')

  else:
    print()
    imprimir_inventario(tabla)

  if opcion == 'c' or (opcion == 'v' and not tabla.empty):
    hora = strftime("%H:%M:%S")
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
  fecha = strftime("%d/%m/%Y")
  print('\n' + fecha, end='\n\n')
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

    except ValueError:
      print('\n\n[!] Intente de nuevo.')
      pausa()


if __name__ == '__main__':
  # import pdb; pdb.set_trace()
  main()
