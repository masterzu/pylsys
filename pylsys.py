#! /usr/bin/env python
# -*- coding: UTF-8 -*-

""" 
a pure python implementation of l-system (Lindenmayer system) for simulate Plants.

Classes graph:

    Lsystem: (abstract) Base for L-System grammar
        +- D0L: Determinist, context-free Lsystem grammar
    Plot: (abstract) Base plot for L-System classes
        +- D0LTurtlePlot: plot with turtle for Determinist, context-free Lsystem grammar

masterzu, 2014
""" 
VERSION = 1

# History 
# * 19 juil. 2014 - 1
# - initial version

class Lsystem:
    """
    The abstract class for L-system
    """
    def __init__(self, axiom, rules, plot=None):
        """
        init func with plot instance of type LsystemPlot
        """
        if axiom == '':
            raise ValueError, 'axiom must be non empty'
        self.state = axiom
        self.axiom = axiom
        self.rules = rules

        self.plot = plot
        if plot is not None:
            plot.Lsystem(self)

        self.generation = 0

    def plot(self, plot=None):
        """
        Get/Set plot system
        """
        # get 
        if plot is None:
            return self.plot
        # set self.plot and plot.lsystem
        self.plot = plot
        # self.plot.lsystem(self)


    def draw(self):
        """
        plot the current state
        """
        if self.plot is not None:
            self.plot.draw(self.state)

    def step(self):
        """
        advance to next generation
        """
        raise NotImplementedError

    def evolute(self, nb_gen):
        """
        Generator of nb_gen next generation

        Return: list of string
        """
        for i in xrange(nb_gen):
            self.step()
            yield self.state


class D0L(Lsystem):
    """
    D0L-system
    The simple Determinist, context free L-system.

    Works with all string, so with D0L branching rules.


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
    def __init__(self, axiom, rules, plot=None):
        """
        Args:
        axiom : string
        rules : dict(character: string)
        plot: Plot
        """
        Lsystem.__init__(self, axiom, rules, plot)
        # self.axiom = axiom
        # self.rules = rules
        # if axiom == '':
        #     raise ValueError, 'axiom must be non empty'
        # self.state = axiom
        # self.generation = 0
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

    def evolute(self, gen):
        """
        Generator of <gen> generation, return 'state' at each generation
        
        >>> d = D0L('F', {'F': 'XF'})
        >>> for i in d.evolute(3): print i
        XF
        XXF
        XXXF

        """
        return Lsystem.evolute(self, gen)



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

class Plot:
    """
    Abstract Class for Lsystem ploting
    """
    def __init__(self):
        raise NotImplementedError

    def lsystem(self, lsys=None):
        """
        Set/Get Lsystem
        """
        # get
        if lsys is None:
            return self.lsystem
        # set self.lsystem and lsys.plot
        self.lsystem = lsys
        #lsys.plot(self)

    def draw(self):
        raise NotImplementedError

class D0LTurtlePlot(Plot):
    """
    plot D0L with python turtle module
    """

    def __init__(self, lengh=10, angle=90, colors=None, lsystem=None):
        self.lengh = lengh
        self.angle = angle
        if colors is None:
            self.colors = ['red', 'green', 'blue', 'orange', 'yellow', 'brown']
        if lsystem is not None:
            self.lsystem(lsystem)

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
        # print "draw in %s the state: %s " % (turtle.pencolor(), state)
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
            self.lengh *= 0.5
            self.nextdraw()
        self.done()
        



if __name__ == '__main__':
    import doctest, sys
    doctest.testmod()



