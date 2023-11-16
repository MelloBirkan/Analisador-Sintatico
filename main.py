class Parser:

  def __init__(self, input):
    # Inicializa o parser com a expressão de entrada, removendo espaços
    self.input = input.replace(" ", "")
    # Define o índice inicial para a leitura dos caracteres da expressão
    self.index = 0

  def parse(self):
    # Inicia a análise sintática pela regra inicial e verifica se todos os tokens foram consumidos
    return self.I() and self.index == len(self.input)

  def I(self):
    # Implementa a regra I -> S
    return self.S()

  def S(self):
    # Implementa a regra S -> TK
    start_index = self.index
    if self.T() and self.K():
      return True
    self.index = start_index
    return False
      

  def K(self):
      # Implementa as regras K -> +TK | ε
    while self.expect('+') or self.expect('-'):
      start_index = self.index
      if self.T() and self.K():
        return True
      self.index = start_index
      break
    return True

  def Z(self):
    # Implementa a regra Z -> *FZ, Z -> /FZ, Z -> ε
    while self.expect('*') or self.expect('/'):
        start_index = self.index
        if self.F() and self.Z():
            return True
        self.index = start_index
        break
    return True

  def T(self):
      # Implementa a regra T -> FZ
        start_index = self.index
        if self.F() and self.Z():
            return True
        self.index = start_index
        return False

  def F(self):
     # Implementa a regra F -> (S), F -> N, F -> -N
      start_index = self.index
      if self.expect('(') and self.S() and self.expect(')'):
          return True
      self.index = start_index
      if self.N():
          return True
      self.index = start_index
      if self.expect('-') and self.N():
          return True
      self.index = start_index
      return False

  def N(self):
      # Implementa a regra N -> 1D 2D 3D 4D ... 9D
      start_index = self.index
      if self.is_digit():
          while self.is_digit():
              self.index += 1
          if self.D():
              return True
          self.index = start_index
      return False

  def D(self):
      # Implementa a regra D -> 0D 1D 2D 3D ... 9D | ε
    while self.is_digit():
        self.index += 1
    return True

  def expect(self, token):
      # Verifica se o caracter o qual está sendo lido é o "esperado"
    if self.index < len(self.input) and self.input[self.index] == token:
        self.index += 1
        return True
    return False

  def is_digit(self):
    # Verifica se o caracter sendo lido é um digito
      return self.index < len(self.input) and self.input[self.index].isdigit()

# Conjunto de expressoes validas:
valid_expressions = [
    "1 + 2", "(3 + 4) * 5", "6 / (7 - 8)", "9 * 10 - 11", "(12 + 13) / 14",
    "15 - (16 * 17)", "18 + (19 / 20)", "(21 - 22) * 23", "24 / (25 + 26)",
    "27 * 28 - 29", "(30 / 31) + 32", "33 - (34 / 35)", "(36 + 37) * 38",
    "39 / 40 - 41", "42 * (43 + 44)", "(45 - 46) / 47", "48 + 49 * 50",
    "51 - 52 / 53", "(54 * 55) + 56", "57 / (58 - 59)"
]

# Conjunto de expressoes invalidas:
invalid_expressions = [
    "+ 1 - 2", "3 * / 4", "(5 + 6", "7 -) 8 * 9", "* 10 + 11",
    "12 / *", "13 (14 + 15)", "16 +)", "17 - * 18", "19 / (/ 20)",
    "(21 + 22", "23 (24 * 25", "26 / 27)", "- / 28 + 29", "30 + * 31",
    "(32 - 33", "34) * 35", "/ 36 / + - 37", "38 - 39) /", "40 * (41 +"
]

# Testa se uma expressao e valida ou invalida
def test_expressions(expressions, is_valid):
    n = 0
    for expr in expressions:
        parser = Parser(expr)
        result = parser.parse()
        validity = "Válida" if result else "Inválida"
        n += 1
        print(f"Expressão {n}: '{expr}': {validity}")
        

print("Testando expressões válidas: ")
test_expressions(valid_expressions, True)

print("\nTestando expressões inválidas:")
test_expressions(invalid_expressions, False)