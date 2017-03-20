#!/usr/bin/python
# -*- coding: utf-8 -*-


class cyEntity:
    """成语实体类"""
    id = 0
    name = ''
    spell = ''
    content = ''
    derivation = ''
    samples = ''
    first = ''
    last = ''

    def __init__(self, cydbrs):
        self.id = cydbrs[0]
        self.name = cydbrs[1]
        self.spell = cydbrs[2]
        self.content = cydbrs[3]
        self.derivation = cydbrs[4]
        self.samples = cydbrs[5]
        self.first = cydbrs[6]
        self.last = cydbrs[7]

    def toString(self):
        return "| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % \
              (self.id, self.name, self.spell, self.content, self.derivation,
               self.samples, self.first, self.last)

