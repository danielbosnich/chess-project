"""
Created on Sun Dec 22 16:38:22 2019

@author: danielb
"""

from tkinter import Button
import logging
from chess_displays import BoardDisplay, PromotionDisplay, TurnDisplay
from chess_pieces import Bishop, King, Knight, Pawn, Queen, Rook
from helpful_dictionaries import tile_positions

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


class Game():
    """Class that represents a running of the game"""
    def __init__(self):
        # Instance variables
        self._display = BoardDisplay()
        self._turn_display = TurnDisplay()
        self._promotion_display = None
        self._pieces = []
        self._possible_move_buttons = []
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
        logging.debug('Button click event was %s', event)
        # Don't show moves if it's not their turn
        if piece.color != self._turn_color:
            self._clear_possible_moves()
            return

        # Show potential moves for a given square
        if piece.position != self._previous_position_shown:
            logging.info('Showing possible moves for the %s %s at %s',
                         piece.color, piece.piece_type, piece.position)
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

    def _remove_piece(self, piece):
        """Removes the passed piece"""
        logging.info('Removing the %s %s at %s',
                     piece.color, piece.piece_type, piece.position)
        piece.button.destroy()
        self._pieces.remove(piece)
        del piece

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

    def _show_game_over(self, winning_color):
        """Changes the displays if the game is over"""
        # Add the pieces but only with lables instead of buttons
        for piece in self._pieces:
            piece.disable_button(self._display.root)

        self._turn_display.show_game_over_display(winning_color)

    def _move_piece(self, event, piece, new_position):
        """Moves the chess piece to a new position and checks some conditions
        after the move"""
        logging.debug('Button click event was %s', event)
        self._clear_possible_moves()
        piece.check_potential_moves(self._return_squares())
        # Check if this is a capture
        captured_piece = None
        if new_position in piece.possible_captures:
            captured_piece = self.return_piece(new_position)
            logging.info("The %s %s at position %s will be captured!",
                         captured_piece.color,
                         captured_piece.piece_type,
                         new_position)
            # Remove the piece being captured
            self._remove_piece(captured_piece)

        # Change the moving piece's location
        logging.info("Moving the %s %s from %s to %s",
                     piece.color,
                     piece.piece_type,
                     piece.position,
                     new_position)
        piece.update_position(new_position)

        # Check if the king was captured and, if so, end the game
        if captured_piece is not None and captured_piece.piece_type == KING:
            logging.info("The %s king has just been captured. The game is over.",
                         captured_piece.color)
            self._show_game_over(piece.color)
            return

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
                    captured_piece = self.return_piece(capture_position)
                    self._remove_piece(captured_piece)

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
        self._last_moved_piece = new_position

        # See if the move was a pawn jumping
        if piece.piece_type == PAWN:
            if abs(int(piece.position[0]) - int(new_position[0])) == 2:
                self._last_move_was_pawn_jump = new_position
            else:
                self._last_move_was_pawn_jump = None
        else:
            self._last_move_was_pawn_jump = None

        # See if the piece has previously been moved and set flag
        if not piece.has_been_moved:
            piece.has_been_moved = True

        # Update the turn color flag and display
        # Pass a boolean for whether the opponent is now in check or not
        self._update_turn_color(self._check_for_check())

    def promotion(self, piece):
        """Completes pawn promotion by creating a promotion """
        self._promotion_display = PromotionDisplay()
        # Wait for the user input
        logging.info("Waiting")
        self._display.root.wait_window(self._promotion_display.root)
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
            new_piece = Bishop(piece.color, piece.position, self._display.root)
        # Remove the pawn and add the new piece
        self._remove_piece(piece)
        new_piece.button.bind('<ButtonRelease-1>',
                              lambda event, arg1=new_piece:
                              self._display_possible_moves(event, arg1))
        self._pieces.append(new_piece)

    def _update_turn_color(self, in_check):
        """Updates the turn color display and instance variable"""
        if self._turn_color == WHITE:
            self._turn_color = BLACK
        else:
            self._turn_color = WHITE
        self._turn_display.update_turn_display(self._turn_color, in_check)

    def _check_for_check(self):
        """Determines if the player is currently in check"""
        squares = self._return_squares()
        for piece in self._pieces:
            if piece.color == self._turn_color:
                piece.check_potential_moves(squares)
                for move in piece.possible_captures:
                    if squares[move].piece_type == KING:
                        logging.info("The %s %s at position %s is in check!",
                                     squares[move].color,
                                     KING,
                                     move)
                        return True
        return False
