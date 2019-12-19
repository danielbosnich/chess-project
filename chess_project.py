"""
Chess!

Created on Fri Nov 30 19:02:32 2018

@author: danielb
"""

from tkinter import Tk, Toplevel, Label, Button
import logging
from helpful_dictionaries import piece_names, text_color, tile_positions
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

    def disable_button(self, position, frame):
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

    def potential_moves(self, squares):
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



































class Game():
    """Class that represents a running of the game"""
    def __init__(self):
        # Instance variables
        self._display = BoardDisplay()
        self._turn_display = TurnDisplay()
        self._promotion_display = None
        self._pieces = []
        self._possible_move_buttons = []
        self._game_over = False
        self._turn_color = WHITE
        self._last_moved_piece = None
        self._last_move_was_pawn_jump = None
        self._previous_position_shown = None
        # Initialiation methods
        self._create_pieces()

    def maintain_display(self):
        """Maintains the Tkinter display"""
        self._display.root.mainloop()

    def _create_pieces(self):
        """Creates the chess piece objects and adds them to the board"""
        # Add the main white pieces
        for column in COLUMNS:
            square_name = str(1) + column
            if column == 'a' or column == 'h': # Rook starting points
                piece = Rook(WHITE, square_name, self._display.root)
            elif column == 'b' or column == 'g': # Knight starting points
                piece = Knight(WHITE, square_name, self._display.root)
            elif column == 'c' or column == 'f': # Bishop starting points
                piece = Bishop(WHITE, square_name, self._display.root)
            elif column == 'd': # Queen starting point
                piece = Queen(WHITE, square_name, self._display.root)
            elif column == 'e': # King starting point
                piece = King(WHITE, square_name, self._display.root)
            piece.button.bind('<ButtonRelease-1>',
                              lambda event, arg1=piece:
                              self._display_possible_moves(event, arg1))
            self._pieces.append(piece)

        # Then add the white pawns
        for column in COLUMNS:
            square_name = str(2) + column
            piece = Pawn(WHITE, square_name, self._display.root)
            piece.button.bind('<ButtonRelease-1>',
                              lambda event, arg1=piece:
                              self._display_possible_moves(event, arg1))
            self._pieces.append(piece)

        # Add the main black pieces
        for column in COLUMNS:
            square_name = str(8) + column
            if column == 'a' or column == 'h': # Rook starting points
                piece = Rook(BLACK, square_name, self._display.root)
            elif column == 'b' or column == 'g': # Knight starting points
                piece = Knight(BLACK, square_name, self._display.root)
            elif column == 'c' or column == 'f': # Bishop starting points
                piece = Bishop(BLACK, square_name, self._display.root)
            elif column == 'd': # Queen starting point
                piece = Queen(BLACK, square_name, self._display.root)
            elif column == 'e': # King starting point
                piece = King(BLACK, square_name, self._display.root)
            piece.button.bind('<ButtonRelease-1>',
                              lambda event, arg1=piece:
                              self._display_possible_moves(event, arg1))
            self._pieces.append(piece)
        # Then add the black pawns
        for column in COLUMNS:
            square_name = str(7) + column
            piece = Pawn(BLACK, square_name, self._display.root)
            piece.button.bind('<ButtonRelease-1>',
                              lambda event, arg1=piece:
                              self._display_possible_moves(event, arg1))
            self._pieces.append(piece)

    def _display_possible_moves(self, event, piece):
        """Displays all possible moves for the piece in a given position"""
        # Don't show moves if it's not their turn
        if piece.color != self._turn_color:
            self._clear_possible_moves()
            return

        # Show potential moves for a given square
        if piece.position != self._previous_position_shown:
            logging.info("Showing moves")
            if self._possible_move_buttons:
                self._clear_possible_moves()
            # Check potential moves for the piece
            piece.check_potential_moves(self._return_squares())
            for position in piece.possible_captures:
                self._create_move_button(piece, position, 'Red')
            for position in piece.possible_moves:
                self._create_move_button(piece, position, 'Blue')
            for position in piece.possible_special_moves:
                self._create_move_button(piece, position, 'Blue')
            self._previous_position_shown = piece.position

        # Stop showing the potential moves for a given square
        else:
            logging.info("Clearing moves")
            logging.debug("Removing the potential moves from the board")
            self._clear_possible_moves()
            self._previous_position_shown = None

    def _clear_possible_moves(self):
        """Clears the possible move buttons"""
        for button in self._possible_move_buttons:
            button.destroy()
        self._possible_move_buttons.clear()

    def _create_move_button(self, piece, position, color):
        """Creates the potential move button"""
        button = Button(self._display.root, text='??',
                        bg=color, fg='White', cursor='hand2')
        button.bind('<ButtonRelease-1>',
                    lambda event, arg1=piece, arg2=position:
                    self._move_piece(event, arg1, arg2))
        button.place(x=tile_positions[position].x,
                     y=tile_positions[position].y,
                     height=BUTTON_SIZE, width=BUTTON_SIZE)
        self._possible_move_buttons.append(button)

    def _is_piece_present(self, position):
        # TODO: Figure out if this is necessary
        """Checks if there is a piece at the passed position"""
        for piece in self._pieces:
            if piece.position == position:
                return True
        return False

    def _remove_piece(self, position):
        """Removes the piece at the passed position"""
        to_remove = None
        for piece in self._pieces:
            if piece.position == position:
                to_remove = piece
                break
        to_remove.button.destroy()
        self._pieces.remove(to_remove)
        del to_remove

    def return_piece(self, position):
        """Returns the chess piece object from the passed position"""
        for piece in self._pieces:
            if piece.position == position:
                return piece
        return None

    def _return_squares(self):
        """Returns a dictionary of square positions and their corresponding
        chess piece (or None if there is no piece)"""
        squares = {}
        for row in ROWS:
            for column in COLUMNS:
                square_name = str(row) + column
                squares[square_name] = None
        for piece in self._pieces:
            squares[piece.position] = piece
        return squares

    def _show_game_over(self):
        """Changes the displays if the game is over"""
        # Add the pieces but only with lables instead of buttons
        for piece in self._pieces:
            piece.disable_button()

        self._turn_display.show_game_over_display(self, WHITE)

    def _move_piece(self, event, piece, new_position):
        """Moves the chess piece to a new position and checks some conditions
        after the move"""
        self._clear_possible_moves()
        piece.check_potential_moves(self._return_squares())
        # Check if this is a capture
        if new_position in piece.possible_captures:
            captured_piece = self.return_piece(new_position)
            # Check if the king is being captured
            if captured_piece.piece_type == KING:
                # Change the flag to indicate the game is over
                logging.info("The %s king has just been captured. The game is over.",
                             captured_piece.color)
                self.game_over = True
            else:
                # Remove the piece being captured
                logging.info("The %s %s at position %s will be captured!",
                             captured_piece.color,
                             captured_piece.piece_type,
                             new_position)
            self._remove_piece(new_position)

        # Change the moving piece's location
        logging.info("Moving the %s %s from %s to %s",
                     piece.color,
                     piece.piece_type,
                     piece.position,
                     new_position)
        piece.update_position(new_position)

        # Check if the previous move deserves a promotion
        if piece.piece_type == PAWN:
            if piece.color == WHITE and new_position[0] == "8":
                logging.info("The %s %s at position %s is up for promotion",
                             WHITE, PAWN, new_position)
                self.promotion(piece)
            elif piece.color == BLACK and new_position[0] == "1":
                logging.info("The %s %s at position %s is up for promotion",
                             BLACK, PAWN, new_position)
                self.promotion(piece)

        # Check if the previous move was an En Passent or Castle
        if new_position in piece.possible_special_moves:
            # If it was a En Passent then capture the appropriate pawn
            if piece.piece_type == PAWN:
                if new_position not in piece.possible_captures:
                    # Determine the position of the pawn being captured
                    new_row = int(new_position[0])
                    capture_column = new_position[1]
                    if piece.color == WHITE:
                        capture_row = new_row - 1
                    elif piece.color == BLACK:
                        capture_row = new_row + 1
                    capture_position = str(capture_row) + capture_column
                    self._remove_piece(capture_position)

            # If it was a Castle then move the appropriate rook
            if piece.piece_type == KING:
                # Figure out if the castle was a queen side or king side
                if new_position[1] == 'c':
                    if piece.color == WHITE:
                        current_rook_position = '1a'
                        new_rook_position = '1d'
                    elif piece.color == BLACK:
                        current_rook_position = '8a'
                        new_rook_position = '8d'
                    rook_piece = self.return_piece(current_rook_position)
                    rook_piece.update_position(new_rook_position)
                elif new_position[1] == 'g':
                    if piece.color == WHITE:
                        current_rook_position = '1h'
                        new_rook_position = '1f'
                    elif piece.color == BLACK:
                        current_rook_position = '8h'
                        new_rook_position = '8f'
                    rook_piece = self.return_piece(current_rook_position)
                    rook_piece.update_position(new_rook_position)

        # Set the last moved piece
        self.last_moved_piece = new_position

        # See if the move was a pawn jumping
        if piece.piece_type == PAWN:
            if abs(int(piece.position[0]) - int(new_position[0])) == 2:
                self.last_move_was_pawn_jump = new_position
            else:
                self.last_move_was_pawn_jump = None
        else:
            self.last_move_was_pawn_jump = None

        # See if the piece has previously been moved and set flag
        if not piece.has_been_moved:
            piece.has_been_moved = True

        # Update the turn flag
        if self._turn_color == WHITE:
            self._turn_color = BLACK
        else:
            self._turn_color = WHITE

    def promotion(self, piece):
        """Completes pawn promotion by creating a promotion """
        self._promotion_display = PromotionDisplay()
        # Wait for the user input
        logging.info("Waiting")
        self._promotion_display.root.mainloop() # TODO: FIgure out why this isn't returning
        logging.info("Finished waiting")
        # If the user closed the window without choosing a piece then just
        # leave the pawn
        if self._promotion_display.chosen_piece is None:
            logging.info("No piece was chosen, leaving the pawn")
            return
        # Otherwise, change the piece out with the selected type
        chosen_piece = self._promotion_display.chosen_piece
        logging.info(chosen_piece)
        if chosen_piece == QUEEN:
            logging.info("HERE")
            new_piece = Queen(piece.color, piece.position, self._display.root)
        elif chosen_piece == KNIGHT:
            new_piece = Knight(piece.color, piece.position, self._display.root)
        elif chosen_piece == ROOK:
            new_piece = Rook(piece.color, piece.position, self._display.root)
        elif chosen_piece == BISHOP:
            new_piece = BISHOP(piece.color, piece.position, self._display.root)
        # Remove the pawn and add the new piece
        self._remove_piece(piece)
        new_piece.button.bind('<ButtonRelease-1>',
                              lambda event, arg1=piece:
                              self._display_possible_moves(event, arg1))
        self._pieces.append(new_piece)

    def check_for_check(self):
        """Determines if the player is currently in check"""
        logging.debug("Determing if the player is in check")
        squares = self._return_squares()
        for piece in self._pieces:
            piece.check_potential_moves()
            for move in piece.potential_captures:
                if squares[move].piece_type == KING:
                    logging.info("The %s %s at position %s is in check!",
                                 squares[move].color,
                                 KING,
                                 move)
                    return True
        return False


