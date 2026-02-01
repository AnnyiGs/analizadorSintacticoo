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
        self.inicio_token = 0

    def sig_simbolo(self):
        self.inicio_token = self.pos

        if self.pos >= len(self.cadena):
            self.tipo = PESOS
            self.simbolo = "$"
            return

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
# Pila
# ----------------------------
class Pila:
    def __init__(self):
        self.datos = []

    def push(self, x):
        self.datos.append(x)

    def pop(self):
        return self.datos.pop()

    def top(self):
        return self.datos[-1]

    def muestra(self):
        salida = ""
        for x in self.datos:
            if x == PESOS:
                salida += "$"
            elif x == MAS:
                salida += "+"
            elif x == E:
                salida += "E"
            elif isinstance(x, str):
                salida += x
            else:
                salida += str(x)
        return salida


# ----------------------------
# Parser LR
# ----------------------------
def parser_lr(cadena, tablaLR, idReglas, lonReglas):
    pila = Pila()
    pila.push(PESOS)
    pila.push(0)

    lexico = Lexico(cadena)
    lexico.sig_simbolo()

    print(f"{'Pila':20} {'Entrada':20} Acción")
    print("-"*55)

    while True:
        estado = pila.top()
        simbolo = lexico.tipo
        accion = tablaLR[estado][simbolo]

        # 👇 ahora sí: entrada REAL pendiente
        entrada_restante = lexico.cadena[lexico.inicio_token:]

        if accion > 0:
            accion_str = f"d{accion}"
        elif accion < 0:
            accion_str = f"r{-accion - 1}"
        elif accion == -1:
            accion_str = "acept"
        else:
            accion_str = "error"

        print(f"{pila.muestra():20} {entrada_restante:20} {accion_str}")

        if accion > 0:  # desplazamiento
            pila.push(lexico.simbolo)
            pila.push(accion)
            lexico.sig_simbolo()

        elif accion < 0:  # reducción
            regla = -accion - 1
            k = lonReglas[regla]

            for _ in range(2 * k):
                pila.pop()

            estado = pila.top()
            pila.push("E")
            pila.push(tablaLR[estado][E])

        else:
            print("Error sintáctico")
            break

        if accion == -1:
            print("Aceptación")
            break


# ----------------------------
# MAIN
# ----------------------------
def main():
    cadena = input("Introduce la cadena a analizar: ")

    tablaLR = [
        # id   +    $    E
        [  5,   0,   0,   1],
        [  0,   6,  -1,   0],
        [  0,  -2,  -2,   0],
        [  5,   0,   0,   4],
        [  0,   6,   0,   0],
        [  0,  -2,  -2,   0],
        [  5,   0,   0,   7],
        [  0,  -1,  -1,   0],
    ]

    idReglas = [E, E]
    lonReglas = [3, 1]

    parser_lr(cadena, tablaLR, idReglas, lonReglas)


if __name__ == "__main__":
    main()