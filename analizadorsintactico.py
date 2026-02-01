# ----------------------------
# Tipos de símbolos
# ----------------------------
ID = 0
MAS = 1
PESOS = 2
E = 3


# ----------------------------
# Analizador Léxico simple
# ----------------------------
class Lexico:
    def __init__(self, cadena):
        self.cadena = cadena + "$"
        self.pos = 0
        self.simbolo = None
        self.tipo = None

    def sig_simbolo(self):
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
        return " ".join(map(str, self.datos))


# ----------------------------
# PARSER LR GENÉRICO
# ----------------------------
def parser_lr(cadena, tablaLR, idReglas, lonReglas):
    pila = Pila()
    pila.push(PESOS)
    pila.push(0)

    lexico = Lexico(cadena)
    lexico.sig_simbolo()

    print(f"{'Pila':25} {'Entrada':20} Acción")
    print("-"*55)

    while True:
        estado = pila.top()
        simbolo = lexico.tipo
        accion = tablaLR[estado][simbolo]

        print(f"{pila.muestra():25} {cadena[lexico.pos-1:]:20} {accion}")

        if accion > 0:  # desplazamiento
            pila.push(simbolo)
            pila.push(accion)
            lexico.sig_simbolo()

        elif accion < 0:  # reducción
            regla = -accion - 1
            k = lonReglas[regla]
            for _ in range(2 * k):
                pila.pop()

            estado = pila.top()
            A = idReglas[regla]
            pila.push(A)
            pila.push(tablaLR[estado][A])

        else:
            print("❌ Error sintáctico")
            break

        if accion == -1:
            print("✅ Aceptación")
            break
