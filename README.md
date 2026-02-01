# Analizador Sintáctico LR

Este proyecto implementa un analizador sintáctico LR para procesar cadenas basadas en una gramática específica. El analizador utiliza una tabla LR y reglas de producción para realizar desplazamientos y reducciones, validando si una cadena pertenece al lenguaje definido por la gramática.

## Características
- **Gramática soportada:**
  - `E -> id + E`
  - `E -> id`
- **Funciones principales:**
  - Análisis léxico para identificar tokens (`id`, `+`, `$`).
  - Análisis sintáctico utilizando una tabla LR y reglas de producción.
  - Validación de cadenas de entrada.

## Requisitos
- Python 3.10 o superior.

## Uso
1. Ejecuta el script principal:
   ```bash
   python anasinta.py
   ```
2. Introduce una cadena para analizar, como `a+b+c` o `hola+mundo`.
3. Observa la salida, que incluye los pasos del análisis sintáctico.

## Estructura del proyecto
- `anasinta.py`: Contiene la implementación del analizador léxico y sintáctico.
- `Practica Analizador Sintactico LR.pdf`: Documento con la gramática y detalles del proyecto.

## Ejemplo de salida
```
Ingresa la cadena (ej: hola+mundo): hola+mundo
PILA                          ENTRADA              ACCIÓN
-----------------------------------------------------------------
$0                            hola+mundo$          d2
$0hola2                       +mundo$              d3
$0hola2+3                     mundo$               d2
$0hola2+3mundo2               $                    r1
$0hola2+3E4                   $                    acept
```

## Notas
- Asegúrate de que la tabla LR y las reglas de producción sean consistentes con la gramática definida.
- Si encuentras errores, verifica la gramática y las acciones en la tabla LR.

## Autor
- **Nombre:** [Tu Nombre]
- **Contacto:** [Tu Correo Electrónico]