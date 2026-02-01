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
        s = ""
        for x in self.datos:
            if x == PESOS:
                s += "$"
            elif x == MAS:
                s += "+"
            elif x == E:
                s += "E"
            elif isinstance(x, str):
                s += x
            else:
                s += str(x)
        return s


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

        # Formatear la pila como una cadena con estados y símbolos separados correctamente
        pila_formateada = "$ " + " ".join(
            str(pila.datos[i]) if i % 2 == 0 else pila.datos[i] for i in range(len(pila.datos))
        )

        # Formatear la entrada restante
        entrada_restante = lexico.cadena[lexico.inicio:]

        # Formatear la acción
        if accion > 0:
            accion_str = f"d{accion}"
        elif accion < 0:
            accion_str = f"r{-accion - 1}"
        elif accion == -1:
            accion_str = "acept"
        else:
            accion_str = "error"

        print(f"{pila_formateada:20} {entrada_restante:20} {accion_str}")

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
            pila.push(E)
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