class BoardDisplay():
    """Class that implements the Tkinter display of the chess board"""
    def __init__(self):
        # Display
        self.root = None
        # Initialization methods
        self._create_display_geometry()

    def _create_display_geometry(self):
        """Creates the display geometry"""
        # Create the overall shape
        self.root = Tk()
        self.root.title("Chess Board")
        display_width = 800
        display_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        display_x_pos = screen_width/3 - display_width/2
        display_y_pos = screen_height*0.45 - display_height/2
        self.root.geometry('%dx%d+%d+%d' % (display_width,
                                            display_height,
                                            display_x_pos,
                                            display_y_pos))

        # Create the checkerboard tiles
        # Adding the tiles to the Tk root because they will never change
        board_positions = (0, 100, 200, 300, 400, 500, 600, 700)
        size = 100
        light_color = "bisque2"
        dark_color = "darkgoldenrod4"
        for y_pos in board_positions:
            if (y_pos/100)%2 == 0:
                for x_pos in board_positions:
                    if (x_pos/100)%2 == 0:
                        square = Label(self.root, bg=light_color)
                        square.place(x=x_pos, y=y_pos, height=size, width=size)
                    else:
                        square = Label(self.root, bg=dark_color)
                        square.place(x=x_pos, y=y_pos, height=size, width=size)
            else:
                for x_pos in board_positions:
                    if (x_pos/100)%2 == 0:
                        square = Label(self.root, bg=dark_color)
                        square.place(x=x_pos, y=y_pos, height=size, width=size)
                    else:
                        square = Label(self.root, bg=light_color)
                        square.place(x=x_pos, y=y_pos, height=size, width=size)


