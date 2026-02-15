class Token:
    def __init__(self, lexema, tipo):
        self.lexema = lexema
        self.tipo = tipo

    def __repr__(self):
        return f"<{self.lexema}, {self.tipo}>"
