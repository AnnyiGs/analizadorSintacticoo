from lexer import Lexer

print("\nIngresa tu código (línea vacía para terminar):")
lineas = []
while True:
    linea = input()
    if linea == "":
        break
    lineas.append(linea)

codigo = "\n".join(lineas)

lexer = Lexer(codigo)
try:
    tokens = lexer.analizar()

    print("\nTOKENS GENERADOS:")
    for t in tokens:
        print(f"(lexema: {t.lexema}, tipo: {t.tipo})")
except Exception as e:
    print(f"\n❌ Error: {e}")  # Capturar y mostrar errores de manera clara