class PromotionDisplay():
    """Class that implements the Tkinter display for the promotion choice"""
    def __init__(self):
        # Display and instance variables
        self.root = None
        self.chosen_piece = None
        # Initialization methods
        self._create_display_geometry()
        self._add_widgets()

    def _create_display_geometry(self):
        """Creates the promotion piece choice display"""
        self.root = Toplevel()
        self.root.title("Pawn Promotion!")
        display_width = 425
        display_height = 150
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        display_x_pos = 2*screen_width/3 - display_width/2
        display_y_pos = screen_height*0.20 - display_height/2
        self.root.geometry('%dx%d+%d+%d' % (display_width,
                                            display_height,
                                            display_x_pos,
                                            display_y_pos))

    def _add_widgets(self):
        """Adds the widgets to the promotion display"""
        piece_choice_text = """Please choose the piece you would like to
                            replace the pawn"""
        piece_choice_prompt = Label(self.root, text=piece_choice_text,
                                    bg='white', fg='black')
        piece_choice_prompt.place(x=0, y=0, height=50, width=425)

        # Add the piece choice buttons
        queen_button = Button(self.root, text='Queen',
                              bg='green', fg='white', cursor='hand2')
        queen_button.bind('<ButtonRelease-1>',
                          lambda event, arg1=QUEEN:
                          self._set_piece_choice(event, arg1))
        queen_button.place(x=45, y=75, height=50, width=50)

        knight_button = Button(self.root, text='Knight',
                               bg='green', fg='white', cursor='hand2')
        knight_button.place(x=140, y=75, height=50, width=50)
        knight_button.bind('<ButtonRelease-1>',
                           lambda event, arg1=KNIGHT:
                           self._set_piece_choice(event, arg1))

        rook_button = Button(self.root, text='Rook',
                             bg='green', fg='white', cursor='hand2')
        rook_button.place(x=235, y=75, height=50, width=50)
        rook_button.bind('<ButtonRelease-1>',
                         lambda event, arg1=ROOK:
                         self._set_piece_choice(event, arg1))

        bishop_button = Button(self.root, text='Bishop',
                               bg='green', fg='white', cursor='hand2')
        bishop_button.place(x=330, y=75, height=50, width=50)
        bishop_button.bind('<ButtonRelease-1>',
                           lambda event, arg1=BISHOP:
                           self._set_piece_choice(event, arg1))

    def _set_piece_choice(self, event, piece_type):
        """Saves the promotion piece choice"""
        logging.info("The piece chosen for promotion was a %s", piece_type)
        self.chosen_piece = piece_type
        self.root.destroy()


