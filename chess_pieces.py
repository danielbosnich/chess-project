"""
Created on Fri Dec 13 19:04:43 2019

@author: danielb
"""

import logging
from tkinter import Button, Label
from helpful_dictionaries import text_color, tile_positions
from helpful_functions import index_to_letter, letter_to_index

WHITE = 'White'
BLACK = 'Black'
BISHOP = 'Bishop'
KING = 'King'
KNIGHT = 'Knight'
PAWN = 'Pawn'
QUEEN = 'Queen'
ROOK = 'Rook'
BUTTON_SIZE = 50
COLUMNS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
ROWS = (1, 2, 3, 4, 5, 6, 7, 8)

class ChessPiece():
    """Class for the individual chess pieces"""
    def __init__(self, color, position, frame, piece_type):
        self.color = color
        self.piece_type = piece_type
        self.position = position
        self.has_been_moved = False
        self.possible_moves = []
        self.possible_special_moves = []
        self.possible_captures = []
        self.button = None
        self._create_button(frame)

    def check_potential_moves(self, current_position):
        """Virual method for finding potential chess piece moves. Implemented
        by each child class"""
        pass

    def clear_potential_moves(self):
        """Clears the potential move and capture lists"""
        self.possible_moves.clear()
        self.possible_special_moves.clear()
        self.possible_captures.clear()

    def _create_button(self, frame):
        """Creates the piece button"""
        logging.debug("Creating a %s %s button at position %s" %
                      (self.color,
                       self.piece_type,
                       self.position))
        self.button = Button(frame,
                             text=self.piece_type[0],
                             bg=self.color,
                             fg=text_color[self.color],
                             cursor='hand2')
        # button['command'] = lambda arg1=position: display_possible_moves(arg1)
        self.button.place(x=tile_positions[self.position].x,
                          y=tile_positions[self.position].y,
                          height=BUTTON_SIZE, width=BUTTON_SIZE)

    def update_position(self, new_position):
        """Moves the piece and updates button on the board"""
        self.position = new_position
        self.button.place(x=tile_positions[self.position].x,
                          y=tile_positions[self.position].y)

    def disable_button(self, frame):
        """Disables the button by changing it to a label"""
        self.button.destroy()
        self.button = Label(frame,
                            text=self.piece_type[0],
                            bg=self.color,
                            fg=text_color[self.color])
        self.button.place(x=tile_positions[self.position].x,
                          y=tile_positions[self.position].y,
                          height=BUTTON_SIZE, width=BUTTON_SIZE)


class Bishop(ChessPiece):
    """Child class for the Bishop piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Bishop')
        self._negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        self._positive_steps = [1, 2, 3, 4, 5, 6, 7]

    def check_potential_moves(self, squares):
        """Returns all potential moves and captures for a bishop"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        self.clear_potential_moves()

        # Diagonal down and left
        for i in self._negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Diagonal down and right
        for i in self._negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Diagonal up and right
        for i in self._positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Diagonal up and left
        for i in self._positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break

