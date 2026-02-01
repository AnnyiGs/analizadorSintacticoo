ID = 0
MAS = 1
PESOS = 2
E = 3


# ----------------------------
# Analizador Léxico
# ----------------------------
class Lexico:
    def __init__(self, cadena):
        self.cadena = cadena + "$"
        self.pos = 0
        self.simbolo = None
        self.tipo = None
        self.inicio = 0

    def sig_simbolo(self):
        self.inicio = self.pos
        c = self.cadena[self.pos]
        self.pos += 1

        if c.isalpha():
            lexema = c
            while self.pos < len(self.cadena) and self.cadena[self.pos].isalpha():
                lexema += self.cadena[self.pos]
                self.pos += 1
            self.simbolo = lexema
            self.tipo = ID
        elif c == "+":
            self.simbolo = "+"
            self.tipo = MAS
        elif c == "$":
            self.simbolo = "$"
            self.tipo = PESOS
        else:
            raise Exception("Símbolo inválido")


# ----------------------------
# Pila LR
# ----------------------------
class Pila:
    def __init__(self):
        self.datos = []  # estado, símbolo, estado, símbolo...

    def push(self, x):
        self.datos.append(x)

    def pop(self):
        return self.datos.pop()

    def top(self):
        return self.datos[-1]

    def muestra(self):
        s = "$"
        for x in self.datos:
            s += str(x)
        return s


# ----------------------------
# Parser LR
# ----------------------------
def parser_lr(cadena, tablaLR, idReglas, lonReglas):
    pila = Pila()
    pila.push(0)

    lexico = Lexico(cadena)
    lexico.sig_simbolo()

    print(f"{'Pila':12} {'Entrada':18} Acción")
    print("-"*45)

    while True:
        estado = pila.top()
        simbolo = lexico.tipo
        accion = tablaLR[estado][simbolo]

        entrada_restante = lexico.cadena[lexico.inicio:]

        if accion > 0:
            accion_str = f"d{accion}"
        elif accion < 0:
            accion_str = f"r{-accion}"
        elif accion == -1:
            accion_str = "acept"
        else:
            accion_str = "error"

        print(f"{pila.muestra():12} {entrada_restante:18} {accion_str}")

        if accion > 0:  # shift
            pila.push(lexico.simbolo)
            pila.push(accion)
            lexico.sig_simbolo()

        elif accion < 0:  # reducción
            regla = -accion - 1

            # Validar que la regla esté dentro del rango de lonReglas
            if regla < 0 or regla >= len(lonReglas):
                print(f"Error: índice de regla fuera de rango ({regla}).")
                break

            k = lonReglas[regla]

            # Validar que la pila tenga suficientes elementos antes de hacer pop
            if len(pila.datos) < 2 * k:
                print("Error: la pila no tiene suficientes elementos para la reducción.")
                print(f"Estado actual de la pila: {pila.muestra()}")
                print(f"Regla: {regla}, Longitud esperada: {2 * k}, Elementos en la pila: {len(pila.datos)}")
                break

            for _ in range(2 * k):
                pila.pop()

            estado = pila.top()
            pila.push(E)
            pila.push(tablaLR[estado][E])

        elif accion == -1:
            print("Aceptación")
            break

        else:
            print("Error sintáctico")
            print(f"Estado: {estado}, Símbolo: {simbolo}")
            break


# ----------------------------
# MAIN
# ----------------------------
def main():
    cadena = input("Introduce la cadena a analizar: ")

    # Gramática: E -> id + E | id
    idReglas = [E, E]  # Ambas reglas producen E
    lonReglas = [3, 1]  # Longitudes de las reglas: 3 para "id + E", 1 para "id"

    # Tabla LR ajustada para la gramática
    tablaLR = [
        # id   +    $    E
        [  2,   0,   0,   1],  # Estado 0
        [  0,   3,  -1,   0],  # Estado 1 (Aceptación en $)
        [  0,  -2,  -2,   0],  # Estado 2 (Reducción por regla 2)
        [  2,   0,   0,   4],  # Estado 3
        [  0,   3,   0,   0],  # Estado 4
        [  0,  -2,  -2,   0],  # Estado 5
        [  2,   0,   0,   7],  # Estado 6
        [  0,  -1,  -1,   0],  # Estado 7 (Aceptación final)
    ]

    parser_lr(cadena, tablaLR, idReglas, lonReglas)


if __name__ == "__main__":
    main()
