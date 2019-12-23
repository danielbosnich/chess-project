"""
Created on Sun Dec 22 16:35:26 2019

@author: danielb
"""

import logging
from tkinter import Tk, Toplevel, Button, Label

WHITE = 'White'
BLACK = 'Black'
BISHOP = 'Bishop'
KING = 'King'
KNIGHT = 'Knight'
PAWN = 'Pawn'
QUEEN = 'Queen'
ROOK = 'Rook'


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
        self.root = Toplevel(bg='white')
        self.root.title("Pawn Promotion!")
        display_width = 400
        display_height = 165
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
        button_size = 65
        piece_choice_text = 'Choose the piece to replace the pawn'
        piece_choice_prompt = Label(self.root, text=piece_choice_text,
                                    bg='white', fg='black',
                                    font='Helvetica 11')
        piece_choice_prompt.place(x=0, y=20, height=30, width=400)

        # Add the piece choice buttons
        queen_button = Button(self.root, text='Queen',
                              bg='green', fg='white', cursor='hand2')
        queen_button.bind('<ButtonRelease-1>',
                          lambda event, arg1=QUEEN:
                          self._set_piece_choice(event, arg1))
        queen_button.place(x=28, y=75, height=button_size, width=button_size)

        knight_button = Button(self.root, text='Knight',
                               bg='green', fg='white', cursor='hand2')
        knight_button.place(x=121, y=75, height=button_size, width=button_size)
        knight_button.bind('<ButtonRelease-1>',
                           lambda event, arg1=KNIGHT:
                           self._set_piece_choice(event, arg1))

        rook_button = Button(self.root, text='Rook',
                             bg='green', fg='white', cursor='hand2')
        rook_button.place(x=214, y=75, height=button_size, width=button_size)
        rook_button.bind('<ButtonRelease-1>',
                         lambda event, arg1=ROOK:
                         self._set_piece_choice(event, arg1))

        bishop_button = Button(self.root, text='Bishop',
                               bg='green', fg='white', cursor='hand2')
        bishop_button.place(x=307, y=75, height=button_size, width=button_size)
        bishop_button.bind('<ButtonRelease-1>',
                           lambda event, arg1=BISHOP:
                           self._set_piece_choice(event, arg1))

    def _set_piece_choice(self, event, piece_type):
        """Saves the promotion piece choice"""
        logging.debug('Button click event was %s', event)
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
        self._turn_label = Label(self.root, text="White, it's your turn!",
                                 bg="white", fg="black", font='Helvetica 11')
        self._turn_label.place(x=0, y=0, height=100, width=250)

    def update_turn_display(self, turn_color, in_check=False):
        """Toggles the turn display"""
        if not in_check:
            message_text = turn_color + ", it's your turn!"
            if turn_color == WHITE:
                display_bg = 'white'
                display_fg = 'black'
            else:
                display_bg = 'black'
                display_fg = 'white'
        else:
            message_text = "Careful " + turn_color + " you're in check!"
            display_bg = 'red'
            display_fg = 'white'

        self._turn_label.configure(text=message_text,
                                   bg=display_bg, fg=display_fg)

    def show_game_over_display(self, winner):
        """Updates the display to show the game over text"""
        game_over_text = "Game over! " + winner + " wins!"
        self._turn_label.configure(text=game_over_text,
                                   bg='orange', fg='black')
