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

    >>> D0L('',{'F': 'F-F++F-F'})._steps(2)
    Traceback (most recent call last):
        ...
    ValueError: axiom must be non empty
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
        if axiom == '':
            raise ValueError, 'axiom must be non empty'
        self.state = axiom
        self.generation = 0
        self.finished = False

    def __repl__(self):
        return 'gen ' + str(self.generation) + ': ' + str(self)

    def __str__(self):
        """
        >>> d = D0L('F', {'F': 'F+F'})
        >>> str(d)
        'F'
        >>> d.step()
        >>> str(d)
        'F+F'
        """
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

        if self.finished:
            return


        s = ""
        os = self.state
        for c in self.state:
            if c in self.rules.keys():
                s = s + self.rules[c]
            else:
                s = s + c
        self.state = s
        if os == s:
            self.finished = True
        self.generation = self.generation + 1
        if verbose:
            self.echo()

    def evolute(self, gen=None):
        """
        Generator of <gen> generation, return 'state' at each generation
        
        >>> d = D0L('F', {'F': 'XF'})
        >>> for i in d.evolute(): print i
        Traceback (most recent call last):
            ...
        Exception: <gen> must be an int
        >>> d = D0L('F', {'F': 'XF'})
        >>> for i in d.evolute(3): print i
        XF
        XXF
        XXXF

        """
        if gen is None:
            raise Exception, '<gen> must be an int'
        for i in xrange(gen):
            self.step()
            yield self.state



    def _steps(self, n):
        print '| axiom : %s' % self.axiom
        for r in self.rules.keys():
            print "| %s -> %s" % (r, self.rules[r])
        for _ in xrange(n):
            self.step(True)


import math
def _turtleBox(string, lengh=10, angle=90):
    """
    just calculate de boxing of a D0L string

    >>> _turtleBox('F')
    (0, 0, 0, 10.0)
    >>> _turtleBox('F+F')
    (0, 10.0, 0, 10.0)

    """
    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0 
    x = 0
    y = 0

    # like in turtle.mode('logo')
    head = 90
    flengh = float(lengh)

    for c in string:
        if c == 'F':
            if angle == 90:
                if head % 360 == 0:
                    x += flengh
                    xmax = max(xmax, x)
                if head % 360 == 90:
                    y += flengh
                    ymax = max(ymax, y)
                if head % 360 == 180:
                    x -= flengh
                    xmin = min(xmin, x)
                if head % 360 == 270:
                    y -= flengh
                    ymin = min(ymin, y)
            else:
                angle_rad = math.radians(head)
                x = x + math.cos(angle_rad) * lengh
                y = y + math.sin(angle_rad) * lengh
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymin = min(ymin, y)
                ymax = max(ymax, y)
        if c == '+':
            head = (head - angle + 360) % 360
        if c == '-':
            head = (head + angle) % 360

        # print xmin, xmax, ymin, ymax

    return xmin, xmax, ymin, ymax


import turtle
class D0LTurtle:
    """
    plot D0L with python turtle module

    >>> t = D0LTurtle()
    """

    def __init__(self, functions=None, lengh=10, angle=90, colors=None):
        self.lengh = lengh
        self.angle = angle
        if colors is None:
            self.colors = ['red', 'green', 'blue', 'orange', 'yellow', 'brown']

	# draw number
        self.ith_draw = 0

        # min and max x, y
        self.xmin = self.ymin = self.xmax = self.ymax = 0

        # turtle head north and positive angles is clockwise
        turtle.mode('logo')
        turtle.speed(0) # fastest
        turtle.hideturtle()
        turtle.tracer(0, 1)
	
        # set pencolor
        self.pencolor()
	
    def pencolor(self, p=None):
        if p is None:
            turtle.pencolor(self.colors[self.ith_draw % len(self.colors)])
        else:
            turtle.pencolor(p)

    def draw(self, state):
        print "draw in %s the state: %s " % (turtle.pencolor(), state)
        for c in state:
            if c == 'F':
                turtle.forward(self.lengh)
                xcor = turtle.xcor() 
                ycor = turtle.ycor() 
                self.xmin = min(self.xmin, xcor)
                self.xmax = max(self.xmax, xcor)
                self.ymin = min(self.ymin, ycor)
                self.ymay = max(self.ymax, ycor)
            if c == '+':
                turtle.left(self.angle)
            if c == '-':
                turtle.right(self.angle)

    def reset(self):
        turtle.penup()
        turtle.home()
        turtle.pendown()
        self.xmin = self.ymin = self.xmax = self.ymax = 0


    def nextdraw(self):
        # next draw
        self.ith_draw += 1

	# next color
        self.pencolor()

        # next origin
        turtle.penup()
        turtle.home()
        turtle.setx(self.xmax + 50)
        turtle.pendown()
        self.xmin = self.xmax = turtle.xcor()
        self.ymin = self.ymax = turtle.ycor()

    def done(self):
        """
        finish all draws 
        and wait for click to close de window
        """
        turtle.exitonclick()

    def draw_evolute(self, list_of_states):
        print 'Draw with:'
        print '- lengh %s' % self.lengh
        print '- angle %s ' % self.angle
        for s in list_of_states:
            self.draw(s)
            self.nextdraw()
        self.done()
        



if __name__ == '__main__':
    import doctest, sys
    print "####### doctest BEGIN ##"
    doctest.testmod()
    print "####### doctest END ####"
    sys.exit()
    g = D0L('F++F++F', {'F': 'F-F++F-F'})
    t = D0LTurtle(angle=60)
    t.draw_evolute(g.evolute(3))

    g = D0L('F', {'F': 'F-F+F+F-F'})
    t = D0LTurtle(lengh=50)
    t.draw_evolute(g.evolute(3))



