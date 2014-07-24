#! /usr/bin/env python
# -*- coding: UTF-8 -*-

""" 
a pure python implementation of l-system (Lindenmayer system) for simulate Plants.

Classes graph:

    BaseLsystem: (abstract) Base for L-System grammar
        +- D0Lsystem: Determinist, context-free Lsystem grammar
    Plot: (abstract) Base plot for L-System classes
        +- PlotD0LTurtle: plot with turtle for Determinist, context-free Lsystem grammar

masterzu, 2014
""" 
VERSION = 1

# History 
# * 19 juil. 2014 - 1
# - initial version

import math
import turtle

class BaseLsystem:
    """
    The abstract class for L-system
    """
    def __init__(self, axiom, rules, plot=None):
        """
        init func with plot instance of type LsystemPlot

        rules tests must be made on subclasses

        >>> BaseLsystem('', '')
        Traceback (most recent call last):
            ...
        TypeError: axiom must be a non empty string

        >>> l = BaseLsystem('Q', '')

        >>> BaseLsystem('Q', '', '')
        Traceback (most recent call last):
            ...
        TypeError: plot must be a instance of Plot subclass
        >>> p = PlotD0LTurtle()
        >>> l = BaseLsystem('Q', '', p)
        """
        # setting
        self.axiom = axiom
        self.rules = rules
        self._plot = plot

        # check axiom
        self.check_axiom()

        # check plot and set plot.lsys
        if plot is not None:
            self.check_plot()
            plot.lsystem(self)

	# the current state
        self.state = axiom
        self.generation = 0

    def check_axiom(self):
        """
        axiom must be a string
        """
        if not isinstance(self.axiom, ''.__class__) or self.axiom == '':
            raise TypeError('axiom must be a non empty string')

    def check_rules(self):
        """
        NotImplementedError

        rules must be define in subclass
        """
        raise NotImplementedError

    def check_plot(self):
        """
        plot must be a instance of Plot subclass
        """
        if not issubclass(self._plot.__class__, Plot):
            raise TypeError('plot must be a instance of Plot subclass')




    def plot(self, plot=None):
        """
        Get/Set plot system

        >>> l = BaseLsystem('Q', '')
        >>> l.plot() is None
        True
        >>> l.plot(3)
        Traceback (most recent call last):
            ...
        TypeError: plot must be a instance of Plot subclass
        >>> p = PlotD0LTurtle()
        >>> l.plot(p)
        >>> isinstance(l.plot(), PlotD0LTurtle)
        True
        """
        # get 
        if plot is None:
            return self._plot
        # set self.plot 
        if not issubclass(plot.__class__, Plot):
            raise TypeError('plot must be a instance of Plot subclass')
        self._plot = plot
        # FIXME and plot.lsystem
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


class D0Lsystem(BaseLsystem):
    """
    A simple Determinist, context free L-system.

    Works with all string, so with D0L branching rules.

    """
    def __init__(self, axiom, rules, plot=None):
        """
        Args:
        axiom : string
        rules : dict(character: string)
        plot: instance of Plot subclass

        >>> D0Lsystem('F','')
        Traceback (most recent call last):
            ...
        TypeError: rules must be a non empty dict
        >>> D0Lsystem('Q',{})
        Traceback (most recent call last):
            ...
        TypeError: rules must be a non empty dict
        >>> l = D0Lsystem('Q',{1: 2})
        """
        BaseLsystem.__init__(self, axiom, rules, plot)

        # check rules is a dict
        self.check_rules()

        self.finished = False

    def check_rules(self):
        if not isinstance(self.rules, {}.__class__):
            raise TypeError('rules must be a non empty dict')
        if self.rules.keys() == []:
            raise TypeError('rules must be a non empty dict')


    def __repl__(self):
        return 'gen ' + str(self.generation) + ': ' + str(self)

    def __str__(self):
        """
        >>> d = D0Lsystem('F', {'F': 'F+F'})
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
        
        >>> d = D0Lsystem('F', {'F': 'XF'})
        >>> for i in d.evolute(3): print i
        XF
        XXF
        XXXF

        """
        return BaseLsystem.evolute(self, gen)



    def _steps(self, n):
        """
        >>> D0Lsystem('F+F+F',{'F': 'F-F++F-F'})._steps(2)
        | axiom : F+F+F
        | F -> F-F++F-F
        gen 1: F-F++F-F+F-F++F-F+F-F++F-F
        gen 2: F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F+F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F+F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F
        >>> D0Lsystem('X',{'X': 'F[+X]F[-X]', 'F': 'FF'})._steps(3)
        | axiom : X
        | X -> F[+X]F[-X]
        | F -> FF
        gen 1: F[+X]F[-X]
        gen 2: FF[+F[+X]F[-X]]FF[-F[+X]F[-X]]
        gen 3: FFFF[+FF[+F[+X]F[-X]]FF[-F[+X]F[-X]]]FFFF[-FF[+F[+X]F[-X]]FF[-F[+X]F[-X]]]
        """
        print '| axiom : %s' % self.axiom
        for r in self.rules.keys():
            print "| %s -> %s" % (r, self.rules[r])
        for _ in xrange(n):
            self.step(True)

def _bounding_box(xmin, xmax, ymin, ymax):
    """
    Calculate the bounding box in integer from float one 

    >>> _bounding_box(0.0, 0.0, 0.0, 0.0)
    (0, 0, 0, 0)
    >>> _bounding_box(0.1, -0.1, 0.0, 0.0)
    Traceback (most recent call last):
        ...
    ValueError
    >>> _bounding_box(-0.1, 0.1, 0.0, 0.1)
    (-1, 1, 0, 1)
    """
    def m(f):
        return int(math.floor(f))
    def M(f):
        return int(math.ceil(f))

    if xmin > xmax or ymin > ymax:
        raise ValueError

    return m(xmin), M(xmax), m(ymin), M(ymax)




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

class PlotD0LTurtle(Plot):
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

    def draw_evolute(self, i):
        """
        draw evolution state using lsystem.evolute(i)
        """
        print 'Draw with:'
        print '- lengh %s' % self.lengh
        print '- angle %s ' % self.angle
        for s in self.lsystem.evolute(i):
            self.draw(s)
            self.lengh *= 0.5
            self.nextdraw()
        self.done()

    def _bbox(self, lengh=10, angle=90):
        """
        just calculate de boxing of a D0L string

        Return:
            (int xmin, int xmax, int ymin, int ymax)

        >> PlotD0lTurtle(lsystem=D0Lsystem('F', {'F': 'F'}))._bbox()
        (0, 0, 0, 10)
        >> PlotD0lTurtle(lsystem=D0Lsystem('F', {'F': 'F+F'}))._bbox()
        (0, 10, 0, 10)
        >> PlotD0lTurtle(lsystem=D0Lsystem('F', {'F': 'F-F'}))._bbox()
        (-10, 0, 0, 10)

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

        string = self.state

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

        return _bounding_box(xmin, xmax, ymin, ymax)
        



if __name__ == '__main__':
    import doctest, sys
    doctest.testmod()



