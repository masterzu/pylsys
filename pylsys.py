#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# 
# a pure python implementation of l-system (Lindenmayer system) for simulate Plants.

# masterzu 
# 
VERSION = 1

# History 
# * 19 juil. 2014 - 1
# - initial version

class D0L:
    """
    D0L-system
    The simple Determinist, context free L-system.

    Works with all string, so with D0L branching rules.

    axiom = string
    rules = dict(character: string)

    >>> D0L('F+F+F',{'F': 'F-F++F-F'})._steps(2)
    | axiom : F+F+F
    | F -> F-F++F-F
    gen 1: F-F++F-F+F-F++F-F+F-F++F-F
    gen 2: F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F+F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F+F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F

    
    >>> D0L('X',{'X': 'F[+X]F[-X]', 'F': 'FF'})._steps(3)
    | axiom : X
    | X -> F[+X]F[-X]
    | F -> FF
    gen 1: F[+X]F[-X]
    gen 2: FF[+F[+X]F[-X]]FF[-F[+X]F[-X]]
    gen 3: FFFF[+FF[+F[+X]F[-X]]FF[-F[+X]F[-X]]]FFFF[-FF[+F[+X]F[-X]]FF[-F[+X]F[-X]]]

    """
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules
        self.state = None
        self.generation = 0

    def __repl__(self):
        return 'gen ' + str(self.generation) + ': ' + str(self)

    def __str__(self):
        if self.state is None:
            return '(none)'
        return str(self.state)

    def echo(self):
        print 'gen ' + str(self.generation) + ': ' + self.state

    def step(self, verbose=False):
        """
        calculate a step of L-system
        """
        if self.state is None:
            self.state = self.axiom

        s = ""
        for c in self.state:
            if c in self.rules.keys():
                s = s + self.rules[c]
            else:
                s = s + c
        self.state = s
        self.generation = self.generation + 1
        if verbose:
            self.echo()

    def _steps(self, n):
        print '| axiom : %s' % self.axiom
        for r in self.rules.keys():
            print "| %s -> %s" % (r, self.rules[r])
        for _ in xrange(n):
            self.step(True)
        print


if __name__ == '__main__':
    D0L('F+F+F',{'F': 'F-F++F-F'})._steps(2)
    D0L('X',{'X': 'F[+X]F[-X]', 'F': 'FF'})._steps(3)


        
        





