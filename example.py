#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from pylsys import *
import turtle 

# simple draw
l = D0Lsystem('F', {'F': 'F+F--F+F'})
print l
l.step(3)
t = PlotD0LTurtle(angle=60, lsystem=l)
t.draw().done()

# draw_evolute
t = PlotD0LTurtle(angle=60, lsystem=D0Lsystem('F', {'F': 'F+F--F+F'}))
t.draw_evolute(3)


# simple branch draw
l = D0Lsystem('F', {'F': 'F[+F][-F]F'})
print l
l.step(3)
t = PlotD0LBranchTurtle(angle=12, lsystem=l)
t.draw().done()

# draw_evolute with branches
t = PlotD0LBranchTurtle(angle=12, lsystem=D0Lsystem('F', {'F': 'F[+F][-F]F'}))
t.draw_evolute(3)

