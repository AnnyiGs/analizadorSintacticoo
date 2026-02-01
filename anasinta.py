import sys

# --- CONSTANTES ---
COL_ID = 0
COL_MAS = 1
COL_PESOS = 2
COL_E = 3

# Mapeo para impresión
NOMBRES_SIMBOLOS = {3: "E"}

class Lexico:
    def __init__(self, entrada):
        self.entrada = entrada
        self.indice = 0
        self.simbolo = ""
        self.tipo = -1

    def sig_simbolo(self):
        if self.indice >= len(self.entrada):
            self.tipo = COL_PESOS
            self.simbolo = "$"
            return

        c = self.entrada[self.indice]

        # --- CAMBIO AQUÍ: LEER PALABRA COMPLETA ---
        if c.isalpha(): 
            start = self.indice
            # Avanzamos mientras sigan siendo letras
            while self.indice < len(self.entrada) and self.entrada[self.indice].isalpha():
                self.indice += 1
            
            self.simbolo = self.entrada[start:self.indice] # Tomamos "hola" completo
            self.tipo = COL_ID
            
        elif c == '+':
            self.simbolo = "+"
            self.tipo = COL_MAS
            self.indice += 1
        elif c.isspace():
            self.indice += 1
            self.sig_simbolo()
        else:
            self.tipo = COL_PESOS
            self.simbolo = "$"
    
    def obtener_resto_entrada(self):
        if self.tipo == COL_PESOS:
            return "$"
        return self.simbolo + self.entrada[self.indice:] + "$"

def formatear_pila(pila):
    salida = ""
    for i, item in enumerate(pila):
        # IMPARES: Son Estados
        if i % 2 != 0:
            salida += str(item)
        # PARES: Son Símbolos
        else:
            if isinstance(item, int):
                salida += NOMBRES_SIMBOLOS.get(item, str(item))
            else:
                salida += item
    return salida

def analizar_cadena_usuario():
    # Tabla Ejercicio 2 (Recursiva)
    tabla_lr = [
        [2,  0,  0,  1],  # 0
        [0,  0, -1,  0],  # 1
        [0,  3, -3,  0],  # 2 
        [2,  0,  0,  4],  # 3
        [0,  0, -2,  0]   # 4 
    ]
    
    id_reglas = [COL_E, COL_E]
    lon_reglas = [3, 1]

    input_str = input("Ingresa la cadena (ej: hola+mundo): ")
    
    print(f"\n{'PILA':<30} {'ENTRADA':<20} {'ACCIÓN'}")
    print("-" * 65)

    pila = ["$", 0] 
    
    lexico = Lexico(input_str)
    lexico.sig_simbolo()
    
    while True:
        estado_actual = pila[-1]
        columna = lexico.tipo
        
        if estado_actual >= len(tabla_lr): break

        accion = tabla_lr[estado_actual][columna]
        
        pila_str = formatear_pila(pila)
        entrada_str = lexico.obtener_resto_entrada()
        
        accion_str = ""
        if accion > 0: accion_str = f"d{accion}"
        elif accion == -1: accion_str = "acept"
        elif accion < -1: accion_str = f"r{abs(accion)-2}"
        else: accion_str = "Error"

        print(f"{pila_str:<30} {entrada_str:<20} {accion_str}")

        if accion > 0: # Desplazamiento
            pila.append(lexico.simbolo) 
            pila.append(accion)
            lexico.sig_simbolo()

        elif accion < 0: # Reducción
            if accion == -1: break
            else:
                idx_regla = abs(accion) - 2
                longitud = lon_reglas[idx_regla]
                id_lhs = id_reglas[idx_regla]
                
                for _ in range(longitud * 2):
                    if pila: pila.pop()
                
                estado_tope = pila[-1]
                goto = tabla_lr[estado_tope][id_lhs]
                
                pila.append(id_lhs)
                pila.append(goto)

        else:
            print("Error de sintaxis")
            break

if __name__ == "__main__":
    analizar_cadena_usuario()