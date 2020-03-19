import numpy as np
import random


# we start our board at square 0 and the winning square is 14
#next_state = [[1], [2], [3,10], [4], [5], [6], [7], [8], [9], [14], [11], [12], [13], [14], [14]]
#next_state_circle = [[1], [2], [3,10], [4], [5], [6], [7], [8], [9], [14], [11], [12], [13], [14], [0]]
#end = 14

next_state = [[1,2], [3], [3], [3]]
next_state_circle = [[1,2], [3], [3], [0]]
end = 3

Expec = np.zeros(end)
Dice = np.zeros(end)

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
    if (dice == 2 and square != 16):
        if layout[square-1] == 4: # take random trap
            trap = random.randint(1,3)
        else:
            trap = layout[square-1]

        if trap == 1: # go back to square 1
            square = 1
        elif trap == 2: # go back 3 steps
            if (square == 11 or square == 12 or square == 13):
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


def number_next_state(layout, current_state, step, dice, circle):
    """output : list of [next_square, pass_next_turn]"""

    if step== 0:
        numbers = [current_state]
    else:
        if circle:
            numbers = next_state_circle[current_state]
        else:
            numbers = next_state[current_state]

    if step == 2 and circle:
        numbers2 = []
        for n in numbers:
            numbers2 += next_state_circle[n]
        numbers = numbers2
    elif step == 2 and not circle:
        numbers2 = []
        for n in numbers:
            numbers2 += next_state[n]
        numbers = numbers2

    if dice == 1:  # security dice
        return [[n, False] for n in numbers]

    else:  # normal dice
        ret = []
        for n in numbers:
            if layout[n] == 1:
                ret.append([1, False])  # back to the first square
            elif layout[n] == 2:
                ret.append([max(1, n - 3), False])  # 3 squares backwards or 1
            elif layout[n] == 3:
                ret.append([n, True])  # wait one turn before playing again
            elif layout[n] == 4:
                rand = random.randint(1, 3)  # randomly applies the effect of 1 of the 3 previous traps, equal proba
                if rand == 1:
                    ret.append([1, False])
                elif rand == 2:
                    ret.append([max(1, n - 3), False])
                else:
                    ret.append([n, True])
            else:
                ret.append([n, False])  # no trap

        return ret


def next_states(layout, current_state, dice, circle):
    """Return a list of [p, k_prim, pass_next_turn] for each possible next state k_prim
    where p is p(k_prim | k, a) and pass_turn is a boolean representing if we have to passe the next turn"""
    n_states = []

    if dice == 1:  # security dice
        for i in [1,0]:
            l = number_next_state(layout, current_state, i, dice, circle)
            for [k_prim, pass_next_turn] in l:
                n_states.append([0.5*(1/len(l)), k_prim, pass_next_turn])

    if dice == 2:  # normal dice
        for i in [2,1,0]:
            l = number_next_state(layout, current_state, i, dice, circle)
            for [k_prim, pass_next_turn] in l:
                n_states.append([(1/3)*(1/len(l)), k_prim, pass_next_turn])

    return n_states


def expected_cost(layout, current_state, dices, pass_turn, count, circle):
    """ Input :  - dices [1], [2] or [1,2] (1: security dice, 2: normal dice)
                - pass_turn : True if the player has to pass the next turn (trap3 prison), False otherwise
                - count : count of recusrive call for a given current_state
                - circle : True of board designed as a circle, False otherwise
        - add value of the expected cost in Expec[current_state] if not already done
        - add value of the dice in Dice[current_state] if not already done
        Output: - expected cost for the square "current_stare" """

    if count > 100:  # we stop the infinite recursive calls
        return 0

    if pass_turn:
        return [1 + expected_cost(layout, current_state, dices, False)]

    if current_state == end:  # V(d) = 0
        return 0

    #print("exp -  curr : ", current_state, ", count : ", count)

    if Expec[current_state] != 0:
        return Expec[current_state]

    if len(dices) == 2:  # the two dices are available

        exp_cost1 = 1  # c(a|k)
        for [p, k_prim, next_pass_turn] in next_states(layout, current_state, 1, circle):
            #print("curr : ", current_state, ", p :", p, ", k_prim :", k_prim, "count : ", count)
            if k_prim == current_state:
                exp_cost1 += p * expected_cost(layout, k_prim, dices, next_pass_turn, count + 1, circle)
            else:
                exp_cost1 += p * expected_cost(layout, k_prim, dices, next_pass_turn, 0, circle)

        exp_cost2 = 1
        for [p, k_prim, next_pass_turn] in next_states(layout, current_state, 2, circle):
            #print("curr : ", current_state, ", p :", p, ", k_prim :", k_prim, "count : ", count)
            if k_prim == current_state:
                exp_cost2 += p * expected_cost(layout, k_prim, dices, next_pass_turn, count + 1, circle)
            else:
                exp_cost2 += p * expected_cost(layout, k_prim, dices, next_pass_turn, 0, circle)

        if exp_cost1 < exp_cost2:
            Expec[current_state] = exp_cost1
            Dice[current_state] = 1
            return exp_cost1
        else:
            Expec[current_state] = exp_cost2
            Dice[current_state] = 2
            return exp_cost2

    else:  # only one dice available
        exp_cost = 1
        for [p, k_prim, next_pass_turn] in next_states(layout, current_state, dices[0], circle):
            #print("curr : ", current_state, ", p :", p, ", k_prim :", k_prim, "count : ", count)
            if k_prim == current_state:
                exp_cost += p * expected_cost(layout, k_prim, dices, next_pass_turn, count + 1, circle)
            else:
                exp_cost += p * expected_cost(layout, k_prim, dices, next_pass_turn, 0, circle)


        Expec[current_state] = exp_cost
        Dice[current_state] = dices[0]
        return exp_cost


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
    expected_cost(layout, 0, [2], False, 0, circle)
    return [Expec, Dice]

def main():

    layout = np.array([0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0])
    circle = False

    [ret1, ret2] = markovDecision(layout, circle)
    print(ret1, ret2)

    # test basic strategies
    #policy_1 = np.ones((15,1))
    #policy_2 = 2*np.ones((15,1))

    #playGame(layout,circle,policy_1)

def test(layout, circle, dices):
    expected_cost(layout, current_state=0, dices=dices, pass_turn=False, count=0, circle=circle)
    print(Expec, Dice)
    return [Expec, Dice]



if __name__ == "__main__":
    main()
