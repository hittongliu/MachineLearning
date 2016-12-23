#! /usr/bin/env python
def f():
  global x = 1
  x = x+1
f()
print x
def f2():
  x = x+1
f2()
print x
