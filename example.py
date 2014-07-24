#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from pylsys import *
import turtle 

# the l-system
l = D0L('F', {'F': 'F-F++F-F'})
# the plot system
t = D0LTurtlePlot(angle=60, lsystem=l)

t.draw_evolute(3)



