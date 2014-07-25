#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from pylsys import *
import turtle 

# simple draw
l = D0Lsystem('F', {'F': 'F-F++F-F'})
l.step(2)
t = PlotD0LTurtle(angle=60, lsystem=l)
t.draw().done()

# draw_evolute
t = PlotD0LTurtle(angle=60, lsystem=D0Lsystem('F', {'F': 'F-F++F-F'}))
t.draw_evolute(5)


