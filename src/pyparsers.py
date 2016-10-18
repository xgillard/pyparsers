'''
This module contains the core of the pyparsers micro framework to develop DSLs
with python (this is actually the only file you'll need to get started:its truly micro).

The objective of the framework is fairly simple: let you develop a parser/interpreter
for the grammar of your choice the way *YOU* think *YOU* would express the grammar.
Therefore, it also strives to be minimalist and provide a few powerful abstractions
to let you get started without having to go through the burden of learning yet
an other parsers engine.

Note::
    Conceptually, this library was inspired by the Scala parsers library.

Author: X. Gillard
'''
import re
from builtins import str

#===============================================================================
# Tokenization
#===============================================================================
class Tokenizer:
    """
    A configurable tokenizer that lets you decide what should be considered whitespace
    (whitespaces are dropped) and what should be considered punctuation (kept).
    """
    def __init__(self):
        self._whitespace = "\s"
        self._punctuation= []

    def whitespace(self, expr):
        """What is considered blank text"""
        self._whitespace = expr

    def puctuation(self, *ops):
        """The 'punctuation' of the language (may connect two other tokens)"""
        self._punctuation = "|".join(ops)

    def tokenize(self, text):
        """
        Tokenizes the given text to a stream (list) of tokens where punctuation is taken into account
        """
        # split and drop whitspaces
        tokens = re.split(self._whitespace, text)
        # separate punctuation from the rest
        tokens = [ self._partition(self._punctuation, token) for token in tokens ]
        # flatten
        tokens = [ x for a in tokens for x in a ]
        return tokens

    def _partition(self, punct, text):
        """
        Partitions a given string in a disjoint set of substrings where some substrings match the given
        punctuation pattern (`punct`) and the rest doesn't
        """
        rest   = text
        result = []

        while rest:
            match = re.search(punct, rest)
            if match:
                # if there was something before, add it
                if match.start() != 0:
                    result.append( rest[0: match.start()] )

                # add the match that was found
                result.append( rest[match.start():match.end()] )
                # consider only what's left
                rest    = rest[match.end():]
            else:
                # add the remainder to the result
                result.append( rest )
                rest    = None

        return result


#===============================================================================
# Parsing
#===============================================================================
class ParseResult:
    """
    This is the abstract class that describes the kind of objects to be returned by the parser apis.
    """
    def __init__(self, pos):
        """
        Creates a new instance remembering the position (:param pos:) in the stream of tokens up to
        which the stream has been correctly parsed.
        """
        self._pos = pos

    def position(self):
        """:return: the position in the stream of tokens up to which this result accounts for."""
        return self._pos

    def success(self):
        """:return: True iff this result represent a successful parse"""
        pass

    def value(self):
        """:return: the value (ast node) parsed."""
        pass

    def reason(self):
        """:return: the reason explaining why this parse has failed"""
        pass

    def transform(self, action):
        """
        :return: an other parse result equivalent to this one but where `action` has been applied to the value

        Note:: This has an effect only in the case where the result is success
        """
        pass


class Success(ParseResult):
    """A parse result encapsulating the case where a subsequence of tokens has correctly been parsed"""
    def __init__(self, pos, value):
        super().__init__(pos)
        self._val = value

    def success(self):
        return True

    def value(self):
        return self._val

    def reason(self):
        return None

    def transform(self, action):
        return Success(self.position(), action(self.value()) )

    def __str__(self):
        return "Success({}, {})".format(self.position(), self.value())


class Failure(ParseResult):
    """A parse result encapsulating the case where the stream of token couldn't be parsed"""
    def __init__(self, pos, reason):
        super().__init__(pos)
        self._reason = reason

    def reason(self):
        return self._reason

    def success(self):
        return False

    def value(self):
        return None

    def transform(self, action):
        return self

    def __str__(self):
        return "Failure({}, {})".format(self.position(), self.reason())


#===============================================================================
# Utility actions
#===============================================================================
def identity(x):
    """A function that does nothing (the default parse action)"""
    return x

#===============================================================================
# The real parser thing !
#===============================================================================
class Parser:
    """
    An actual parser object that can be combined with some other parser to build more advanced
    grammars
    """
    def __init__(self, fn):
        """Creates a new object and remembers the function being decorated"""
        self._fn     = fn if not isinstance(fn, str) else text(fn)

    def __call__(self, tokens, position=0):
        """Executes the underlying function"""
        if position >= len(tokens):
            return Failure(position, "Reached end of token stream")
        return self._fn(tokens, position)

    def then(self, other, action=identity):
        """
        Combines this parser with an other one to return a new parser that recognizes this content followed
        by the content recognized by the other parser
        """
        other = other if isinstance(other, Parser) else Parser(other)
        return sequence(self._fn, other, action)

    def alt(self, other, action=identity):
        """
        Combines this parser with an other one to return a new parser that recognizes either this content
        or the one from the other
        """
        other = other if isinstance(other, Parser) else Parser(other)

        def choice(tokens, position=0):
            """Internal function to recognize either one or the other content"""
            me  = self._fn(tokens, position)
            if me.success():
                return me.transform(action)

            # return the result transformed as necessary
            return other(tokens, position).transform(action)
        # The parser result
        return Parser(choice)

    def __add__(self, other):
        """Allows the sequential combination of parsers in a symbolic fashion"""
        return self.then(other)

    def __or__(self, other):
        """Allows the alternative combination of parsers in a symbolic fashion"""
        return self.alt(other)


