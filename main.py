"""
main.py
========
Programa principal del Sistema de Gestión de Vehículos.

Muestra un menú interactivo en consola para registrar, consultar y
administrar una flota de coches y motos, demostrando herencia y
polimorfismo. La lógica de negocio vive en las clases; aquí solo se
gestiona la interacción con el usuario.

Autor: Javier Martínez Andrade
Materia: Programación Orientada a Objetos
Actividad 2 - Tema 3: Herencia
"""

from clases.vehiculos import Vehiculo, Coche, Moto


# ---------------------------------------------------------------------- #
#                       FUNCIONES AUXILIARES                             #
# ---------------------------------------------------------------------- #
def mostrar_menu():
    """Imprime el menú principal."""
    print("\n" + "=" * 40)
    print("  🚗 SISTEMA DE GESTIÓN DE VEHÍCULOS 🏍️")
    print("=" * 40)
    print("1.  Registrar coche")
    print("2.  Registrar moto")
    print("3.  Mostrar flota")
    print("4.  Encender/Apagar vehículo")
    print("5.  Calcular alquiler")
    print("6.  Alquilar vehículo")
    print("7.  Devolver vehículo")
    print("8.  Ver estadísticas")
    print("9.  Dar de baja vehículo")
    print("10. Salir")
    print("=" * 40)


def pedir_año():
    """Pide un año y lo valida con el método estático de la clase."""
    año = int(input("Año: "))
    if not Vehiculo.validar_año(año):
        raise ValueError("El año debe ser mayor a 1900 y no superar el año actual.")
    return año


def pedir_precio():
    """Pide el precio base y lo valida con el método estático de la clase."""
    precio = float(input("Precio base de alquiler: "))
    if not Vehiculo.validar_precio(precio):
        raise ValueError("El precio base debe ser un número positivo.")
    return precio


def pedir_entero_positivo(mensaje):
    """Pide un entero positivo (para puertas o cilindrada)."""
    valor = int(input(mensaje))
    if valor <= 0:
        raise ValueError("El valor debe ser un entero positivo.")
    return valor


def seleccionar_vehiculo(flota):
    """Muestra la flota numerada y devuelve el vehículo elegido."""
    if not flota:
        print("⚠️  No hay vehículos registrados todavía.")
        return None

    print("\nFlota actual:")
    for i, v in enumerate(flota, start=1):
        tipo = type(v).__name__
        print(f"  {i}. {v.marca} {v.modelo} ({tipo})")

    indice = int(input("Seleccione el número del vehículo: ")) - 1
    if indice < 0 or indice >= len(flota):
        raise IndexError("Ese número de vehículo no existe en la flota.")
    return flota[indice]


# ---------------------------------------------------------------------- #
#                   OPCIONES DEL MENÚ (acciones)                         #
# ---------------------------------------------------------------------- #
def registrar_coche(flota):
    """Opción 1: registra un coche en la flota."""
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    año = pedir_año()
    precio = pedir_precio()
    puertas = pedir_entero_positivo("Número de puertas: ")

    coche = Coche(marca, modelo, año, precio, puertas)
    flota.append(coche)


def registrar_moto(flota):
    """Opción 2: registra una moto en la flota."""
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    año = pedir_año()
    precio = pedir_precio()
    cilindrada = pedir_entero_positivo("Cilindrada (cc): ")

    moto = Moto(marca, modelo, año, precio, cilindrada)
    flota.append(moto)


def mostrar_flota(flota):
    """Opción 3: muestra la información de toda la flota (polimorfismo)."""
    if not flota:
        print("⚠️  No hay vehículos registrados todavía.")
        return

    print("\n========== FLOTA DE VEHÍCULOS ==========")
    for v in flota:
        # Polimorfismo: cada vehículo muestra su información específica.
        v.mostrar_info()
    print("========================================")


def encender_apagar(flota):
    """Opción 4: alterna el estado del motor del vehículo elegido."""
    v = seleccionar_vehiculo(flota)
    if v is None:
        return
    if v.encendido:
        v.apagar()
    else:
        v.encender()


def calcular_alquiler(flota):
    """Opción 5: calcula el costo de alquiler del vehículo elegido."""
    v = seleccionar_vehiculo(flota)
    if v is None:
        return
    if not v.disponible:
        print(f"⚠️  {v.marca} {v.modelo} está alquilado; no se puede cotizar.")
        return

    unidad = "días" if isinstance(v, Coche) else "horas"
    tiempo = int(input(f"Tiempo de alquiler ({unidad}): "))
    if tiempo <= 0:
        raise ValueError("El tiempo debe ser un número positivo.")

    costo = v.calcular_alquiler(tiempo)
    print(f"💲 Costo de alquiler de {v.marca} {v.modelo}: ${costo:.2f}")


def alquilar_vehiculo(flota):
    """Opción 6: marca un vehículo como alquilado."""
    v = seleccionar_vehiculo(flota)
    if v:
        v.alquilar()


def devolver_vehiculo(flota):
    """Opción 7: marca un vehículo como devuelto."""
    v = seleccionar_vehiculo(flota)
    if v:
        v.devolver()


def ver_estadisticas(flota):
    """Opción 8: muestra estadísticas de la flota."""
    encendidos = sum(1 for v in flota if v.encendido)
    coches = sum(1 for v in flota if isinstance(v, Coche))
    motos = sum(1 for v in flota if isinstance(v, Moto))

    print("\n📊 ESTADÍSTICAS DE LA FLOTA")
    print(f"  Total de vehículos : {Vehiculo.total_vehiculos()}")
    print(f"  Motores encendidos : {encendidos}")
    print(f"  Coches             : {coches}")
    print(f"  Motos              : {motos}")


def dar_de_baja(flota):
    """Opción 9: elimina un vehículo de la flota (activa el destructor)."""
    v = seleccionar_vehiculo(flota)
    if v:
        flota.remove(v)
        del v  # invoca el destructor __del__


# ---------------------------------------------------------------------- #
#                          PROGRAMA PRINCIPAL                            #
# ---------------------------------------------------------------------- #
def main():
    flota = []  # lista de vehículos registrados

    print("¡Bienvenido al sistema de gestión de la agencia de vehículos!")

    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                registrar_coche(flota)
            elif opcion == "2":
                registrar_moto(flota)
            elif opcion == "3":
                mostrar_flota(flota)
            elif opcion == "4":
                encender_apagar(flota)
            elif opcion == "5":
                calcular_alquiler(flota)
            elif opcion == "6":
                alquilar_vehiculo(flota)
            elif opcion == "7":
                devolver_vehiculo(flota)
            elif opcion == "8":
                ver_estadisticas(flota)
            elif opcion == "9":
                dar_de_baja(flota)
            elif opcion == "10":
                print("\n¡Gracias por usar el sistema! Hasta pronto. 👋")
                break
            else:
                print("⚠️  Opción no válida. Elige un número del 1 al 10.")

        except ValueError as error:
            # Errores de conversión y de validación.
            print(f"❌ Error: {error}")
        except IndexError as error:
            # Índices de vehículo fuera de rango.
            print(f"❌ Error: {error}")
        except Exception as error:
            # Red de seguridad para cualquier otro error inesperado.
            print(f"❌ Ocurrió un error inesperado: {error}")


if __name__ == "__main__":
    main()
