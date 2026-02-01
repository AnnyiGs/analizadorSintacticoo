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

        elif accion < 0:  # reduce
            regla = -accion - 1
            k = lonReglas[regla]

            for _ in range(2 * k):
                pila.pop()

            estado = pila.top()
            pila.push("E")
            pila.push(tablaLR[estado][E])

        elif accion == -1:
            print("Aceptación")
            break

        else:
            print("Error sintáctico")
            break


# ----------------------------
# MAIN
# ----------------------------
def main():
    cadena = input("Introduce la cadena a analizar: ")

    tablaLR = [
        # id  +   $   E
        [ 2,  0,  0,  1],   # 0
        [ 0,  0, -1,  0],   # 1  ← aquí estaba tu bug
        [ 0,  3, -2,  0],   # 2
        [ 2,  0,  0,  4],   # 3
        [ 0,  0, -1,  0],   # 4
    ]

    # r1: E → id + E
    # r2: E → id
    idReglas = [E, E]
    lonReglas = [3, 1]

    parser_lr(cadena, tablaLR, idReglas, lonReglas)


if __name__ == "__main__":
    main()