#===============================================================================
# Standard parsers (useful stuffs you might have done yourself)
#===============================================================================
def text(text, action=identity):
    """
    Generates a parser that recognizes the given text (and only that)
    :param text: the text being recognized
    :param action: the action applied to the parsed token
    """
    def do_parse(tokens, position=0):
        if tokens[position] == text :
            return Success(position + 1, text)
        else:
            return Failure(position, "Expected {} instead of {}".format(text, tokens[position]))
    return Parser(do_parse)

def one_of(enumerated, action=identity):
    """
    Generates a parser that recognizes one of the specified given values
    :param enumerated: the list of the values recognized by this parser.
    :param action: the action applied to the parsed token
    """
    def do_parse(tokens, position=0):
        if tokens[position] in enumerated:
            return Success(position+1, action(tokens[position]))
        else:
            return Failure(position, "Expecting one of the following tokens "+str(enumerated))
    return Parser(do_parse)

def regex(pattern, action=identity):
    """
    Generates a parser that recognizes the given regex.
    :param pattern: pattern recognized by this parser.
    :param action: the action applied to the parsed result
    """
    def do_parse(tokens, position=0):
        results = re.match("^"+pattern+"$", tokens[position])
        return Success(1+position, action(tokens[position])) if results else Failure(position, "Expecting a token matching "+pattern)
    return Parser(do_parse)

def sequence(*parsers, action=lambda *x: x):
    """
    Generates a composite parser for a sequence of tokens.

    :param parsers: a sequence of parsers that must be recognized
    :param action: an action to be applied to the sequence of outputs recognized by the parsers.
           (note: one param per recognized value)
    :return: a parse result containing action( *( *parsers.value() ) ).
           (In case the result is a failure, action is obviously not applied)
    """
    def do_parse(tokens, position=0):
        output = []
        for p in parsers:
            # try to parse
            current= parser(p) if not isinstance(p, Parser) else p
            result = current(tokens, position)
            # if its a failure, stop parsing
            if not result.success():
                return result
            # else update the result and the current position.
            output.append(result.value())
            position = result.position()

        return Success(position, action(*output))

    return Parser(do_parse)

def repeat(repeated, min_occurs=0, max_occurs=float("inf"), action=identity):
    """
    Generates a parser for a rule that can be repeated.

    :param repeated: the rule that can happen many times
    :param action: the function that receives the *list* of inputs as param and treats them all.
    :return: a parse result containing the processed output of the many results of `repeated`
    """
    repeated = parser(repeated) if not isinstance(repeated, Parser) else repeated

    def do_parse(tokens, position=0):
        results = []
        current = repeated(tokens, position)
        while current.success():
            position = current.position()
            results.append(current.value())

            current = repeated(tokens, position)

        res_len = len(results)
        if res_len < min_occurs :
            return Failure(position, "{} occurred only {} times (minimum: {})"\
                                                    .format(repeated, res_len, min_occurs))
        elif res_len > max_occurs:
            return Failure(position, "{} occurred {} times (maximum: {})"\
                                                    .format(repeated, res_len, max_occurs))
        else:
            return Success(position, action(results))

    return Parser(do_parse)

def optional(rule, action=identity):
    """
    Generates a parser that possibly recognizes an optional string

    :param rule: the rule to be possibly matched
    :param action: the action to be applied on the result
    :return: a parser that recognises `rule` 0 or one time.
    """
    rule = parser(rule) if not isinstance(rule, Parser) else rule
    def do_parse(tokens, position=0):
        result = rule(tokens, position)
        if result.success():
            return result.transform(action)
        else:
            return Success(position, action(None))

    return do_parse


#===============================================================================
#
#===============================================================================
def parser(fn):
    """Wraps a function to make it a parser (useful to implement recursive call)"""
    return Parser(fn)

def parse_all(text, axiom, tokenizer=Tokenizer()):
    """
    Utility function to parse *all* the text of the given input text
    :param text: the text to be parsed
    :param axiom: the axiom (base rule of the derivation) that generates the root of the ast
    :param tokenizer: an optional tokenizer customized to your needs
    :return: the value corresponding to a successful parse of the text
    :raises: an exception if not all text could be parsed
    """
    tokens       = tokenizer.tokenize(text)
    parse_result = axiom(tokens)
    # Check possible failures
    if not parse_result.success():
        raise SyntaxError("At {} : {}".format(parse_result.position(), parse_result.reason()))
    if not parse_result.position() == len(tokens):
        raise SyntaxError("At {} : Invalid suffix".format(parse_result.position()))
    # Ok we're good, return the result
    return parse_result.value()
