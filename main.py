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

def tokenize(text, line):
    if len(text) == 0:
        sys.stdout.write("Empty File!\n")
        return
    pos = 0;tokenset = []

    while True:
        if pos == len(text):
            break

        if text[pos].isdigit():
            current_token = ''
            while pos < len(text) and text[pos].isdigit():
                current_token += text[pos]
                pos += 1
            token = Token(current_token, line, pos, TokenType.INTEGER_TYPE)
            tokenset.append(token)

        elif text[pos] == '+':
            token = Token(text[pos], line, pos, TokenType.PLUS_TYPE)
            tokenset.append(token)
            pos += 1

        elif text[pos] == '-':
            token = Token(text[pos], line, pos, TokenType.MINUS_TYPE)
            tokenset.append(token)
            pos += 1

        elif text[pos] == '*':
            token = Token(text[pos], line, pos, TokenType.MUL_TYPE)
            tokenset.append(token)
            pos += 1

        elif text[pos] == '/':
            token = Token(text[pos], line, pos, TokenType.DIV_TYPE)
            tokenset.append(token)
            pos += 1

        elif text[pos].isspace():
            pos += 1

    return tokenset

class AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Unary:
    def __init__(self, op, node):
        self.op = op
        self.node = node

class Number:
    def __init__(self, token):
        self.token = token
        self.value = token.token

class Parser:
    def __init__(self, lex):
        self.lex = lex
        self.parser_pos = 0
        self.current_token = self.lex[self.parser_pos]

    def eat(self):
        self.parser_pos += 1
        if self.parser_pos > len(self.lex) - 1:
            self.current_token = None
            return
        self.current_token = self.lex[self.parser_pos]
    
    def parser_factor(self):
        token = self.current_token
        if token.tokentype == TokenType.PLUS_TYPE:
            self.eat()
            node = Unary(token, self.parser_factor())
            return node
        elif token.tokentype == TokenType.MINUS_TYPE:
            self.eat()
            node = Unary(token, self.parser_factor())
            return node
        elif token.tokentype == TokenType.INTEGER_TYPE:
            self.eat()
            return Number(token)
    
    def parser_term(self):
        node = self.parser_factor()
        while self.current_token is not None and \
            self.current_token.tokentype in (TokenType.MUL_TYPE, TokenType.DIV_TYPE):
            token = self.current_token
            self.eat()
            node = AST(left=node, op=token, right=self.parser_factor())
        return node
    
    def parser_expr(self):
        node = self.parser_term()
        while self.current_token is not None and \
            self.current_token.tokentype in (TokenType.PLUS_TYPE, TokenType.MINUS_TYPE):
            token = self.current_token
            self.eat()
            node = AST(left=node, op=token, right=self.parser_term())
        return node

    def parse(self):
        return self.parser_expr()

class Interpreter:
    def __init__(self, parser) -> None:
        self.parser = parser
    
    def visit(self, node):
        if node.__class__.__name__ == Unary.__name__:
            return self.visit_Unary(node)
        elif node.__class__.__name__ == AST.__name__:
            return self.visit_AST(node)
        elif node.__class__.__name__ == Number.__name__:
            return self.visit_Number(node)
        
    def visit_Unary(self, node):
        op = node.op.tokentype
        if op == TokenType.PLUS_TYPE:
            return self.visit(node.node)
        elif op == TokenType.MINUS_TYPE:
            return -(self.visit(node.node))

    def visit_AST(self, node):
        if node.op.tokentype == TokenType.PLUS_TYPE:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.tokentype == TokenType.MINUS_TYPE:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.tokentype == TokenType.MUL_TYPE:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.tokentype == TokenType.DIV_TYPE:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
        return int(node.value)
    
    def inter(self):
        ast = self.parser.parse()
        return self.visit(ast)

def main():
    line = 0
    while True: 
        input_text = input(">> ")
        if input_text == 'quit':
            break
        tokenset = tokenize(input_text, line)
        parser = Parser(tokenset)
        inter = Interpreter(parser)
        val = inter.inter()
        print(">>", val)
        line += 1

if __name__ == "__main__":
    main()