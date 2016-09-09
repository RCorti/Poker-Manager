#!/usr/bin/env python
class HH_ParseError(Exception):
    def __init__(self, arg):
        self.args = arg
    def __str__(self):
        return repr(self.args)