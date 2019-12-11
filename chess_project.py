"""
Chess!

Created on Fri Nov 30 19:02:32 2018

@author: danielb
"""

from tkinter import Tk, Label, Button, Frame
import logging
from helpful_dictionaries import piece_names, text_color
from helpful_functions import index_to_letter, letter_to_index


class ChessPiece():
    """Class for the individual chess pieces"""
    def __init__(self, color):
        self.color = color
        self.has_been_moved = False

    def potential_moves(self, current_position):
        """Virual method for finding potential chess piece moves. Implemented
        by each child class"""
        pass

class Bishop(ChessPiece):
    """Child class for the Bishop"""
    piece_type = "B"
    def __init__(self, color):
        super().__init__(color)

    def potential_moves(self, current_position):
        """Returns all potential moves and captures for a bishop"""
        current_row = int(current_position[0])
        current_column = letter_to_index(current_position[1])
        piece_color = squares[current_position].color
        negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        positive_steps = [1, 2, 3, 4, 5, 6, 7]
        possible_moves = []
        possible_captures = []
        # Diagonal down and left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal down and right
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and right
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and left
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        return(possible_moves, possible_captures)

class King(ChessPiece):
    """Child class for the King"""
    piece_type = "K" # Note, upper case 'K' for King
    def __init__(self, color):
        super().__init__(color)

    def potential_moves(self, current_position):
        """Returns all potential moves, special moves, and potential captures
        for a king"""
        current_row = int(current_position[0])
        current_column = letter_to_index(current_position[1])
        piece_color = squares[current_position].color
        steps = [-1, 0, 1]
        possible_moves = []
        possible_special_moves = []
        possible_captures = []
        for i in steps:
            for j in steps:
                adjusted_column = index_to_letter(current_column + i)
                adjusted_row = current_row + j
                if adjusted_column in columns and adjusted_row in rows:
                    possible_move = str(adjusted_row) + adjusted_column
                    if not squares[possible_move]:
                        possible_moves.append(possible_move)
                    elif squares[possible_move]:
                        if squares[possible_move].color != piece_color:
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
    """Child class for the Knight"""
    piece_type = "k" # Note, lower case 'k' for Knight
    def __init__(self, color):
        super().__init__(color)

    def potential_moves(self, current_position):
        """Returns all potential moves and captures for a knight"""
        current_row = int(current_position[0])
        current_column = letter_to_index(current_position[1])
        piece_color = squares[current_position].color
        steps = [-2, -1, 1, 2]
        possible_moves = []
        possible_captures = []
        for i in steps:
            for j in steps:
                adjusted_column = index_to_letter(current_column + i)
                adjusted_row = current_row + j
                if abs(i) + abs(j) == 3:
                    if adjusted_column in columns and adjusted_row in rows:
                        possible_move = str(adjusted_row) + adjusted_column
                        if not squares[possible_move]:
                            possible_moves.append(possible_move)
                        elif squares[possible_move]:
                            if squares[possible_move].color != piece_color:
                                possible_captures.append(possible_move)
        return(possible_moves, possible_captures)

