# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 19:14:43 2019

@author: danielb
"""

import unittest
from helpful_functions import index_to_letter, letter_to_index

class HelpfulFunctionsTestCase(unittest.TestCase):
    """Tests functionality of index to letter and letter to index functions"""
    
    def test_index_to_letter(self):
        """Does the index_to_letter function work properly"""
        output = []
        input_variables = [1, 2, 3, 4, 5, 6, 7, 8]
        expected_output = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for index in input_variables:
            response = index_to_letter(index)
            output.append(response)
        self.assertEqual(output, expected_output)
        
        
    def test_letter_to_index(self):
        """Does the letter_to_index function work properly"""
        output = []
        input_variables = ["a", "b", "c", "d", "e", "f", "g", "h"]
        expected_output = [1, 2, 3, 4, 5, 6, 7, 8]
        for letter in input_variables:
            response = letter_to_index(letter)
            output.append(response)
        self.assertEqual(output, expected_output)
    
unittest.main()