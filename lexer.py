import re
from token import Token

TIPOS = {
    "identificador": 0,
    "entero": 1,
    "real": 2,
    "cadena": 3,
    "tipo": 4,
    "opSuma": 5,
    "opMul": 6,
    "opRelac": 7,
    "opOr": 8,
    "opAnd": 9,
    "opNot": 10,
    "opIgualdad": 11,
    ";": 12,
    ",": 13,
    "(": 14,
    ")": 15,
    "{": 16,
    "}": 17,
    "=": 18,
    "if": 19,
    "while": 20,
    "return": 21,
    "else": 22,
    "$": 23
}

RESERVADAS = {
    "if": TIPOS["if"],
    "while": TIPOS["while"],
    "return": TIPOS["return"],
    "else": TIPOS["else"],
    "int": TIPOS["tipo"],
    "float": TIPOS["tipo"],
    "void": TIPOS["tipo"]
}

class Lexer:
    def __init__(self, texto):
        self.texto = texto

    def manejar_error(self, lex):
        """Maneja errores léxicos y genera un mensaje claro."""
        raise Exception(f"❌ Error léxico: símbolo inválido '{lex}'")

    def analizar(self):
        tokens = []
        patron = re.compile(
            r"\d+\.\d+|"
            r"\d+|"
            r"&&|\|\||==|!=|<=|>=|"
            r"[+\-*/<>(){};,=]|"
            r"[a-zA-Z][a-zA-Z0-9]*|"
            r"\s+|"
            r"."
        )

        for m in patron.finditer(self.texto):
            lex = m.group()

            if lex.isspace():
                continue

            if re.fullmatch(r"\d+\.\d+", lex):
                tokens.append(Token(lex, TIPOS["real"]))
            elif lex.isdigit():
                tokens.append(Token(lex, TIPOS["entero"]))
            elif lex in RESERVADAS:
                tokens.append(Token(lex, RESERVADAS[lex]))
            elif re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", lex):
                tokens.append(Token(lex, TIPOS["identificador"]))
            elif lex in ["+", "-"]:
                tokens.append(Token(lex, TIPOS["opSuma"]))
            elif lex in ["*", "/"]:
                tokens.append(Token(lex, TIPOS["opMul"]))
            elif lex in ["<", "<=", ">", ">="]:
                tokens.append(Token(lex, TIPOS["opRelac"]))
            elif lex in ["==", "!="]:
                tokens.append(Token(lex, TIPOS["opIgualdad"]))
            elif lex == "&&":
                tokens.append(Token(lex, TIPOS["opAnd"]))
            elif lex == "||":
                tokens.append(Token(lex, TIPOS["opOr"]))
            elif lex == "!":
                tokens.append(Token(lex, TIPOS["opNot"]))
            elif lex in [";", ",", "(", ")", "{", "}", "="]:
                tokens.append(Token(lex, TIPOS[lex]))
            else:
                self.manejar_error(lex)

        tokens.append(Token("$", TIPOS["$"]))
        return tokens