class King(ChessPiece):
    """Child class for the King piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'King')
        self.steps = [-1, 0, 1]

    def check_potential_moves(self, squares):
        """Sets all potential moves and captures for a king"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        self.clear_potential_moves()
        for i in self.steps:
            for j in self.steps:
                adjusted_column = index_to_letter(current_column + i)
                adjusted_row = current_row + j
                if adjusted_column in COLUMNS and adjusted_row in ROWS:
                    possible_move = str(adjusted_row) + adjusted_column
                    if not squares[possible_move]:
                        self.possible_moves.append(possible_move)
                    elif squares[possible_move]:
                        if squares[possible_move].color != self.color:
                            self.possible_captures.append(possible_move)

        # Check for possible castle move
        if not squares[self.position].has_been_moved:
            # Check the white pieces
            if squares[self.position].color == "White":
                # Check for king side castle first
                in_between_positions = []
                rook_position = "1h"
                if squares[rook_position]:
                    if not squares[rook_position].has_been_moved:
                        for i in 1, 2:
                            check_column = index_to_letter(current_column + i)
                            check_position = str(current_row) + check_column
                            if squares[check_position]:
                                in_between_positions.append(True)
                            else:
                                in_between_positions.append(False)
                    if all(not check for check in in_between_positions):
                        possible_move = str(current_row) + \
                        index_to_letter(current_column + 2)
                        self.possible_special_moves.append(possible_move)
                # Now check for queen side castle
                in_between_positions = []
                rook_position = "1a"
                if squares[rook_position]:
                    if not squares[rook_position].has_been_moved:
                        for i in 1, 2, 3:
                            check_column = index_to_letter(current_column - i)
                            check_position = str(current_row) + check_column
                            if squares[check_position]:
                                in_between_positions.append(True)
                            else:
                                in_between_positions.append(False)
                    if all(not check for check in in_between_positions):
                        possible_move = str(current_row) + \
                        index_to_letter(current_column - 2)
                        self.possible_special_moves.append(possible_move)
            # Check the black pieces
            elif squares[self.position].color == "Black":
                # Check for king side castle first
                in_between_positions = []
                rook_position = "8h"
                if squares[rook_position]:
                    if not squares[rook_position].has_been_moved:
                        for i in 1, 2:
                            check_column = index_to_letter(current_column + i)
                            check_position = str(current_row) + check_column
                            if squares[check_position]:
                                in_between_positions.append(True)
                            else:
                                in_between_positions.append(False)
                    if all(not check for check in in_between_positions):
                        possible_move = str(current_row) + \
                        index_to_letter(current_column + 2)
                        self.possible_special_moves.append(possible_move)
                # Now check for queen side castle
                in_between_positions = []
                rook_position = "8a"
                if squares[rook_position]:
                    if not squares[rook_position].has_been_moved:
                        for i in 1, 2, 3:
                            check_column = index_to_letter(current_column - i)
                            check_position = str(current_row) + check_column
                            if squares[check_position]:
                                in_between_positions.append(True)
                            else:
                                in_between_positions.append(False)
                    if all(not check for check in in_between_positions):
                        possible_move = str(current_row) + \
                        index_to_letter(current_column - 2)
                        self.possible_special_moves.append(possible_move)


class Knight(ChessPiece):
    """Child class for the Knight piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Knight')
        self.steps = [-2, -1, 1, 2]

    def check_potential_moves(self, squares):
        """Sets all potential moves and captures for a knight"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        self.clear_potential_moves()
        for i in self.steps:
            for j in self.steps:
                adjusted_column = index_to_letter(current_column + i)
                adjusted_row = current_row + j
                if abs(i) + abs(j) == 3:
                    if adjusted_column in COLUMNS and adjusted_row in ROWS:
                        possible_move = str(adjusted_row) + adjusted_column
                        if not squares[possible_move]:
                            self.possible_moves.append(possible_move)
                        elif squares[possible_move]:
                            if squares[possible_move].color != self.color:
                                self.possible_captures.append(possible_move)


