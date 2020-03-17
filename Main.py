import numpy as np
import random

def gameTurn(layout, circle, square, dice):
    """Inputs :
    layout : vector (numpy.ndarray) representing the layout of the game
        layout[i] =     0 if it is an ordinary square
                        1 if it is a “restart” trap (go back to square 1)
                        2 if it is a “penalty” trap (go back 3 steps)
                        3 if it is a “prison” trap (skip next turn)
                        4 if it is a “mystery” trap (random effect among the three previous)
    circle : boolean variable.
        circle =        True if the player must land exactly on the finish square to win
                        False if the player still wins by overstepping the final square
    square : integer variable [1-15].
        square =        actual position on the board
    dice : integer variable [1-2]
        dice =          1: use the "security" dice
                        2: use the "normal" dice

    Output : [new_square, skip_next]
        new_square:     (int) new position after one game step,
                        using the dice and starting at the square given as inputs
        skip_next:           (bool) True if step on prison trap
    """

    skip_next = False

    # -- Throw the dice
    if dice == 1:
        step = random.randint(0,1)
    else:
        step = random.randint(0,2)

    # -- Take the step
    if step != 0:
        if square == 3:
            lane = random.randint(0,1) # (0: slow lane, 1: fast lane)
            square += (7*lane + step)
        elif square == 10:
            square = 14 + step
        elif (square == 9 and step == 2):
            square = 15
        else:
            square += step

    if (square == 16 and circle == True): # in case of circular plate
        square = 1

    # -- Triggers
    if (dice == 1 and square != 16):
        if layout[square-1] == 4: # take random trap
            trap = random.randint(1,3)
        else:
            trap = layout[square-1]

        if trap == 1: # go back to square 1
            square = 1
        elif trap == 2: # go back 3 steps
            if (square == 11 or square == 12 or suqre == 13):
                square -= (7 + 3)
            elif (square == 2 or square == 3): # IF can not go back 3 steps
                square = 1
            else:
                square -= 3
        elif trap == 3:
            skip_next = True

    return [square,skip_next]

def playGame(layout, circle, policy):
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
    policy : vector (numpy.ndarray) representing the dice to choose at each square
        policy[i] = 1: use the "security" dice
                    2: use the "normal" dice
    """
    print("Start of the game at square 1")

    square = 1
    turn = 1
    skip_next = False

    while (square < 15):
        if skip_next == True:
            print("Turn "+str(turn)+": you are in the prison")
            skip_next = False
        else:
            [square,skip_next] = gameTurn(layout, circle, square, policy[square-1])
            print("Turn "+str(turn)+": you are now on square "+str(square))
        turn += 1

    print("End of the game")

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

    layout = np.array([0,0,0,0,0,0,3,0,0,0,0,2,1,0,0])
    circle = False

    # test basic strategies
    policy_1 = np.ones((15,1))
    policy_2 = 2*np.ones((15,1))

    playGame(layout,circle,policy_1)


if __name__ == "__main__":
    main()
