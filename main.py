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
tokens = lexer.analizar()

print("\nTOKENS GENERADOS:")
for t in tokens:
    print(t)
