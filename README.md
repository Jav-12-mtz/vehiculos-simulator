# 🚗 Sistema de Gestión de Vehículos 🏍️

Sistema por consola en **Python** para administrar la flota de una agencia de
alquiler de vehículos. Permite registrar **coches** y **motos**, encender/apagar
el motor, calcular el costo de alquiler, alquilar y devolver unidades, consultar
estadísticas y dar de baja vehículos.

Es el proyecto de la **Actividad 2 – Tema 3: Herencia** de la materia
**Programación Orientada a Objetos** (ITA – Educación a Distancia). Aplica
**herencia**, **reutilización de miembros con `super()`**, **redefinición de
métodos** y **polimorfismo**.

---

## 📂 Estructura del proyecto

```
vehiculos_simulator/
│
├── main.py              # Menú interactivo y lógica de interacción
├── README.md            # Este archivo
└── clases/
    ├── __init__.py
    └── vehiculos.py     # Clase base Vehiculo + clases derivadas
```

- **`clases/vehiculos.py`** contiene la lógica de negocio (qué es un vehículo y qué sabe hacer).
- **`main.py`** contiene la interfaz: el menú y la interacción con el usuario.

---

## 🧬 Jerarquía de clases

| Clase      | Hereda de  | Se alquila por | Atributo propio | `calcular_alquiler`                     |
|------------|------------|----------------|-----------------|-----------------------------------------|
| `Vehiculo` | —          | (base)         | —               | `precio_base * tiempo`                  |
| `Coche`    | `Vehiculo` | **día**        | `num_puertas`   | `precio_base * dias + num_puertas * 10` |
| `Moto`     | `Vehiculo` | **hora**       | `cilindrada`    | `precio_base * horas + cilindrada * 0.5`|

Cada clase derivada:

- Reutiliza el constructor de la base con `super().__init__()`.
- **Redefine** `calcular_alquiler()` (sin `super()`, porque la regla de negocio es distinta).
- **Extiende** `mostrar_info()` reutilizando `super().mostrar_info()` y añadiendo su dato propio.

---

## ⚙️ Cómo funciona

### Clase base `Vehiculo`
- **Atributos:** `marca`, `modelo`, `año`, `precio_base` (públicos); `_encendido`, `_disponible` (protegidos); `_contador_vehiculos` (de clase).
- **Constructor / destructor:** registran el vehículo (y suman al contador) / lo dan de baja (y restan al contador).
- **Métodos de instancia:** `encender()`, `apagar()`, `calcular_alquiler()`, `mostrar_info()`, `alquilar()` y `devolver()` (estos dos **lanzan excepción** si el estado no lo permite).
- **Métodos de clase (`@classmethod`):** `total_vehiculos()` y `crear_desde_diccionario()` (constructor alternativo).
- **Métodos estáticos (`@staticmethod`):** `validar_año()` y `validar_precio()`.
- **Propiedades (`@property`):** `encendido` y `disponible` (solo lectura).

### Polimorfismo
El menú guarda todos los vehículos en una misma lista y los trata por igual. Al
llamar `v.mostrar_info()` o `v.calcular_alquiler(t)`, Python ejecuta la versión
de la clase concreta (`Coche` o `Moto`) sin que el menú necesite saber el tipo.

---

## ▶️ Cómo ejecutar

Requisitos: **Python 3.8 o superior** (sin librerías externas).

```bash
# 1. Clona el repositorio
git clone https://github.com/Jav-12-mtz/vehiculos-simulator.git

# 2. Entra a la carpeta del proyecto
cd vehiculos-simulator

# 3. Ejecuta el programa
python main.py
```

> 💡 En Windows, si no se ven los emojis en la consola, ejecuta antes
> `chcp 65001` o usa la **Terminal de Windows**.

---

## 📋 Menú de opciones

| Opción | Acción | Concepto demostrado |
|:------:|--------|---------------------|
| 1  | Registrar coche            | Constructor + herencia (`super()`) |
| 2  | Registrar moto             | Constructor + herencia (`super()`) |
| 3  | Mostrar flota              | Polimorfismo + extensión de `mostrar_info()` |
| 4  | Encender/Apagar vehículo   | Métodos de instancia + propiedades |
| 5  | Calcular alquiler          | Redefinición de `calcular_alquiler()` |
| 6  | Alquilar vehículo          | Cambio de estado + excepción |
| 7  | Devolver vehículo          | Cambio de estado + excepción |
| 8  | Ver estadísticas           | Método de clase + `isinstance` |
| 9  | Dar de baja vehículo       | Destructor (`__del__`) |
| 10 | Salir                      | Cierre del programa |

---

## 🛡️ Validaciones y manejo de errores

- El **año** debe ser mayor a 1900 y no superar el año actual (`validar_año()`).
- El **precio base** debe ser un número positivo (`validar_precio()`).
- El **número de puertas** y la **cilindrada** deben ser enteros positivos.
- No se calcula el alquiler de un vehículo que está alquilado.
- Los **índices fuera de rango** se manejan con `IndexError`.
- `alquilar()` y `devolver()` **lanzan excepción** si el estado no lo permite.
- Todo se captura con `try/except` para mostrar mensajes claros.

---

## 👤 Autor

**Javier Martínez Andrade**
Programación Orientada a Objetos — Tema 3: Herencia
Instituto Tecnológico de Aguascalientes — Educación a Distancia
