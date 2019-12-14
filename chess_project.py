"""
Chess!

Created on Fri Nov 30 19:02:32 2018

@author: danielb
"""

from tkinter import Tk, Label, Button, Frame
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
        self.button = None
        self._create_button(frame)

    def potential_moves(self, current_position):
        """Virual method for finding potential chess piece moves. Implemented
        by each child class"""
        pass

    def _create_button(self, frame):
        """Creates the piece button"""
        logging.debug("Creating a %s %s button at position %s" %
                      (self.color,
                       self.piece_type,
                       self.position))
        self.button = Button(frame,
                             text=self.piece_type[0],
                             bg=self.color,
                             fg=text_color[self.color])
        # button['command'] = lambda arg1=position: display_possible_moves(arg1)
        self.button.place(x=tile_positions[self.position].x,
                          y=tile_positions[self.position].y,
                          height=BUTTON_SIZE, width=BUTTON_SIZE)

    def update_position(self, new_position):
        """Moves the piece and updates button on the board"""
        self.position = new_position
        self.button.configure(x=tile_positions[self.position].x,
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

    def potential_moves(self):
        """Returns all potential moves and captures for a bishop"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        positive_steps = [1, 2, 3, 4, 5, 6, 7]
        possible_moves = []
        possible_captures = []
        # Diagonal down and left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal down and right
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and right
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and left
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        return(possible_moves, possible_captures)

class King(ChessPiece):
    """Child class for the King piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'King')

    def potential_moves(sel):
        """Returns all potential moves, special moves, and potential captures
        for a king"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        steps = [-1, 0, 1]
        possible_moves = []
        possible_special_moves = []
        possible_captures = []
        for i in steps:
            for j in steps:
                adjusted_column = index_to_letter(current_column + i)
                adjusted_row = current_row + j
                if adjusted_column in COLUMNS and adjusted_row in ROWS:
                    possible_move = str(adjusted_row) + adjusted_column
                    if not squares[possible_move]:
                        possible_moves.append(possible_move)
                    elif squares[possible_move]:
                        if squares[possible_move].color != self.color:
                            possible_captures.append(possible_move)

        # Check for possible castle move
        if not squares[current_position].has_been_moved:
            # Check the white pieces
            if squares[current_position].color == "White":
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
                        possible_special_moves.append(possible_move)
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
                        possible_special_moves.append(possible_move)
            # Check the black pieces
            if squares[current_position].color == "Black":
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
                        possible_special_moves.append(possible_move)
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
                        possible_special_moves.append(possible_move)

        return(possible_moves, possible_special_moves, possible_captures)

class Knight(ChessPiece):
    """Child class for the Knight piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Knight')

    def potential_moves(self):
        """Returns all potential moves and captures for a knight"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        steps = [-2, -1, 1, 2]
        possible_moves = []
        possible_captures = []
        for i in steps:
            for j in steps:
                adjusted_column = index_to_letter(current_column + i)
                adjusted_row = current_row + j
                if abs(i) + abs(j) == 3:
                    if adjusted_column in COLUMNS and adjusted_row in ROWS:
                        possible_move = str(adjusted_row) + adjusted_column
                        if not squares[possible_move]:
                            possible_moves.append(possible_move)
                        elif squares[possible_move]:
                            if squares[possible_move].color != self.color:
                                possible_captures.append(possible_move)
        return(possible_moves, possible_captures)

class Pawn(ChessPiece):
    """Child class for the Pawn piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Pawn')

    def potential_moves(self):
        """Returns all potential moves, special moves, and potential captures
        for a pawn"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        possible_moves = []
        possible_special_moves = []
        possible_captures = []
        if self.color == 'Black':
            adjusted_row = current_row - 1
        elif self.color == 'White':
            adjusted_row = current_row + 1
        if adjusted_row in rows:
            possible_move = str(adjusted_row) + index_to_letter(current_column)
            if not squares[possible_move]:
                possible_moves.append(possible_move)

        # Check for possible captures separately
        if piece_color == 'Black':
            adjusted_row = current_row - 1
        elif piece_color == 'White':
            adjusted_row = current_row + 1
        if adjusted_row in rows:
            for i in -1, 1:
                adjusted_column = index_to_letter(current_column + i)
                if adjusted_column in columns:
                    possible_capture = str(adjusted_row) + adjusted_column
                    if squares[possible_capture]:
                        if squares[possible_capture].color != piece_color:
                            possible_captures.append(possible_capture)

        # Check if the pawn hasn't been moved yet and can skip a square
        if (piece_color == 'Black' and
                not squares[current_position].has_been_moved):
            adjusted_row = current_row - 2
            check_row_in_front = current_row - 1
            possible_move = str(adjusted_row) + index_to_letter(current_column)
            check_square_in_front = str(check_row_in_front) + \
            index_to_letter(current_column)
            if (not squares[check_square_in_front] and
                    not squares[possible_move]):
                possible_moves.append(possible_move)
        elif (piece_color == 'White' and
              not squares[current_position].has_been_moved):
            adjusted_row = current_row + 2
            check_row_in_front = current_row + 1
            possible_move = str(adjusted_row) + index_to_letter(current_column)
            check_square_in_front = str(check_row_in_front) + \
            index_to_letter(current_column)
            if (not squares[check_square_in_front] and
                    not squares[possible_move]):
                possible_moves.append(possible_move)

        # Check for an En Passent
        if last_move_was_pawn_jump:
            required_column = last_move_was_pawn_jump[1]
            logging.debug("The required column for the en passent is %s" %
                          (required_column))
            if piece_color == BLACK and current_row == 4:
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
                                    possible_special_moves.append(
                                        possible_capture_move)
            elif piece_color == WHITE and current_row == 5:
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
                                    possible_special_moves.append(
                                        possible_capture_move)
        return(possible_moves, possible_special_moves, possible_captures)

class Queen(ChessPiece):
    """Child class for the Queen piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Queen')

    def potential_moves(self):
        """Returns all potential moves and captures for a queen"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        positive_steps = [1, 2, 3, 4, 5, 6, 7]
        possible_moves = []
        possible_captures = []
        # Straight moves
        # Left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Right
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Down
        for i in negative_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Up
        for i in positive_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal moves
        # Diagonal down and left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal down and right
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and right
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and left
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in COLUMNS and adjusted_row in ROWS:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != self.color:
                        possible_captures.append(possible_move)
                    break
        return(possible_moves, possible_captures)

class Rook(ChessPiece):
    """Child class for the Rook piece"""
    def __init__(self, color, position, frame):
        super().__init__(color, position, frame, 'Rook')

    def potential_moves(self):
        """Returns all potential moves and captures for a rook"""
        current_row = int(self.position[0])
        current_column = letter_to_index(self.position[1])
        negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        positive_steps = [1, 2, 3, 4, 5, 6, 7]
        possible_moves = []
        possible_captures = []
        # Horizontal movements
        # Left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Right
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in COLUMNS:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Vertical movements
        # Down
        for i in negative_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Up
        for i in positive_steps:
            adjusted_row = current_row + i
            if adjusted_row in ROWS:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        return(possible_moves, possible_captures)



































class Game():
    def __init__(self):
        # Instance variables
        self._display = BoardDisplay()
        self._pieces = []
        self._possible_move_buttons = []
        self._game_over = False
        self._turn_color = WHITE
        self._last_moved_piece = None
        self._last_move_was_pawn_jump = None
        self._previous_position_shown = None
        # Initialiation methods
        self._create_pieces()

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
            self._pieces.append(piece)
        # Then add the white pawns
        for column in COLUMNS:
            square_name = str(2) + column
            piece = Pawn(WHITE, square_name, self._display.root)
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
            self._pieces.append(piece)
        # Then add the black pawns
        for column in COLUMNS:
            square_name = str(7) + column
            piece = Pawn(BLACK, square_name, self._display.root)
            self._pieces.append(piece)

    def maintain_display(self):
        """Maintains the Tkinter display"""
        self._display.root.mainloop()

    def display_possible_moves(self, current_position):
        """Displays all possible moves for the piece in a given position"""
        # Show potential moves for a given square
        if current_position != self.previous_position_shown:
            # Get an array of possible moves, special moves, and captures
            [possible_moves, possible_special_moves, possible_captures] = \
            check_possible_moves(current_position)
            for row in ROWS:
                for column in COLUMNS:
                    position = str(row) + column
                if position in possible_captures:
                    self.create_capture_button(position, 'Red')
                elif (position in possible_moves or position in
                      possible_special_moves or position in possible_captures):
                    self.create_move_button(position, 'Blue')
            self.create_move_button(current_position)
            self.previous_position_shown = current_position

        # Stop showing the potential moves for a given square
        else:
            logging.debug("Removing the potential moves from the board")
            self.clear_possible_moves()
            self.previous_position_shown = None

    def clear_possible_moves(self):
        """Clears the possible move buttons"""
        for button in self._possible_move_buttons:
            button.destroy()
        self._possible_move_buttons.clear()

    def create_move_button(self, position, color):
        """Creates the potential move button"""
        button = Button(self._display.root, text='???',
                        bg=color, fg='White', cursor='hand2')
        #button['command'] = lambda arg1=position: display_possible_moves(arg1)
        button.place(x=tile_positions[position].x,
                     y=tile_positions[position].y,
                     height=BUTTON_SIZE, width=BUTTON_SIZE)
        self._possible_move_buttons.append(button)

    def is_piece_present(self, position):
        """Checks if there is a piece at the passed position"""
        for piece in self._pieces:
            if piece.position == position:
                return True
        return False

    def return_piece(self, position):
        """Returns the chess piece object from the passed position"""
        for piece in self._pieces:
            if piece.position == position:
                return piece
        return None

    def add_piece(self, piece_type, piece_color, position):
        """Creates the correct type of chess piece based on the inputs"""
        # Different piece types
        if piece_type == BISHOP:
            piece = Bishop(piece_color)
        elif piece_type == KING:
            piece = King(piece_color)
        elif piece_type == KNIGHT:
            piece = Knight(piece_color)
        elif piece_type == PAWN:
            piece = Pawn(piece_color)
        elif piece_type == QUEEN:
            piece = Queen(piece_color)
        elif piece_type == ROOK:
            piece = Rook(piece_color)
        self.pieces.append(piece)

    def show_game_over(self):
        """Changes the displays if the game is over"""
        #game_over_text = "Game over! " + self.turn_color + " wins!"

        # Change the move turn frame and turn all buttons to labels
        #turn_frame.destroy()
        #turn_frame = Frame(overall_turn_frame, width=250, height=100)
        #turn_frame.pack()
        #turn_label = Label(overall_turn_frame, text=game_over_text,
                           #bg="orange", fg="black")
        #turn_label.place(x=0, y=0, height=100, width=250)

        # Add the pieces but only with lables instead of buttons
        for piece in self._pieces:
            piece.disable_button()

    def move_the_piece(self, current_position, new_position):
        """Moves the chess piece in the back end of the program"""
        # Move the piece in the back end
        self.move_piece(current_position, new_position)

        # Change the turn color
        if self.turn_color == WHITE:
            self.turn_color = BLACK
        else:
            self.turn_color = WHITE

    def move_piece(self, current_position, new_position):
        """Moves the chess piece to a new position and checks some conditions
        after the move"""
        # Get possible moves and possible captures
        [possible_moves, possible_special_moves, possible_captures] = \
        check_possible_moves(current_position)

        moving_piece = self.return_piece(current_position)
        # Check if this is a capture
        if new_position in possible_captures:
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
                captured_piece.button.destroy()
                del captured_piece

        # Change the moving piece's location
        logging.info("Moving the %s %s from %s to %s",
                     moving_piece.color,
                     moving_piece.piece_type,
                     current_position,
                     new_position)
        moving_piece.update_position(new_position)

        # Check if the previous move deserves a promotion
        if moving_piece.piece_type == PAWN:
            if moving_piece.color == WHITE and new_position[0] == "8":
                logging.info("The %s %s at position %s is up for promotion" %
                             (WHITE, PAWN, new_position))
                promotion(new_position)
            elif moving_piece.color == BLACK and new_position[0] == "1":
                logging.info("The %s %s at position %s is up for promotion" %
                             (BLACK, PAWN, new_position))
                promotion(new_position)

        # Check if the previous move was an En Passent or Castle
        if new_position in possible_special_moves:
            # If it was a En Passent then capture the appropriate pawn
            if moving_piece.piece_type == PAWN:
                if new_position not in possible_captures:
                    # Determine the position of the pawn being captured
                    new_row = int(new_position[0])
                    capture_column = new_position[1]
                    if moving_piece.color == WHITE:
                        capture_row = new_row - 1
                    elif moving_piece.color == BLACK:
                        capture_row = new_row + 1
                    capture_position = str(capture_row) + capture_column
                    # TODO: Remove the piece at capture_position

            # If it was a Castle then move the appropriate rook
            if moving_piece.piece_type == KING:
                # Figure out if the castle was a queen side or king side
                if new_position[1] == "c":
                    if moving_piece.color == WHITE:
                        current_rook_position = "1a"
                        new_rook_position = "1d"
                    elif moving_piece.color == BLACK:
                        current_rook_position = "8a"
                        new_rook_position = "8d"
                    rook_piece = self.return_piece(current_rook_position)
                    rook_piece.update_position(new_rook_position)
                elif new_position[1] == "g":
                    if moving_piece.color == WHITE:
                        current_rook_position = "1h"
                        new_rook_position = "1f"
                    elif moving_piece.color == BLACK:
                        current_rook_position = "8h"
                        new_rook_position = "8f"
                    rook_piece = self.return_piece(current_rook_position)
                    rook_piece.update_position(new_rook_position)

        # Set the last moved piece
        self.last_moved_piece = new_position

        # See if the move was a pawn jumping
        if moving_piece.piece_type == PAWN:
            if abs(int(current_position[0]) - int(new_position[0])) == 2:
                self.last_move_was_pawn_jump = new_position
            else:
                self.last_move_was_pawn_jump = None
        else:
            self.last_move_was_pawn_jump = None

        # See if the piece has previously been moved and set flag
        if not moving_piece.has_been_moved:
            moving_piece.has_been_moved = True


class BoardDisplay():
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


def promotion_back_end(chosen_piece, piece_position):
    """Completes the back end managing after a pawn promotion"""
    # Then complete the promotion
    logging.debug("Completing the final step of the pawn promotion")
    if squares[piece_position].piece_type == PAWN:
        if (squares[piece_position].color == WHITE and
                piece_position[0] == '8'):
            logging.info("Promotion the %s at position %s to a %s" %
                         (piece_names[PAWN],
                          piece_position,
                          piece_names[chosen_piece]))
            squares[piece_position] = None
            add_piece(chosen_piece, WHITE, piece_position)
        elif (squares[piece_position].color == BLACK and
              piece_position[0] == '1'):
            logging.info("Promotion the %s at position %s to a %s" %
                         (piece_names[PAWN],
                          piece_position,
                          piece_names[chosen_piece]))
            squares[piece_position] = None
            add_piece(chosen_piece, BLACK, piece_position)
    else:
        print("Too late for promotion, another move has already happened")

def check_for_check():
    """Determines if the player is currently in check"""
    logging.debug("Determing if the player is in check")
    for position in squares:
        # Go through all the opponents pieces and see if they could
        # capture the king
        if squares[position] and squares[position].color != turn_color:
            [possibles_moves, possible_special_moves, possible_captures] = \
            check_possible_moves(position)
            for capture in possible_captures:
                if squares[capture].piece_type == KING:
                    logging.info("The %s %s at position %s is in check!" %
                                 (squares[capture].color,
                                  piece_names[KING],
                                  capture))
                    return True

def check_possible_moves(current_position):
    """Checks possible moves based on the piece located at the
    passed position"""
    piece = squares[current_position].piece_type
    possible_moves = []
    possible_special_moves = []
    possible_captures = []
    if piece == KING or piece == PAWN:
        [possible_moves, possible_special_moves, possible_captures] = \
        squares[current_position].potential_moves(current_position)
    elif piece == BISHOP or piece == KNIGHT or piece == QUEEN or piece == ROOK:
        [possible_moves, possible_captures] = \
        squares[current_position].potential_moves(current_position)

    moves_str = " ".join(possible_moves) + " ".join(possible_special_moves)
    captures_str = " ".join(possible_captures)
    logging.info("The possible moves for the %s %s at position %s are: %s" %
                 (squares[current_position].color,
                  piece_names[squares[current_position].piece_type],
                  current_position,
                  moves_str))
    logging.info("The possible captures for the %s %s at position %s are: %s" %
                 (squares[current_position].color,
                  piece_names[squares[current_position].piece_type],
                  current_position,
                  captures_str))

    return(possible_moves, possible_special_moves, possible_captures)

def promotion(piece_position):
    """Creates the pawn promotion display the user will use to pick a piece"""
    # Create the frame with buttons that the user will use to pick
    # a piece during promotion
    logging.debug("Creating the promotion choice frame with piece buttons")
    global piece_choice
    piece_choice = Tk()
    w3 = 425
    h3 = 150
    x3 = 2*ws/3 - w3/2
    y3 = hs*0.20 - h3/2
    piece_choice.geometry('%dx%d+%d+%d' % (w3, h3, x3, y3))
    piece_choice.title("Pawn Promotion!")
    piece_choice_frame = Frame(piece_choice, width=w3, height=h3)
    piece_choice_frame.pack()
    piece_choice_text = """Please choose the piece you would like to replace
                        the pawn"""
    piece_choice_prompt = Label(piece_choice_frame, text=piece_choice_text,
                                bg="white", fg="black")
    piece_choice_prompt.place(x=0, y=0, height=50, width=425)

    # Create the potential piece choice buttons
    q_button = Button(piece_choice_frame, text="Q", bg="green", fg="white")
    q_button['command'] = lambda arg1="Q", arg2=piece_position: \
                          promotion_button_choice(arg1, arg2)
    q_button.place(x=45, y=75, height=50, width=50)
    k_button = Button(piece_choice_frame, text="k", bg="green", fg="white")
    k_button['command'] = lambda arg1="k", arg2=piece_position: \
                          promotion_button_choice(arg1, arg2)
    k_button.place(x=140, y=75, height=50, width=50)
    r_button = Button(piece_choice_frame, text="R", bg="green", fg="white")
    r_button['command'] = lambda arg1="R", arg2=piece_position: \
                          promotion_button_choice(arg1, arg2)
    r_button.place(x=235, y=75, height=50, width=50)
    b_button = Button(piece_choice_frame, text="B", bg="green", fg="white")
    b_button['command'] = lambda arg1="B", arg2=piece_position: \
                          promotion_button_choice(arg1, arg2)
    b_button.place(x=330, y=75, height=50, width=50)

def promotion_button_choice(passed_piece, piece_position):
    """Completes the book-keeping after a pawn promotion"""
    # Change the piece in the back end and reset displays
    logging.info("The piece chosen for promotion was a %s" %
                 (piece_names[passed_piece]))
    promotion_back_end(passed_piece, piece_position)
    piece_choice.destroy()


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
