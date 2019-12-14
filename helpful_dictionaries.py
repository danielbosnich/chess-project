"""
Created on Sat Feb 23 18:16:43 2019

@author: danielb
"""

from collections import namedtuple
   
# Dicitonary with whole piece name based on piece character
piece_names = {
        'B': 'Bishop',
        'K': 'King',
        'k': 'Knight',
        'P': 'Pawn',
        'Q': 'Queen',
        'R': 'Rook'
        }
 
# Dictionary with text color to use based on piece color 
text_color = {
        'Black': 'White',
        'Red': 'White',
        'Blue': 'White',
        'White': 'Black'
        }

# Dictionary with x and y positions based on tile name
TileTuple = namedtuple('TileTuple', 'x y')
tile_positions = {
    '1a': TileTuple(25, 725),
    '2a': TileTuple(25, 625),
    '3a': TileTuple(25, 525),
    '4a': TileTuple(25, 425),
    '5a': TileTuple(25, 325),
    '6a': TileTuple(25, 225),
    '7a': TileTuple(25, 125),
    '8a': TileTuple(25, 25),
    '1b': TileTuple(125, 725),
    '2b': TileTuple(125, 625),
    '3b': TileTuple(125, 525),
    '4b': TileTuple(125, 425),
    '5b': TileTuple(125, 325),
    '6b': TileTuple(125, 225),
    '7b': TileTuple(125, 125),
    '8b': TileTuple(125, 25),
    '1c': TileTuple(225, 725),
    '2c': TileTuple(225, 625),
    '3c': TileTuple(225, 525),
    '4c': TileTuple(225, 425),
    '5c': TileTuple(225, 325),
    '6c': TileTuple(225, 225),
    '7c': TileTuple(225, 125),
    '8c': TileTuple(225, 25),
    '1d': TileTuple(325, 725),
    '2d': TileTuple(325, 625),
    '3d': TileTuple(325, 525),
    '4d': TileTuple(325, 425),
    '5d': TileTuple(325, 325),
    '6d': TileTuple(325, 225),
    '7d': TileTuple(325, 125),
    '8d': TileTuple(325, 25),
    '1e': TileTuple(425, 725),
    '2e': TileTuple(425, 625),
    '3e': TileTuple(425, 525),
    '4e': TileTuple(425, 425),
    '5e': TileTuple(425, 325),
    '6e': TileTuple(425, 225),
    '7e': TileTuple(425, 125),
    '8e': TileTuple(425, 25),
    '1f': TileTuple(525, 725),
    '2f': TileTuple(525, 625),
    '3f': TileTuple(525, 525),
    '4f': TileTuple(525, 425),
    '5f': TileTuple(525, 325),
    '6f': TileTuple(525, 225),
    '7f': TileTuple(525, 125),
    '8f': TileTuple(525, 25),
    '1g': TileTuple(625, 725),
    '2g': TileTuple(625, 625),
    '3g': TileTuple(625, 525),
    '4g': TileTuple(625, 425),
    '5g': TileTuple(625, 325),
    '6g': TileTuple(625, 225),
    '7g': TileTuple(625, 125),
    '8g': TileTuple(625, 25),
    '1h': TileTuple(725, 725),
    '2h': TileTuple(725, 625),
    '3h': TileTuple(725, 525),
    '4h': TileTuple(725, 425),
    '5h': TileTuple(725, 325),
    '6h': TileTuple(725, 225),
    '7h': TileTuple(725, 125),
    '8h': TileTuple(725, 25)
}