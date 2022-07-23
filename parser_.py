from unittest import result
from tokens import TokenTypes, Token
from nodes import *


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = iter(tokens)
        self.advance()

    def raise_error(self):
        raise Exception("Invalid syntax")

    def advance(self):
        try:
            self.currennt_token: Token = next(self.tokens)
        except StopIteration:
            self.currennt_token = None

    def expr(self):
        result = self.term()

        while self.currennt_token != None and self.currennt_token.type in (TokenTypes.PLUS, TokenTypes.MINUS):
            if self.currennt_token.type == TokenTypes.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.currennt_token.type == TokenTypes.MIUNS:
                self.advance()
                result = SubtractNode(result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.currennt_token != None and self.currennt_token.type in (TokenTypes.MULTIPLY, TokenTypes.DIVIDE):
            if self.currennt_token.type == TokenTypes.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.factor())
            elif self.currennt_token.type == TokenTypes.DIVIDE:
                self.advance()
                result = DivivdeNode(result, self.factor())

        return result

    def factor(self):
        token = self.currennt_token

        if token.type == TokenTypes.LPAREN:
            self.advance()
            result = self.expr()
            if self.currennt_token.type != TokenTypes.RPAREN:
                self.raise_error()
            self.advance()
            return result

        elif token.type == TokenTypes.NUMBER:
            self.advance()
            return NumberNode(token.value)
        elif token.type == TokenTypes.PLUS:
            self.advance()
            return PlusNode(self.factor())
        elif token.type == TokenTypes.MINUS:
            self.advance()
            return MinusNode(self.factor())

        self.raise_error()

    def parse(self):
        if self.currennt_token == None:
            return None

        result = self.expr()

        if self.currennt_token != None:
            self.raise_error()

        return result
