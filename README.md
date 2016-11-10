# PyParsers
PyParsers is a pure python3 micro framework that aims at letting you easily
design and implement a parser for the DSL **you** have in mind. Concretely, it
pursues the following two objectives:
  - You shouldn't need to _learn_ yet another framework for doing what you want.
  - The code should be _easily understood_, even in a far away future.

**Note: If you ask yourself about the rationale behind the development of pyparsers, just jump to the end of this page.**

## Table of contents
* [Usage](#usage)
  * [Examples](#examples)
  * [API Reference](#api-reference)
* [Installation](#installation)
  * [Using pip](#using-pip)
  * [Manual installation](#manual-installation)
* [How to contribute](#how-to-contribute)
* [The rationale behind pyparsers](#the-rationale-behind-pyparsers)
* [Theoretical background and references](#theoretical-background-and-references)

## Usage
Using pyparsers is fairly simple and should feel familiar if you know how to
express grammars in BNF (And if you don't, just search Bachus-Naur Form on
Wikipedia to get started).

The following examples illustrate several of the possible uses of pyparsers to
let you get a grip on what is feasible and how to achieve it. If you'd rather
get a description of the different functions and the way to use them, just skip
the _Examples_ section and jump straight to the _API Reference_.

### Examples
_**TODO**_

### API Reference
As announced in the introduction, pyparsers makes its best to require no learning
from your side. However, it wouldn't be a library if there was absolutely _no api_
you could learn. A full documentation of the API can be found [here](http://htmlpreview.github.io/?https://github.com/xgillard/pyparsers/blob/devel/doc/build/html/index.html).

_**TODO**_

## Installation
**TODO: The module isn't published to PyPI yet. This needs to be done**
### Using pip
Installing PyParsers couldn't be any easier thanks to `pip`. All it takes you is
to type the following command:

    pip3 install pyparsers

### Manual installation.
If you don't want to use pip to install pyparsers but rather prefer to start from
the sources, and execute the unittests you can proceed as such:

    git clone https://github.com/xgillard/pyparsers.git
    cd pyparsers
    python3 -m unittest
    python3 setup.py install

Or if you just want to include pyparsers within your very own project and ship
it alongside your source code, just download the `pyparsers.py` file and dump it
wherever you like.

## How to contribute
To be honest, I didn't even think of a procedure for other people to contribute
to the project. However, if you would like to contribute to pyparsers and enrich
it with features you feel are missing, I definitely encourage you to do so. Hence,
I suggest you just fork the repo and send me a pull request once you have something
you would like to share. If you really are into it and want to build up a team to
collaborate on this repo, just drop me a line and we'll figure it out.

## The rationale behind pyparsers
I have decided to develop pyparsers as I wasn't happy with  the use of `pyparsing`
which is the de facto standard library to develop DSLs with python. In particular,
I didn't like the fact that it takes you quite a bit of reading and learning
before you get the feeling that you only start to really master what you are
doing with the lib.
More specifically, I didn't like the fact that there exist many different constructs
to achieve seemingly similar goals with only a few subtle differences
(when stating this, I am for instance thinking about `Word` vs `Keyword` vs `Literal`).
Besides that, I had the feeling that the constructs of pyparsing were just not
_natural_ for me. For instance, I would have preferred that library if there was
no distinction between the `|` and `^` operators and `|` simply returned the first
match.
Finally, what really got me into writing pyparsers was the displeasure I had when
facing the pyparsing handles _recursive_ grammars and _infix_ rules. Although some
_might_ like it, I really had the feeling that the API foreseen by the library
for these use cases were just making my code fragile (it is way too easy to create
infinite recursion without even realizing you are doing it) and cluttered on top
of being hard to understand and maintain.

## Theoretical background and references
Reading and understanding the theoretical references related to the development
of parsers and interpreters really **is _not_ obligatory** to be able to use
pyparsers. However, it might be a good idea if you'd like to get a deeper
understanding of the ways it works and the reason why I chose to implement things
the way I did.

Given that the literature related to the development compilers and interpreters
is plain huge, I won't have enough room here to list all relevant papers and/or
books. Therefore, I simply chose to list the ones I found of particular interest.
  - "Programming in Scala 2nd edition", Ordersky, Spoon, Venners -- Artima (2008)
  - "Packrat parsers can support left recursion", Warth, Douglass and Millstein -- PEPM (2008)
  - "Compilers: Principles, Techniques, and Tools", Aho, Lam, Sethi, Ullman -- Addison Wesley (1986)
  - "Introduction to Compiler Construction in a Java World", Campbell, Iyer, Akbal-Deliba -- CRC Press (2012)
