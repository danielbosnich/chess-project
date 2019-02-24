# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:34:07 2019

@author: danielb
"""

def index_to_letter(number):
    """Changes a numerical index into its corresponding letter"""
    indexKey = {
        1: 'a',
        2: 'b',
        3: 'c',
        4: 'd',
        5: 'e',
        6: 'f',
        7: 'g',
        8: 'h'
        }
    if number < 1 or number > 8:
        return -1
    else:
        return indexKey[number]

def letter_to_index(letter):
    """Changes a letter into its corresponding numerical index"""
    letterKey = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': 8
        }
    return letterKey[letter]