class Pawn(ChessPiece):
    """Child class for the Pawn"""
    piece_type = "P"
    def __init__(self, color):
        super().__init__(color)

    def potential_moves(self, current_position):
        """Returns all potential moves, special moves, and potential captures
        for a pawn"""
        current_row = int(current_position[0])
        current_column = letter_to_index(current_position[1])
        piece_color = squares[current_position].color
        possible_moves = []
        possible_special_moves = []
        possible_captures = []
        if piece_color == 'Black':
            adjusted_row = current_row - 1
        elif piece_color == 'White':
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
                    if adjusted_column in columns:
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
                    if adjusted_column in columns:
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
    """Child class for the Queen"""
    piece_type = "Q"
    def __init__(self, color):
        super().__init__(color)

    def potential_moves(self, current_position):
        """Returns all potential moves and captures for a queen"""
        current_row = int(current_position[0])
        current_column = letter_to_index(current_position[1])
        piece_color = squares[current_position].color
        negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        positive_steps = [1, 2, 3, 4, 5, 6, 7]
        possible_moves = []
        possible_captures = []
        # Straight moves
        # Left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in columns:
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
            if adjusted_column in columns:
                possible_move = str(current_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Down
        for i in negative_steps:
            adjusted_row = current_row + i
            if adjusted_row in rows:
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
            if adjusted_row in rows:
                possible_move = str(adjusted_row) + \
                index_to_letter(current_column)
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal moves
        # Diagonal down and left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal down and right
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and right
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row + i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        # Diagonal up and left
        for i in positive_steps:
            adjusted_column = index_to_letter(current_column + i)
            adjusted_row = current_row - i
            if adjusted_column in columns and adjusted_row in rows:
                possible_move = str(adjusted_row) + adjusted_column
                if not squares[possible_move]:
                    possible_moves.append(possible_move)
                elif squares[possible_move]:
                    if squares[possible_move].color != piece_color:
                        possible_captures.append(possible_move)
                    break
        return(possible_moves, possible_captures)

class Rook(ChessPiece):
    """Child class for the Rook"""
    piece_type = "R"
    def __init__(self, color):
        super().__init__(color)

    def potential_moves(self, current_position):
        """Returns all potential moves and captures for a rook"""
        current_row = int(current_position[0])
        current_column = letter_to_index(current_position[1])
        piece_color = squares[current_position].color
        negative_steps = [-1, -2, -3, -4, -5, -6, -7]
        positive_steps = [1, 2, 3, 4, 5, 6, 7]
        possible_moves = []
        possible_captures = []
        # Horizontal movements
        # Left
        for i in negative_steps:
            adjusted_column = index_to_letter(current_column + i)
            if adjusted_column in columns:
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
            if adjusted_column in columns:
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
            if adjusted_row in rows:
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
            if adjusted_row in rows:
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
        self.game_over = False
        self.columns = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        self.rows = (1, 2, 3, 4, 5, 6, 7, 8)
        self.squares = {}
        self.last_moved_piece = None
        self.last_move_was_pawn_jump = None


class Board():
    def __init__(self):
        self.display = BoardDisplay()


class BoardDisplay():
    def __init__(self):
        # Display
        self.root = None
        self.frame = None
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
        self.frame = Frame(self.root,
                           width=display_width,
                           height=display_height)
        self.frame.pack()
        
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
        

def move_piece(current_position, new_position):
    """Moves the chess piece to a new position and checks some conditions
    after the move"""
    # First, make sure there's a piece at the current position
    try:
        assert squares[current_position], "There's no piece at that position"
    except AssertionError as error:
        logging.error(error)
        raise

    # Get possible moves and possible captures
    [possible_moves, possible_special_moves, possible_captures] = \
    check_possible_moves(current_position)

    piece_copy = squares[current_position].piece_type
    color_copy = squares[current_position].color
    # Check if this is a capture
    if new_position in possible_captures:
        # Check if the king is being captured
        if squares[new_position].piece_type == KING:
            # Change the flag to indicate the game is over
            logging.info("The %s %s has just been captured. The game is over" %
                         (squares[new_position].color,
                          piece_names[KING]))
            global game_over
            game_over = True
            squares[new_position] = None
        else:
            # Remove the piece being captured
            logging.info("The %s %s at position %s will be captured!" %
                         (squares[new_position].color,
                          piece_names[squares[new_position].piece_type],
                          new_position))
            squares[new_position] = None
    # Change the moving piece's location
    logging.info("Moving the %s %s from %s to %s" %
                 (color_copy,
                  piece_names[piece_copy],
                  current_position,
                  new_position))
    add_piece(piece_copy, color_copy, new_position)
    # And remove the piece from its previous location
    squares[current_position] = None

    # Check if the previous move deserves a promotion
    if squares[new_position].piece_type == PAWN:
        if squares[new_position].color == WHITE and new_position[0] == "8":
            logging.info("The %s %s at position %s is up for promotion" %
                         (WHITE, piece_names[PAWN], new_position))
            promotion(new_position)
        elif squares[new_position].color == BLACK and new_position[0] == "1":
            logging.info("The %s %s at position %s is up for promotion" %
                         (BLACK,
                          piece_names[PAWN],
                          new_position))
            promotion(new_position)

    # Check if the previous move was an En Passent or Castle
    if new_position in possible_special_moves:
        # If it was a En Passent then capture the appropriate pawn
        if squares[new_position].piece_type == PAWN:
            if new_position not in possible_captures:
                #Determine the position of the pawn being captured
                new_row = int(new_position[0])
                capture_column = new_position[1]
                if squares[new_position].color == WHITE:
                    capture_row = new_row - 1
                elif squares[new_position].color == BLACK:
                    capture_row = new_row + 1
                capture_position = str(capture_row) + capture_column
                squares[capture_position] = None

        # If it was a Castle then move the appropriate rook
        if squares[new_position].piece_type == KING:
            #Figure out if the castle was a queen side or king side
            if new_position[1] == "c":
                if squares[new_position].color == WHITE:
                    current_rook_position = "1a"
                    new_rook_position = "1d"
                elif squares[new_position].color == BLACK:
                    current_rook_position = "8a"
                    new_rook_position = "8d"
                rook_piece_copy = squares[current_rook_position].piece_type
                rook_color_copy = squares[current_rook_position].color
                squares[current_rook_position] = None
                add_piece(rook_piece_copy, rook_color_copy, new_rook_position)
            elif new_position[1] == "g":
                if squares[new_position].color == WHITE:
                    current_rook_position = "1h"
                    new_rook_position = "1f"
                elif squares[new_position].color == BLACK:
                    current_rook_position = "8h"
                    new_rook_position = "8f"
                rook_piece_copy = squares[current_rook_position].piece_type
                rook_color_copy = squares[current_rook_position].color
                squares[current_rook_position] = None
                add_piece(rook_piece_copy, rook_color_copy, new_rook_position)

    # Set the last moved piece
    global last_moved_piece
    last_moved_piece = new_position

    # See if the move was a pawn jumping
    if squares[new_position].piece_type == PAWN:
        global last_move_was_pawn_jump
        if abs(int(current_position[0]) - int(new_position[0])) == 2:
            last_move_was_pawn_jump = new_position
        else:
            last_move_was_pawn_jump = None
    else:
        last_move_was_pawn_jump = None

    # See if the piece has previously been moved and set flag
    if not squares[new_position].has_been_moved:
        squares[new_position].has_been_moved = True

def add_piece(piece_type, piece_color, position):
    """Creates the correct type of chess piece based on the inputs"""
    # First, make sure the position is empty
    try:
        assert not squares[position], """There's already a piece at that
                                        position"""
    except AssertionError as error:
        logging.error(error)
        raise

    # Different piece types
    if piece_type == BISHOP:
        squares[position] = Bishop(piece_color)
    elif piece_type == KING:
        squares[position] = King(piece_color)
    elif piece_type == KNIGHT:
        squares[position] = Knight(piece_color)
    elif piece_type == PAWN:
        squares[position] = Pawn(piece_color)
    elif piece_type == QUEEN:
        squares[position] = Queen(piece_color)
    elif piece_type == ROOK:
        squares[position] = Rook(piece_color)

def promotion_back_end(chosen_piece, piece_position):
    """Completes the back end managing after a pawn promotion"""
    # First, make sure there's a piece at the position
    try:
        assert squares[piece_position], "There's no piece at that position"
    except AssertionError as error:
        logging.error(error)
        raise

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

# Determines the piece type and calls the correct potential move function
def check_possible_moves(current_position):
    """Checks possible moves based on the piece located at the
    passed position"""
    # First, make sure there's a piece at the passed position
    try:
        assert squares[current_position], "There's no piece at that position"
    except AssertionError as error:
        logging.error(error)
        raise

    # Then, get the possible moves
    logging.debug("Returning possible moves and captures")
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

# Board Positions Dictionary (should move to a separate file at some point)
bP = {
    "1a": (25, 725),
    "2a": (25, 625),
    "3a": (25, 525),
    "4a": (25, 425),
    "5a": (25, 325),
    "6a": (25, 225),
    "7a": (25, 125),
    "8a": (25, 25),
    "1b": (125, 725),
    "2b": (125, 625),
    "3b": (125, 525),
    "4b": (125, 425),
    "5b": (125, 325),
    "6b": (125, 225),
    "7b": (125, 125),
    "8b": (125, 25),
    "1c": (225, 725),
    "2c": (225, 625),
    "3c": (225, 525),
    "4c": (225, 425),
    "5c": (225, 325),
    "6c": (225, 225),
    "7c": (225, 125),
    "8c": (225, 25),
    "1d": (325, 725),
    "2d": (325, 625),
    "3d": (325, 525),
    "4d": (325, 425),
    "5d": (325, 325),
    "6d": (325, 225),
    "7d": (325, 125),
    "8d": (325, 25),
    "1e": (425, 725),
    "2e": (425, 625),
    "3e": (425, 525),
    "4e": (425, 425),
    "5e": (425, 325),
    "6e": (425, 225),
    "7e": (425, 125),
    "8e": (425, 25),
    "1f": (525, 725),
    "2f": (525, 625),
    "3f": (525, 525),
    "4f": (525, 425),
    "5f": (525, 325),
    "6f": (525, 225),
    "7f": (525, 125),
    "8f": (525, 25),
    "1g": (625, 725),
    "2g": (625, 625),
    "3g": (625, 525),
    "4g": (625, 425),
    "5g": (625, 325),
    "6g": (625, 225),
    "7g": (625, 125),
    "8g": (625, 25),
    "1h": (725, 725),
    "2h": (725, 625),
    "3h": (725, 525),
    "4h": (725, 425),
    "5h": (725, 325),
    "6h": (725, 225),
    "7h": (725, 125),
    "8h": (725, 25)
}

# Displays the board and pieces
def display_board():
    """Displays the chess board and all the pieces"""
    create_checkerboard()

    # Add all the pieces
    logging.debug("Adding the chess pieces to the board")
    for row in rows:
        for column in columns:
            position = str(row) + column
            if squares[position]:
                if turn_color == WHITE:
                    if squares[position].color == WHITE:
                        create_piece_button(position, squares[position].color)
                    elif squares[position].color == BLACK:
                        create_piece_label(position, squares[position].color)
                elif turn_color == BLACK:
                    if squares[position].color == WHITE:
                        create_piece_label(position, squares[position].color)
                    elif squares[position].color == BLACK:
                        create_piece_button(position, squares[position].color)

# Display potential moves
def display_possible_moves(current_position):
    """Displays all possible moves for the piece in a given position"""
    # Display the possible moves
    global previous_position_shown
    # Show potential moves for a given square
    if current_position != previous_position_shown:
        logging.info("Displaying possible moves for the %s %s at position %s" %
                     (squares[current_position].color,
                      piece_names[squares[current_position].piece_type],
                      current_position))
        # Get an array of possible moves, special moves, and captures
        [possible_moves, possible_special_moves, possible_captures] = \
        check_possible_moves(current_position)

        create_checkerboard()

        # Now add the pieces and potential moves
        for row in rows:
            for column in columns:
                position = str(row) + column
                if position in possible_captures:
                    create_capture_button(current_position, position, "Red")
                elif squares[position]:
                    if turn_color == WHITE:
                        if squares[position].color == WHITE:
                            create_piece_button(position,
                                                squares[position].color)
                        elif squares[position].color == BLACK:
                            create_piece_label(position,
                                               squares[position].color)
                    elif turn_color == BLACK:
                        if squares[position].color == WHITE:
                            create_piece_label(position,
                                               squares[position].color)
                        elif squares[position].color == BLACK:
                            create_piece_button(position,
                                                squares[position].color)
                elif (position in possible_moves or position in
                      possible_special_moves):
                    create_move_button(current_position, position, "Blue")
        previous_position_shown = current_position

    # Stop showing the potential moves for a given square
    elif current_position == previous_position_shown:
        logging.debug("Removing the potential moves from the board")
        display_board()
        previous_position_shown = None

# Moves the piece
def move_the_piece(current_position, new_position):
    """Moves the chess piece in the back end of the program"""
    # Move the piece in the back end
    move_piece(current_position, new_position)

    # Change the turn color
    global turn_color
    if turn_color == WHITE:
        turn_color = BLACK
    elif turn_color == BLACK:
        turn_color = WHITE

    reset_display()

def reset_display():
    """Resets the turn display and checks if the game is over"""
    # Make sure the game isn't over
    if not game_over:
        logging.debug("The game is still going on. Resetting the turn display")
        # Re-display the board
        display_board()

        global turn_frame
        # See if the player is in check
        if check_for_check():
            #Create the check turn frame
            turn_frame.destroy()
            turn_frame = Frame(overall_turn_frame, width=250, height=100)
            turn_frame.pack()
            turn_text = "Careful, " + turn_color +", you're in check!"
            if turn_color == WHITE:
                turn_label = Label(overall_turn_frame, text=turn_text,
                                   bg="red", fg="white")
                turn_label.place(x=0, y=0, height=100, width=250)
            elif turn_color == BLACK:
                turn_label = Label(overall_turn_frame, text=turn_text,
                                   bg="red", fg="black")
                turn_label.place(x=0, y=0, height=100, width=250)
        else:
            #Change the move turn frame
            turn_frame.destroy()
            turn_frame = Frame(overall_turn_frame, width=250, height=100)
            turn_frame.pack()
            turn_text = turn_color+", it is your turn!"
            if turn_color == WHITE:
                turn_label = Label(overall_turn_frame, text=turn_text,
                                   bg="white", fg="black")
                turn_label.place(x=0, y=0, height=100, width=250)
            elif turn_color == BLACK:
                turn_label = Label(overall_turn_frame, text=turn_text,
                                   bg="black", fg="white")
                turn_label.place(x=0, y=0, height=100, width=250)

    # If the game is over, call the game over display function
    else:
        logging.info("The game is now over. Thank you for playing :)")
        show_game_over()

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
    reset_display()

def show_game_over():
    """Changes the displays if the game is over"""
    logging.debug("Game is over. Beginning final clean up steps")
    global turn_frame
    winning_color = squares[last_moved_piece].color
    game_over_text = "Game over! " + winning_color + " wins!"

    # Change the move turn frame and turn all buttons to labels
    turn_frame.destroy()
    turn_frame = Frame(overall_turn_frame, width=250, height=100)
    turn_frame.pack()
    turn_label = Label(overall_turn_frame, text=game_over_text,
                       bg="orange", fg="black")
    turn_label.place(x=0, y=0, height=100, width=250)

    create_checkerboard()

    # Add the pieces but only with lables instead of buttons
    for row in rows:
        for column in columns:
            position = str(row) + column
            if squares[position]:
                create_piece_label(position, squares[position].color)


def create_piece_label(position, label_color):
    """Creates the chess piece labels"""
    logging.debug("Creating a %s %s label at position %s" %
                  (label_color,
                   piece_names[squares[position].piece_type],
                   position))
    label = Label(temp_frame, text=squares[position].piece_type,
                  bg=label_color, fg=text_color[label_color])
    label.place(x=bP[position][0], y=bP[position][1], height=50, width=50)

def create_piece_button(position, button_color):
    """Creates the chess piece buttons"""
    logging.debug("Creating a %s %s button at position %s" %
                  (button_color,
                   piece_names[squares[position].piece_type],
                   position))
    button = Button(temp_frame, text=squares[position].piece_type,
                    bg=button_color, fg=text_color[button_color])
    button['command'] = lambda arg1=position: display_possible_moves(arg1)
    button.place(x=bP[position][0], y=bP[position][1], height=50, width=50)

def create_capture_button(current_position, position, button_color):
    """Creates the red potential capture buttons"""
    logging.debug("Creating a potential capture button at position %s" %
                  (position))
    button = Button(temp_frame, text=squares[position].piece_type,
                    bg=button_color, fg=text_color[button_color])
    button['command'] = lambda arg1=current_position, \
                        arg2=position: move_the_piece(arg1, arg2)
    button.place(x=bP[position][0], y=bP[position][1], height=50, width=50)

def create_move_button(current_position, position, button_color):
    """Creates the blue potential move buttons"""
    logging.debug("Creating a potential move button at position %s" %
                  (position))
    button = Button(temp_frame, text="??", bg=button_color,
                    fg=text_color[button_color])
    button['command'] = lambda arg1=current_position, \
                        arg2=position: move_the_piece(arg1, arg2)
    button.place(x=bP[position][0], y=bP[position][1], height=50, width=50)

def create_checkerboard():
    """Creates the chess checkboard without any pieces"""
    # Cleanup the previous board
    global temp_frame
    temp_frame.destroy()
    temp_frame = Frame(overall_frame, width=800, height=800)
    temp_frame.pack()

    # Create the checkerboard
    logging.debug("Creating the checkerboard")
    x_position = (0, 100, 200, 300, 400, 500, 600, 700)
    y_position = (0, 100, 200, 300, 400, 500, 600, 700)
    for i in y_position:
        test_num_y = i/100
        if test_num_y%2 == 0:
            for j in x_position:
                test_num_x = j/100
                if test_num_x%2 == 0:
                    square = Label(temp_frame, bg="bisque2")
                    square.place(x=j, y=i, height=100, width=100)
                else:
                    square = Label(temp_frame, bg="darkgoldenrod4")
                    square.place(x=j, y=i, height=100, width=100)
        else:
            for j in x_position:
                test_num_x = j/100
                if test_num_x%2 == 0:
                    square = Label(temp_frame, bg="darkgoldenrod4")
                    square.place(x=j, y=i, height=100, width=100)
                else:
                    square = Label(temp_frame, bg="bisque2")
                    square.place(x=j, y=i, height=100, width=100)


def main():
    """Main function"""
    # Create the chess piece objects in the back end
    #for row in rows:
    #    for column in columns:
    #        square_name = str(row) + column
    #        squares[square_name] = None
    
    # Add the white pieces
    # First add the main pieces
    #for column in columns:
    #    square_name = str(1) + column
    #    if column == 'a' or column == 'h': # Rook starting points
    #        squares[square_name] = Rook(WHITE)
    #    elif column == 'b' or column == 'g': # Knight starting points
    #        squares[square_name] = Knight(WHITE)
    #    elif column == 'c' or column == 'f': # Bishop starting points
    #        squares[square_name] = Bishop(WHITE)
    #    elif column == 'd': # Queen starting point
    #        squares[square_name] = Queen(WHITE)
    #    elif column == 'e': # King starting point
    #        squares[square_name] = King(WHITE)
    
    # Then add the pawns
    #for column in columns:
    #    square_name = str(2) + column
    #    squares[square_name] = Pawn(WHITE)
    
    
    # Add the black pieces
    # First add the main pieces
    #for column in columns:
    #    square_name = str(8) + column
    #    if column == 'a' or column == 'h': # Rook starting points
    #        squares[square_name] = Rook(BLACK)
    #    elif column == 'b' or column == 'g': # Knight starting points
    #        squares[square_name] = Knight(BLACK)
    #    elif column == 'c' or column == 'f': # Bishop starting points
    #        squares[square_name] = Bishop(BLACK)
    #    elif column == 'd': # Queen starting point
    #        squares[square_name] = Queen(BLACK)
    #    elif column == 'e': # King starting point
    #        squares[square_name] = King(BLACK)
    
    # Then add the pawns
    #for column in columns:
    #    square_name = str(7) + column
    #    squares[square_name] = Pawn(BLACK)


    # Create front end global variables
    global temp_frame
    global turn_frame
    global overall_frame
    global overall_turn_frame
    global previous_position_shown
    global turn_color
    global game_over
    global ws
    global hs
    previous_position_shown = None
    turn_color = WHITE
    game_over = False

    # Start up logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s : %(funcName)s() - %(message)s',
        level=logging.INFO)
    logging.info("Starting the game and the logger")

    # Create the overall shape
    #board = Tk()
    #w1 = 800
    #h1 = 800
    #ws = board.winfo_screenwidth()
    #hs = board.winfo_screenheight()
    #x1 = ws/3 - w1/2
    #y1 = hs*0.45 - h1/2
    #board.geometry('%dx%d+%d+%d' % (w1, h1, x1, y1))
    #board.title("Chess Board")
    #overall_frame = Frame(board, width=w1, height=h1)
    #overall_frame.pack()
    #temp_frame = Frame(overall_frame, width=w1, height=h1)
    #temp_frame.pack()

    # Create the text box that displays whose turn it is
    #player_turn = Tk()
    #w2 = 250
    #h2 = 100
    #x2 = 2*ws/3 - w2/2
    #y2 = hs*0.45 - h2/2
    #player_turn.geometry('%dx%d+%d+%d' % (w2, h2, x2, y2))
    #overall_turn_frame = Frame(player_turn, width=w2, height=h2)
    #overall_turn_frame.pack()
    #turn_frame = Frame(overall_turn_frame, width=w2, height=h2)
    #turn_frame.pack()
    #turn_label = Label(overall_turn_frame, text="White, it is your turn!",
    #                   bg="white", fg="black")
    #turn_label.place(x=0, y=0, height=100, width=250)

    # Start the game
    #display_board()

    # Keep the overall board frame always displayed
    #board.mainloop()
    
    board = BoardDisplay()
    board.root.mainloop()

    # Close the logger
    logging.info("Ending the game and shutting down the logger")
    logging.shutdown()

# Making some back end information globally accesible by placing it in __main__
# Back end variable definitions
columns = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
rows = (1, 2, 3, 4, 5, 6, 7, 8)
squares = {}
WHITE = "White"
BLACK = "Black"
BISHOP = "B"
KING = "K"
KNIGHT = "k"
PAWN = "P"
QUEEN = "Q"
ROOK = "R"
global last_moved_piece
last_moved_piece = None
global last_move_was_pawn_jump
last_move_was_pawn_jump = None

# This keeps the whole program from running when imported as a module
if __name__ == "__main__":
    main()
