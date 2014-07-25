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
        self._check_axiom()

        # check plot and set plot.lsys
        if plot is not None:
            self._check_plot()
            plot.lsystem(self)

	# the current state
        self._current_state = axiom
        self.generation = 0

    def _check_axiom(self):
        """
        axiom must be a string
        """
        if not isinstance(self.axiom, ''.__class__) or self.axiom == '':
            raise TypeError('axiom must be a non empty string')

    def _check_rules(self):
        """
        NotImplementedError

        rules must be define in subclass
        """
        raise NotImplementedError

    def _check_plot(self):
        """
        plot must be a instance of Plot subclass
        """
        if not issubclass(self._plot.__class__, Plot):
            raise TypeError('plot must be a instance of Plot subclass')


    def state(self):
        """
        return current state

        >>> l = BaseLsystem('F', '')
        >>> l.state()
        'F'
        """
        return self._current_state


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
        self._plot = plot
        self._check_plot()
        # FIXME and plot.lsystem
        # self.plot.lsystem(self)


    def draw(self):
        """
        plot the current state
        """
        if self.plot is not None:
            self.plot.draw(self.string())

    def step(self, count):
        """
        advance to next generation and return the new state

        NotImplementedError
        """
        raise NotImplementedError

    def evolute(self, nb_gen):
        """
        Generator of nb_gen next generation

        Return: list of string
        """
        for i in xrange(nb_gen):
            self.step()
            yield self._current_state


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
        self._check_rules()

        self.finished = False

    def _check_rules(self):
        if not isinstance(self.rules, {}.__class__):
            raise TypeError('rules must be a non empty dict')
        if self.rules.keys() == []:
            raise TypeError('rules must be a non empty dict')

    def __str__(self):
        """
        return the current state

        >>> d = D0Lsystem('F', {'F': 'F+F'})
        >>> str(d)
        'F'
        >>> d.step()
        'F+F'
        >>> print d
        F+F
        >>> str(d)
        'F+F'
        """
        if self._current_state is None:
            return '(none)'
        return str(self._current_state)
    
    def __repl__(self):
        return self.__str__()

    def step(self, count=1):
        """
        calculate <count>  step of L-system

        Returns:
        	the new state

        >>> l = D0Lsystem('F', {'F': 'CF'})
        >>> l.step()
        'CF'
        >>> l.step(1)
        'CCF'
        >>> l.step(2)
        'CCCCF'
        """
        for i in xrange(count):
            if self.finished:
                return self._current_state


            s = ""
            os = self._current_state
            for c in self._current_state:
                if c in self.rules.keys():
                    s = s + self.rules[c]
                else:
                    s = s + c
            self._current_state = s
            if os == s:
                self.finished = True
            self.generation = self.generation + 1

        return self._current_state

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
            self.step()
            print 'gen ' + str(self.generation) + ': ' + self._current_state

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

    All public func must return self to chain the call
    """
    def __init__(self):
        """
        reimplement in subclasses
        """
        pass

    def lsystem(self, lsys=None):
        """
        Set/Get Lsystem

        >>> p = Plot()
        >>> p.lsystem(1)
        Traceback (most recent call last):
            ...
        TypeError: lsystem must be a instance of BaseLsystem subclass

        >>> p.lsystem(BaseLsystem('F', {}))
        >>> l = p.lsystem()
        >>> isinstance(l, BaseLsystem)
        True
        >>> l.state()
        'F'
        >>> p.lsystem(D0Lsystem('F',{'F': 'F'}))
        >>> l = p.lsystem()
        >>> isinstance(l, D0Lsystem)
        True
        >>> l.state()
        'F'
        """
        # get
        if lsys is None:
            return self._lsystem
        # set self._lsystem and lsys.plot
        self._lsystem = lsys
        self._check_lsystem()

    def _check_lsystem(self):
        if not issubclass(self._lsystem.__class__, BaseLsystem):
            raise TypeError('lsystem must be a instance of BaseLsystem subclass')
        

    def draw(self):
        """
        NotImplementedError
        """
        raise NotImplementedError

class PlotD0LTurtle(Plot):
    """
    plot D0L with python turtle module
    """

    def __init__(self, lengh=10, angle=90, colors=None, lsystem=None):
        import turtle
        self.lengh = lengh
        self.angle = angle
        if colors is None:
            self.colors = ['red', 'green', 'blue', 'orange', 'yellow', 'brown']
        if lsystem is not None:
            self.lsystem(lsystem)

	# draw number
        self.ith_draw = 0

	# origin of next draw
        self.origin = [0, 0]

        # bounding_box
        self._box = 0, 0, 0, 0


        # turtle head north and positive angles is clockwise
        turtle.mode('world')
        turtle.setheading(90)
        turtle.speed(0) # fastest
        turtle.hideturtle()
        turtle.tracer(0, 1)
	
        # set pencolor
        self.pencolor()

    ###
    # plot functions
    # return self
    ###
	
    def pencolor(self, p=None):
        import turtle
        if p is None:
            turtle.pencolor(self.colors[self.ith_draw % len(self.colors)])
        else:
            turtle.pencolor(p)
        return self

    def draw(self):
        import turtle

        state = self.lsystem().state()

	# calculate de bounding box
        self._box = self._bounding_box()
        xmin, xmax, ymin, ymax = self._box

        # change origin to translate draw in positive x, y
        if xmin < 0:
            self.origin[0] -= xmin
            # self.origin = self.origin[0] - xmin, self.origin[1]
        # if ymin < 0:
        #     self.origin = self.origin[0], self.origin[1] - ymin

        if any(self.origin):
            self._move_turtle_origin()


        for c in state:
            if c == 'F':
                turtle.forward(self.lengh)
                # xcor = turtle.xcor() 
                # ycor = turtle.ycor() 
                # self.xmin = min(self.xmin, xcor)
                # self.xmax = max(self.xmax, xcor)
                # self.ymin = min(self.ymin, ycor)
                # self.ymay = max(self.ymax, ycor)
            if c == '+':
                turtle.left(self.angle)
            if c == '-':
                turtle.right(self.angle)
        return self

    def reset(self):
        import turtle
        turtle.penup()
        turtle.home()
        turtle.pendown()
        self.origin = [0, 0]
        return self


    def nextdraw(self):
        import turtle
        # next draw
        self.ith_draw += 1

	# next color
        self.pencolor()

        # move turtle
        self._move_turtle_nextdraw()

        return self

    def done(self):
        import turtle
        """
        finish all draws 
        and wait for click to close de window
        """
        # change the screen size
        x0, y0 = self.origin
        xmin, xmax, ymin, ymax = self._box
	
        # FIXME: I suppose self._box if bigger when self.generation is bigger
        width = x0 + xmax - xmin
        height = y0 + ymax - ymin
        # use size to preserve aspect ratio = 1
        size = max(width, height)
        # turtle.screensize(canvwidth=200, canvheight=200)
        turtle.setup(400, 400)
        turtle.setworldcoordinates(0, 0, size, size)
        # print "screen = %dx%d" % (width, height)
        turtle.exitonclick()
        return self

    def draw_evolute(self, i):
        """
        draw evolution state using lsystem.evolute(i)
        """
        # print 'Draw with:'
        # print '- lengh %s' % self.lengh
        # print '- angle %s ' % self.angle
        for s in self.lsystem().evolute(i):
            # print "o=%s" % (self.origin,)
            self.draw()
            # print "box=%s" % (self._box,)
            self.lengh *= 0.5
            self.nextdraw()
        self.done()
        return self

    def _move_turtle_origin(self):
        import turtle
        turtle.penup()
        turtle.setpos(self.origin)
        turtle.pendown()

    def _move_turtle_nextdraw(self):
        import turtle
        self.origin[0] += 10
        self._move_turtle_origin()



    ###
    # private function
    ###

    def _bounding_box(self):
        """
        just calculate de boxing of a D0L string

        Return:
            (int xmin, int xmax, int ymin, int ymax)
        >>> PlotD0LTurtle(lsystem=D0Lsystem('F', {'F': 'F'}))._bounding_box()
        (0, 0, 0, 10)
        >>> PlotD0LTurtle(lsystem=D0Lsystem('F+F', {'F': 'F'}))._bounding_box()
        (0, 10, 0, 10)
        >>> PlotD0LTurtle(lsystem=D0Lsystem('F-F', {'F': 'F'}))._bounding_box()
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
        lengh = self.lengh
        angle = self.angle
        flengh = float(lengh)

        state = self.lsystem().state()


        for c in state:
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
                    x = x + math.cos(angle_rad) * flengh
                    y = y + math.sin(angle_rad) * flengh
                    xmin = min(xmin, x)
                    xmax = max(xmax, x)
                    ymin = min(ymin, y)
                    ymax = max(ymax, y)
            if c == '+':
                head = (head - angle + 360) % 360
            if c == '-':
                head = (head + angle) % 360
	# print "_bounding_box(%s) = %d, %d, %d, %d" % (state, xmin, xmax, ymin, ymax)
        return _bounding_box(xmin, xmax, ymin, ymax)


        



if __name__ == '__main__':
    import doctest, sys
    doctest.testmod()