class TurnDisplay():
    """Class that implements the Tkinter turn display"""
    def __init__(self):
     # Display and instance variables
        self.root = None
        self.chosen_piece = None
        self._turn_label = None
        self._is_white_turn = True
        self._white_turn_text = "White, it's your turn!"
        self._black_turn_text = "Black, it's your turn!"
        # Initialization methods
        self._create_display_geometry()

    def _create_display_geometry(self):
        """Creates the Tkinter display"""
        self.root = Toplevel()
        self.root.title('Turn Display')
        display_width = 250
        display_height = 100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        display_x_pos = 2*screen_width/3 - display_width/2
        display_y_pos = screen_height*0.45 - display_height/2
        self.root.geometry('%dx%d+%d+%d' % (display_width,
                                            display_height,
                                            display_x_pos,
                                            display_y_pos))
        self._turn_label = Label(self.root, text=self._white_turn_text,
                                 bg="white", fg="black")
        self._turn_label.place(x=0, y=0, height=100, width=250)

    def toggle_turn_display(self):
        """Toggles the turn display"""
        if self._is_white_turn:
            self._turn_label.configure(text=self._white_turn_text,
                                       bg='white', fg='black')
            self._is_white_turn = False
        else:
            self._turn_label.configure(text=self._black_turn_text,
                                       bg='black', fg='white')
            self._is_white_turn = True

    def show_game_over_display(self, winner):
        """Updates the display to show the game over text"""
        game_over_text = "Game over! " + winner + " wins!"
        self._turn_label.configure(text=game_over_text,
                                   bg='orange', fg='black')


def main():
    """Main function"""
    # Start up logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s : %(funcName)s() - %(message)s',
        level=logging.INFO)
    logging.info("Starting the game and the logger")

    # Start the game
    game = Game()
    game.maintain_display()

    # Close the logger
    logging.info("Ending the game and shutting down the logger")
    logging.shutdown()

if __name__ == "__main__":
    main()
