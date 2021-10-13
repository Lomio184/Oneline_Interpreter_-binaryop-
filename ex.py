# ----- Start Code ----- #
from enum import Enum
import sys

class TokenType(Enum):
    INTEGER_TYPE    = 0
    SYMBOL_TYPE     = 1
    UNARY_TYPE      = 2
    OP_TYPE         = 3
    PLUS_TYPE       = '+'
    MINUS_TYPE      = '-'
    MUL_TYPE        = '*'
    DIV_TYPE        = '/'

class Token:
    def __init__(self, token, line, col, tokentype):
        self.token = token
        self.line = line
        self.col  = col
        self.tokentype = tokentype


def main():
    line = 0
    while True: 
        input_text = input(">> ")

if __name__ == "__main__":
    main()