class Pawn(ChessPiece):
    """Child class for the Pawn piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Pawn')

    def check_potential_moves(self, squares):
        """Sets all potential moves and captures for a pawn"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        self.clear_potential_moves()
        if self.color == 'Black':
            adjusted_row = current_row - 1
        elif self.color == 'White':
            adjusted_row = current_row + 1
        if adjusted_row in ROWS:
            possible_move = str(adjusted_row) + index_to_letter(current_column)
            if not squares[possible_move]:
                self.possible_moves.append(possible_move)

        # Check for possible captures separately
        if self.color == 'Black':
            adjusted_row = current_row - 1
        else:
            adjusted_row = current_row + 1
        if adjusted_row in ROWS:
            for i in -1, 1:
                adjusted_column = index_to_letter(current_column + i)
                if adjusted_column in COLUMNS:
                    possible_capture = str(adjusted_row) + adjusted_column
                    if squares[possible_capture]:
                        if squares[possible_capture].color != self.color:
                            self.possible_captures.append(possible_capture)

        # Check if the pawn hasn't been moved yet and can skip a square
        if self.color == 'Black' and not self.has_been_moved:
            adjusted_row = current_row - 2
            check_row_in_front = current_row - 1
            possible_move = str(adjusted_row) + index_to_letter(current_column)
            check_square_in_front = str(check_row_in_front) + \
            index_to_letter(current_column)
            if (not squares[check_square_in_front] and
                    not squares[possible_move]):
                self.possible_moves.append(possible_move)
        elif self.color == 'White' and not self.has_been_moved:
            adjusted_row = current_row + 2
            check_row_in_front = current_row + 1
            possible_move = str(adjusted_row) + index_to_letter(current_column)
            check_square_in_front = str(check_row_in_front) + \
            index_to_letter(current_column)
            if (not squares[check_square_in_front] and
                    not squares[possible_move]):
                self.possible_moves.append(possible_move)

        # Check for an En Passent
        # TODO: Figure out how to pass lash_move_was_pawn_jump
        last_move_was_pawn_jump = False
        if last_move_was_pawn_jump:
            required_column = last_move_was_pawn_jump[1]
            logging.debug("The required column for the en passent is %s" %
                          (required_column))
            if self.color == BLACK and current_row == 4:
                for i in -1, 1:
                    adjusted_column = index_to_letter(current_column + i)
                    if adjusted_column in COLUMNS:
                        check_for_pawn = str(current_row) + adjusted_column
                        if squares[check_for_pawn]:
                            if squares[check_for_pawn].piece_type == PAWN:
                                if adjusted_column == required_column:
                                    adjusted_row = current_row - 1
                                    possible_capture_move = str(adjusted_row) \
                                    + adjusted_column
                                    self.possible_special_moves.append(
                                        possible_capture_move)
            elif self.color == WHITE and current_row == 5:
                for i in -1, 1:
                    adjusted_column = index_to_letter(current_column + i)
                    if adjusted_column in COLUMNS:
                        check_for_pawn = str(current_row) + adjusted_column
                        if squares[check_for_pawn]:
                            if squares[check_for_pawn].piece_type == PAWN:
                                if  adjusted_column == required_column:
                                    adjusted_row = current_row + 1
                                    possible_capture_move = str(adjusted_row) \
                                    + adjusted_column
                                    self.possible_special_moves.append(
                                        possible_capture_move)

class Queen(ChessPiece):
    """Child class for the Queen piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Queen')
        self._negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        self._positive_steps = [1, 2, 3, 4, 5, 6, 7]

    def check_potential_moves(self, squares):
        """Returns all potential moves and captures for a queen"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        self.clear_potential_moves()
        # Straight moves
        # Left
        for i in self._negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Right
        for i in self._positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Down
        for i in self._negative_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Up
        for i in self._positive_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Diagonal moves
        # Diagonal down and left
        for i in self._negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Diagonal down and right
        for i in self._negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Diagonal up and right
        for i in self._positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Diagonal up and left
        for i in self._positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break

class Rook(ChessPiece):
    """Child class for the Rook piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Rook')
        self._negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        self._positive_steps = [1, 2, 3, 4, 5, 6, 7]

    def check_potential_moves(self, squares):
        """Returns all potential moves and captures for a rook"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        self.clear_potential_moves()
        # Horizontal movements
        # Left
        for i in self._negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Right
        for i in self._positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Vertical movements
        # Down
        for i in self._negative_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
        # Up
        for i in self._positive_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    self.possible_moves.append(possible_move)
                else:
                    if squares[possible_move].color != self.color:
                        self.possible_captures.append(possible_move)
                    break
