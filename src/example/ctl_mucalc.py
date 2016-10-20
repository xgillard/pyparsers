# -*- encoding: utf-8 -*-
'''
This module contains a rather simple example on how to develop an interpreter
that translates a CTL formula to an equivalent 𝜇-calculus formula.

Author: X. Gillard
'''

from pyparsers import *

#===============================================================================
# The parser itself
#===============================================================================
class CTL:
    """A very simple CTL interpreter"""
    def __init__(self, actions):
        self._act = Actions()
    
    def tokenizer(self):
        """The tokenizer: recognizes a few special chars"""
        tok = Tokenizer()
        tok.punctuation(r"!", r"&", r"\|", r"\(", r"\)", r"\[", r"\]")
        return tok
    
    def atomic_prop(self, tokens, position=0):
        """A parser that recognises a simple atomic proposition identifier"""
        ident = regex("[a-z]+")
        return ident(tokens, position)
    
    def state_formula(self, tokens, position=0):
        """Parses a CTL formula and produces the equivalent mu calculus expression"""
        phi    = parser(self.state_formula)
        atomic = parser(self.atomic_prop)                                           \
               | sequence("(", phi, ")",                action=self._act.surround)
               
        state  = sequence("!", phi,                     action=self._act.negation)  \
               | sequence(atomic, "|", phi,             action=self._act._or)       \
               | sequence(atomic, "&", phi,             action=self._act._and)      \
               | sequence("EX", phi,                    action=self._act.ex)        \
               | sequence("EG", phi,                    action=self._act.eg)        \
               | sequence("E", "[", phi, "U", phi, "]", action=self._act.eu)        \
               | sequence("AX", phi,                    action=self._act.ax)        \
               | sequence("AG", phi,                    action=self._act.ag)        \
               | sequence("A", "[", phi, "U", phi, "]", action=self._act.au)        \
               | atomic
               
        return state(tokens, position)
    
    def interpret(self, text):
        return parse_all(text, self.state_formula, self.tokenizer())


#==============================================================================
# The interpretation of the formulas
#==============================================================================
class Actions:
    """A set of action that produce the mu calculus encoding of a CTL formula"""
    
    def __init__(self):
        self.bound_var = self._gen_bound_var()
    
    def _gen_bound_var(self):
        """A Generator that produces an infinite sequene of fresh bound variables"""
        while True:
            j =  0
            for i in range(ord("Z"), ord("A")-1, -1):
                yield chr(i) + str(j) if j > 0 else chr(i)
            j += 1
            
    def surround(self, _left, f, _right): 
        return "({})".format(f)
    
    def negation(self, _not, f):
        "!{}".format(f)
    
    def _or(self, phi, __or, psi):
        return "{} | {}".format(phi, psi)
    
    def _and(self, phi, __and, psi):
        return "{} & {}".format(phi, psi)
    
    def ex(self, _ex, phi):
        return "<a> {}".format(phi)
    
    def eg(self, _eg, phi):
        return "( 𝜈 {0} . {1} & <a> {0} )".format(next(self.bound_var), phi)
    
    def eu(self, _e, _left, phi, _U, psi, _right):
        return "( 𝜇 {0} . {2} | ({1} & <a> {0}) )".format(next(self.bound_var), phi, psi)
    
    def ax(self, _ax, phi):
        return "[a] {}".format(phi)
    
    def ag(self, _eg, phi):
        return "( 𝜈 {0} . {1} & [a] {0} )".format(next(self.bound_var), phi)
    
    def au(self, _e, _left, phi, _U, psi, _right):
        return "( 𝜇 {0} . {2} | ({1} & [a] {0}) )".format(next(self.bound_var), phi, psi)

   
#===============================================================================
# A factory that creates the appropriate interpreter
#===============================================================================
def ctl(fairness=None):
    # TODO : Implement the same interpretation as above but using a fairness assumption
    return CTL(Actions())   
   
#===============================================================================
# The program entry point.
#===============================================================================
if __name__ == "__main__":
    formula = "E[ f U g ]"
    print("{} === {} ".format( formula, ctl().interpret(formula) ))