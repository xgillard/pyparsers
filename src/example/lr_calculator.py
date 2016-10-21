'''
This module contains a rather simple example on how to develop a simple
calculator DSL using pyparsers. In particular it illustrates how one can
use the left recursion support to define a grammar that feel *really natural* 

Note:: 
    Although I use @memoize and @leftrec heavily in this class, you are definitely
    not forced to use these decorators everywhere (as an example, the `expression`
    method is left undecorated in the body of `LRCalculator`). 
    
    If all you really want to do is to give your parsing a performance boost, just 
    use @memoize on the method that gets called too often. Similaryly, you only need
    to decorate a function with @leftrec when that function defines left recursive
    rule (CAVEAT: this means direct or indirect left recursion).
    
Note::
    Although this is not strictly mandatory, I do believe it is a good idea to 
    encapsulate your grammar (hence parser) in a class. This way, you have an 
    easier access to the other rules and are not bound by the python limits on the
    order in which you declare your parsing functions.
    An example of this is given in the `atom` function that does a forward reference
    on the `expression` function defined further down.

Author: X. Gillard
'''

from pyparsers import *

#===============================================================================
# Gives a simple example of how to implement a left recursive calculator.
# Note: Reliance on regexes is maybe the most cryptic bit. Is that an issue ?
#===============================================================================
class LRCalculator:
    def tokenizer(self):
        tok = Tokenizer()
        tok.punctuation(r"\+", r"-", r"\*", r"/", r"\^", r"%", r"\(", r"\)")
        return tok
    
    @memoize
    def number(self, tokens, position=0): 
        return regex("-?[0-9]+(\.[0-9]+)?", float)(tokens, position)
    
    @memoize
    def atom(self, tokens, position=0):
        expr = sequence("(", self.expression, ")", action=lambda _l,e,_r: e) \
             | parser(self.number)
        return expr(tokens, position)
    
    @leftrec
    def product(self, tokens, position=0):
        mul_ = parser(self.product)
        expr = sequence(mul_, "*", mul_, action=lambda x,_,y: x*y) \
             | sequence(mul_, "/", mul_, action=lambda x,_,y: x/y) \
             | parser(self.atom)
        return expr(tokens, position)
    
    @leftrec
    def addition(self, tokens, position=0):
        add_ = parser(self.addition)
        expr = sequence(add_ , "+", add_, action=lambda x,_,y: x+y) \
             | sequence(add_ , "-", add_, action=lambda x,_,y: x-y) \
             | parser(self.product)
        return expr(tokens, position)
    
    def expression(self, tokens, position=0):
        return self.addition(tokens, position)
    
    def parse(self, text):
        return parse_all(text, parser(self.addition), self.tokenizer())


#===============================================================================
# Easily illustrates how to use the framework
#===============================================================================
expression = "( (2+3)/5 ) * 2"
parse_res  = LRCalculator().parse(expression)
print(parse_res)
