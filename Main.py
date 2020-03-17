import numpy as np


def markovDecision(layout, circle):
    """Inputs :
    layout : vector (numpy.ndarray) representing the layout of the game
        layout[i] = 0 if it is an ordinary square
                    1 if it is a “restart” trap (go back to square 1)
                    2 if it is a “penalty” trap (go back 3 steps)
                    3 if it is a “prison” trap (skip next turn)
                    4 if it is a “mystery” trap (random effect among the three previous)
    circle : boolean variable.
        circle =    True if the player must land exactly on the finish square to win
                    False if the player still wins by overstepping the final square
    Output : [Expec,Dice]
        Expec =     vector (numpy.ndarray) containing the expected cost (= number of turns)
                    associated to the 14 squares of the game, excluding the finish one
        Dice =      vector (numpy.ndarray) containing the choice of the dice to use for each of
                    the 14 squares of the game (1 for “security” dice, 2 for “normal” dice), excluding
                    the finish one.

    """
    print("todo")


def main():
    print("todo")

    layout = np.array()


if __name__ == "__main__":
    main()