# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 19:14:43 2019

@author: danielb
"""

import unittest
from chess_project import ChessPiece, Bishop, King, Knight, Pawn, Queen, Rook


class PieceTypeAndColorTestCases(unittest.TestCase):
    """Tests out the piece type and piece color method variables"""        
    def test_bishop_piece_type(self):
        expected_output = "B"
        my_piece = Bishop("White")
        self.assertEqual(my_piece.piece_type, expected_output)
        
    def test_bishop_piece_color(self):
        expected_output = "White"
        my_piece = Bishop("White")
        self.assertEqual(my_piece.color, expected_output)
        
    def test_king_piece_type(self):
        expected_output = "K"
        my_piece = King("Black")
        self.assertEqual(my_piece.piece_type, expected_output)
        
    def test_king_piece_color(self):
        expected_output = "Black"
        my_piece = King("Black")
        self.assertEqual(my_piece.color, expected_output)
        
    def test_knight_piece_type(self):
        expected_output = "k"
        my_piece = Knight("White")
        self.assertEqual(my_piece.piece_type, expected_output)
        
    def test_knight_piece_color(self):
        expected_output = "White"
        my_piece = Knight("White")
        self.assertEqual(my_piece.color, expected_output)
        
    def test_pawn_piece_type(self):
        expected_output = "P"
        my_piece = Pawn("Black")
        self.assertEqual(my_piece.piece_type, expected_output)
        
    def test_pawn_piece_color(self):
        expected_output = "Black"
        my_piece = Pawn("Black")
        self.assertEqual(my_piece.color, expected_output)
        
    def test_queen_piece_type(self):
        expected_output = "Q"
        my_piece = Queen("White")
        self.assertEqual(my_piece.piece_type, expected_output)
        
    def test_queen_piece_color(self):
        expected_output = "White"
        my_piece = Queen("White")
        self.assertEqual(my_piece.color, expected_output)
        
    def test_rook_piece_type(self):
        expected_output = "R"
        my_piece = Rook("Black")
        self.assertEqual(my_piece.piece_type, expected_output)
        
    def test_rook_piece_color(self):
        expected_output = "Black"
        my_piece = Rook("Black")
        self.assertEqual(my_piece.color, expected_output)
        
        
unittest.main()