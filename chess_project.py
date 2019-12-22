"""
Chess!

Created on Fri Nov 30 19:02:32 2018

@author: danielb
"""

import logging
from game import Game

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
