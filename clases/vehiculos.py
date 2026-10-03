"""
vehiculos.py
=============
Jerarquía de clases para el Sistema de Gestión de Vehículos.

Contiene:
    - Vehiculo   -> clase base
    - Coche      -> clase derivada (se alquila por día)
    - Moto       -> clase derivada (se alquila por hora)

Conceptos aplicados (Unidad 3 - Herencia):
    * Herencia y reutilización de miembros con super().
    * Redefinición (override) de métodos: calcular_alquiler().
    * Extensión de métodos: mostrar_info().
    * Polimorfismo en tiempo de ejecución.
    * Atributo de clase, métodos de clase (@classmethod),
      métodos estáticos (@staticmethod) y propiedades (@property).
    * Constructor (__init__) y destructor (__del__).

Autor: Javier Martínez Andrade
"""

from datetime import datetime


class Vehiculo:
    """Clase base que representa un vehículo genérico de la flota."""

    # Atributo de clase: compartido por TODAS las instancias.
    _contador_vehiculos = 0

    def __init__(self, marca, modelo, año, precio_base):
        """Constructor: inicializa los atributos del vehículo."""
        self.marca = marca                 # público
        self.modelo = modelo               # público
        self.año = año                     # público
        self.precio_base = precio_base     # público
        self._encendido = False            # protegido: motor apagado al inicio
        self._disponible = True            # protegido: disponible para alquilar

        Vehiculo._contador_vehiculos += 1  # se cuenta en la CLASE
        print(f"🚗 Vehículo registrado: {marca} {modelo} ({año})")

    def __del__(self):
        """Destructor: se ejecuta al dar de baja un vehículo."""
        print(f"🗑️ {self.marca} {self.modelo} ha sido dado de baja.")
        Vehiculo._contador_vehiculos -= 1

    # ================================================================== #
    #                           PROPIEDADES                              #
    # ================================================================== #
    @property
    def encendido(self):
        """Estado del motor (solo lectura)."""
        return self._encendido

    @property
    def disponible(self):
        """Disponibilidad del vehículo (solo lectura)."""
        return self._disponible

    # ================================================================== #
    #                       MÉTODOS DE INSTANCIA                         #
    # ================================================================== #
    def encender(self):
        """Enciende el motor si no estaba encendido."""
        if self._encendido:
            print(f"⚠️  {self.marca} {self.modelo}: El motor ya estaba encendido.")
            return
        self._encendido = True
        print(f"🔑 {self.marca} {self.modelo}: Motor encendido.")

    def apagar(self):
        """Apaga el motor si estaba encendido."""
        if not self._encendido:
            print(f"⚠️  {self.marca} {self.modelo}: El motor ya estaba apagado.")
            return
        self._encendido = False
        print(f"🔒 {self.marca} {self.modelo}: Motor apagado.")

    def calcular_alquiler(self, tiempo):
        """
        Calcula el costo de alquiler base.

        Este método se REDEFINE en las clases derivadas, ya que los coches
        cobran por día y las motos por hora.
        """
        return self.precio_base * tiempo

    def mostrar_info(self):
        """Muestra la información del vehículo. Se EXTIENDE en las derivadas."""
        estado_motor = "Encendido" if self._encendido else "Apagado"
        disponibilidad = "Disponible" if self._disponible else "Alquilado"
        print("──────────────────────────────────────────")
        print(f"  {self.marca} {self.modelo} ({self.año})")
        print(f"  Precio base : ${self.precio_base}")
        print(f"  Motor       : {estado_motor}")
        print(f"  Estado      : {disponibilidad}")

    def alquilar(self):
        """Marca el vehículo como alquilado. Lanza error si ya lo estaba."""
        if not self._disponible:
            raise ValueError(f"{self.marca} {self.modelo} ya está alquilado.")
        self._disponible = False
        print(f"✅ {self.marca} {self.modelo} ha sido alquilado.")

    def devolver(self):
        """Marca el vehículo como devuelto. Lanza error si no estaba alquilado."""
        if self._disponible:
            raise ValueError(f"{self.marca} {self.modelo} no estaba alquilado.")
        self._disponible = True
        print(f"✅ {self.marca} {self.modelo} ha sido devuelto.")

    # ================================================================== #
    #                        MÉTODOS DE CLASE                            #
    # ================================================================== #
    @classmethod
    def total_vehiculos(cls):
        """Devuelve cuántos vehículos están activos (registrados)."""
        return cls._contador_vehiculos

    @classmethod
    def crear_desde_diccionario(cls, datos):
        """Constructor alternativo: crea un vehículo a partir de un diccionario."""
        return cls(datos["marca"], datos["modelo"],
                   datos["año"], datos["precio_base"])

    # ================================================================== #
    #                        MÉTODOS ESTÁTICOS                           #
    # ================================================================== #
    @staticmethod
    def validar_año(año):
        """Verifica que el año sea mayor a 1900 y no supere el año actual."""
        return 1900 < año <= datetime.now().year

    @staticmethod
    def validar_precio(precio):
        """Verifica que el precio sea un número positivo."""
        return isinstance(precio, (int, float)) and precio > 0


# ====================================================================== #
#                          CLASES DERIVADAS                              #
# ====================================================================== #
class Coche(Vehiculo):
    """Coche: se alquila por día, con un recargo por número de puertas."""

    def __init__(self, marca, modelo, año, precio_base, num_puertas):
        # Reutiliza el constructor de la clase base con super().
        super().__init__(marca, modelo, año, precio_base)
        self.num_puertas = num_puertas

    def calcular_alquiler(self, dias):
        """Redefine el cálculo: cobra por día más un recargo por puertas."""
        return self.precio_base * dias + (self.num_puertas * 10)

    def mostrar_info(self):
        # Extiende el método base: primero lo reutiliza y añade lo suyo.
        super().mostrar_info()
        print("  Tipo        : Coche 🚗")
        print(f"  Puertas     : {self.num_puertas}")

    def abrir_maletero(self):
        """Método propio del coche."""
        print(f"🧳 {self.marca} {self.modelo}: Maletero abierto.")


class Moto(Vehiculo):
    """Moto: se alquila por hora, con un recargo por cilindrada."""

    def __init__(self, marca, modelo, año, precio_base, cilindrada):
        super().__init__(marca, modelo, año, precio_base)
        self.cilindrada = cilindrada

    def calcular_alquiler(self, horas):
        """Redefine el cálculo: cobra por hora más un recargo por cilindrada."""
        return self.precio_base * horas + (self.cilindrada * 0.5)

    def mostrar_info(self):
        super().mostrar_info()
        print("  Tipo        : Moto 🏍️")
        print(f"  Cilindrada  : {self.cilindrada} cc")

    def hacer_caballito(self):
        """Método propio de la moto."""
        print(f"🏍️ {self.marca} {self.modelo}: ¡Haciendo caballito!")
