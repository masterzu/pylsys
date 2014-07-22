#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import pylsys
import turtle 

l = pylsys.D0L('F', {'F': 'F-F++F-F'})
t = pylsys.D0LTurtle(angle=60)
t.draw_evolute(l.evolute(3))



