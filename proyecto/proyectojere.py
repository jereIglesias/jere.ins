# Strategy
from abc import ABC, abstractmethod

class EstrategiaReserva(ABC):
    @abstractmethod
    def asignar_sala(self, salas):
        pass

class EstrategiaAlta(EstrategiaReserva):
    def asignar_sala(self, salas):
        return max(salas, key=lambda s: s.capacidad) if salas else None

class EstrategiaMedia(EstrategiaReserva):
    def asignar_sala(self, salas):
        return salas[0] if salas else None

class EstrategiaBaja(EstrategiaReserva):
    def asignar_sala(self, salas):
        return min(salas, key=lambda s: s.capacidad) if salas else None


# Modelo
class Sala:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.ocupada = False

    def __str__(self):
        return f"{self.nombre} (capacidad: {self.capacidad}, ocupada: {self.ocupada})"

class Empleado:
    def __init__(self, nombre):
        self.nombre = nombre

class Reserva:
    def __init__(self, empleado, estrategia, salas):
        self.empleado = empleado
        self.sala = estrategia.asignar_sala([s for s in salas if not s.ocupada])
        if self.sala:
            self.sala.ocupada = True


# Controlador
class ControladorReservas:
    def __init__(self, salas):
        self.salas = salas
        self.reservas = []

    def crear_reserva(self, empleado, estrategia):
        reserva = Reserva(empleado, estrategia, self.salas)
        if reserva.sala:
            self.reservas.append(reserva)
            return f"✅ Reserva creada en {reserva.sala.nombre} para {empleado.nombre}"
        else:
            return "❌ No hay salas disponibles."

    def cancelar_reserva(self, empleado):
        for r in self.reservas:
            if r.empleado == empleado:
                r.sala.ocupada = False
                self.reservas.remove(r)
                return f"❌ Reserva de {empleado.nombre} cancelada."
        return "⚠ No se encontró una reserva para ese empleado."


# Vista de consola simple
def mostrar_salas(salas):
    print("\n📌 Estado de las salas:")
    for sala in salas:
        print(" -", sala)


# Main
if __name__ == "__main__":
    salas = [Sala("Sala A", 10), Sala("Sala B", 5), Sala("Sala C", 20)]
    controlador = ControladorReservas(salas)

    mostrar_salas(salas)

    jere = Empleado("Jere")
    mati = Empleado("Mati")
    ana = Empleado("Ana")

    print(controlador.crear_reserva(jere, EstrategiaAlta()))
    print(controlador.crear_reserva(mati, EstrategiaBaja()))
    print(controlador.crear_reserva(ana, EstrategiaMedia()))

    mostrar_salas(salas)

    print(controlador.cancelar_reserva(mati))
    mostrar_salas(salas)








