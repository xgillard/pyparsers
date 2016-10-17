'''
This module contains a rather simple example on how to develop a simple
calculator DSL using pyparsers.

Author: X. Gillard
'''

from pyparsers import *

#===============================================================================
# Gives a simple example of how to implement a calculator.
# Note: Reliance on regexes is maybe the most cryptic bit. Is that an issue ?
#===============================================================================
class Calculator:

    def tokenizer(self):
        tok = Tokenizer()
        tok.puctuation(r"\+", r"-", r"\*", r"/", r"\^", r"%", r"\(", r"\)")
        return tok

    def number(self, tokens, position=0):
        expr = regex(r"-?\s*\d+"      , int)  \
            |  regex(r'-?\s*\d+\.\d+' , float)
        return expr(tokens, position)

    def power(self, tokens, position=0):
        number = parser(self.number)
        power  = parser(self.power)
        expr   = sequence(number, "^", power, action=lambda a, b, c: a**c) \
               | number
        return expr(tokens, position)

    def multiplication(self, tokens, position=0):
        power = parser(self.power)
        arith = parser(self.arith)
        multi = parser(self.multiplication)

        atom  = power \
              | sequence("(", arith, ")", action=lambda a, b, c: b)

        expr  = sequence(atom, "*", multi, action=lambda a, b, c: a*c) \
              | sequence(atom, "/", multi, action=lambda a, b, c: a/c) \
              | sequence(atom, "%", multi, action=lambda a, b, c: a%c) \
              | atom
        return expr(tokens, position)

    def term(self, tokens, position=0):
        factor = parser(self.multiplication)
        term   = parser(self.term)
        expr   = sequence(factor, "+", term, action=lambda a, b, c: a+c) \
               | sequence(factor, "-", term, action=lambda a, b, c: a-c) \
               | factor
        return expr(tokens, position)

    def arith(self, tokens, position=0):
        return self.term(tokens, position)

    def parse(self, text):
        return parse_all(text, self.arith, self.tokenizer())


#===============================================================================
# Easily illustrates how to use the framework
#===============================================================================
expression = "( (2+3)/5 )*2^2 % 3"
parse_res  = Calculator().parse(expression)
print(parse_res)

#===============================================================================
# optional
#===============================================================================
#===============================================================================
blabla = sequence("chi", optional("chat"), action=lambda a,b: (a,b))

print(blabla("chi chat chi chat chi chi chat".split()))
#===============================================================================

#===============================================================================
# repeat
#===============================================================================
#===============================================================================
rpt = repeat(sequence("+", "-", action=lambda x,y: (x,y)), max_occurs=1)

print(rpt("+ - + - + +".split()))
#===============================================================================
