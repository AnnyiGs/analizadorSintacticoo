import sys

# --- CONSTANTES ---
# id=0, +=1, $=2, E=3
COL_ID = 0
COL_MAS = 1
COL_PESOS = 2
COL_E = 3

# Mapeo solo para No Terminales o símbolos especiales numéricos
NOMBRES_SIMBOLOS = {3: "E", 2: "$"}

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

        if c.isalpha(): 
            self.simbolo = c  # Guardamos 'a', 'b', etc.
            self.tipo = COL_ID
            self.indice += 1
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
    for item in pila:
        # Si es un número (Estado o ID de No Terminal)
        if isinstance(item, int):
            # Si está en el mapa (ej. 3 -> E), lo usamos. Si no, es un estado (0, 1, 2...)
            salida += NOMBRES_SIMBOLOS.get(item, str(item))
        else:
            # Si es string (ej. "a", "+", "$"), lo ponemos directo
            salida += item
    return salida

def analizar_cadena_usuario():
    # --- CONFIGURACIÓN EJERCICIO 2 ---
    # Filas: 0-4, Cols: id, +, $, E
    tabla_lr = [
        [2,  0,  0,  1],  # 0
        [0,  0, -1,  0],  # 1
        [0,  3, -3,  0],  # 2 
        [2,  0,  0,  4],  # 3
        [0,  0, -2,  0]   # 4 
    ]
    
    id_reglas = [COL_E, COL_E] # Reglas producen E
    lon_reglas = [3, 1]        # Longitudes

    # --- INICIO ---
    # Ejemplo sugerido: a+b+c+d+e+f
    input_str = input("Ingresa la cadena (ej: a+b+c): ")
    
    # Encabezados alineados
    print(f"\n{'PILA':<30} {'ENTRADA':<20} {'ACCIÓN'}")
    print("-" * 65)

    # Inicializamos pila con el símbolo "$" textual y estado 0
    pila = ["$", 0] 
    
    lexico = Lexico(input_str)
    lexico.sig_simbolo()
    
    while True:
        estado_actual = pila[-1] # El tope siempre es un estado (int)
        columna = lexico.tipo
        
        if estado_actual >= len(tabla_lr):
            print("Error: Estado inválido")
            break

        accion = tabla_lr[estado_actual][columna]
        
        # --- IMPRESIÓN ---
        pila_str = formatear_pila(pila)
        entrada_str = lexico.obtener_resto_entrada()
        
        accion_str = ""
        if accion > 0: accion_str = f"d{accion}"
        elif accion == -1: accion_str = "acept"
        elif accion < -1: accion_str = f"r{abs(accion)-2}"
        else: accion_str = "Error"

        print(f"{pila_str:<30} {entrada_str:<20} {accion_str}")
        # -----------------

        if accion > 0: # Desplazamiento
            # CAMBIO CLAVE: Metemos el símbolo real ("a", "+") en vez del tipo (0, 1)
            pila.append(lexico.simbolo) 
            pila.append(accion)
            lexico.sig_simbolo()

        elif accion < 0: # Reducción
            if accion == -1:
                break
            else:
                idx_regla = abs(accion) - 2
                longitud = lon_reglas[idx_regla]
                id_lhs = id_reglas[idx_regla] # Esto es 3 (E)
                
                # Sacar 2 elementos por cada longitud
                for _ in range(longitud * 2):
                    if pila: pila.pop()
                
                estado_tope = pila[-1]
                goto = tabla_lr[estado_tope][id_lhs]
                
                # Metemos el ID del No Terminal (3) y el nuevo estado
                # El formateador convertirá 3 -> "E"
                pila.append(id_lhs)
                pila.append(goto)

        else:
            print("Error de sintaxis")
            break

if __name__ == "__main__":
    analizar_cadena_usuario()