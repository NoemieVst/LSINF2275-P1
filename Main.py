import numpy as np
import random

import matplotlib.pyplot as plt


# we start our board at square 0 and the winning square is 14
next_state = [[1], [2], [3,10], [4], [5], [6], [7], [8], [9], [14], [11], [12], [13], [14], [14]]
next_state2 = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [14], [11], [12], [13], [14], [14]]
next_state_circle = [[1], [2], [3,10], [4], [5], [6], [7], [8], [9], [14], [11], [12], [13], [14], [0]]
next_state_circle2 = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [14], [11], [12], [13], [14], [0]]
three_backwards = [ 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 10]
end = 14

# For the tests
# next_state = [[1,3], [2], [4], [4], [4]]
# next_state2 = [[1], [2], [4], [4], [4]]
# next_state_circle = [[1,3], [2], [4], [4], [0]]
# next_state_circle2 = [[1], [2], [4], [4], [0]]
# three_backwards = [0,0,0,0]
# end = 4

# next_state = [[1], [2], [3], [4], [5], [5]]
# next_state2 = [[1], [2], [3], [4], [5], [5]]
# next_state_circle = [[1], [2], [3], [4], [5], [0]]
# next_state_circle2 = [[1], [2], [3], [4], [5], [0]]
# three_backwards = [0,0,0,0,1]
# end = 5


Expec_init = np.zeros(end)

Expec = np.full(end, np.inf)
Dice = np.full(end, np.inf)


class Strategy():
    def __init__(self, name, random, layout, circle, policy=[]):
        self.name = name
        self.random = random # random=True: play without a policy, using random choices
        self.layout = layout
        self.circle = circle
        self.policy = policy # not needed IF random=True

        self.costs = [None]*14 # number of turns left for each case
        self.average_costs = [None]*14 # average number of turns left for each case
        for case in range(14):
            self.costs[case] = list()

        self.turns = list() # number of turns for each simulated game

    def run_experiments(self, nb_times):
        for i in range(nb_times):
            self.play_game()

        for case in range(14):
            if len(self.costs[case]) != 0:
                self.average_costs[case] = sum(self.costs[case]) / len(self.costs[case])

    def play_game(self):
        # -- play
        turns_numbers = [None]*14
        for case in range(14):
            turns_numbers[case] = list()

        square = 1
        theorical_suqare = 1
        turn = 1
        skip_next = False

        while (square < 15):
            turns_numbers[theorical_suqare-1].append(turn)
            if skip_next == True:
                skip_next = False
            else:
                if self.random == False:
                    [square,skip_next,theorical_suqare] = gameTurn(self.layout, self.circle, square, self.policy[square-1])
                else:
                    [square,skip_next,theorical_suqare] = gameTurn(self.layout, self.circle, square, random.randint(1,2))
            turn += 1

        # -- save data
        self.turns.append(turn) # append the total number of turns of the actual game

        for case in range(14):
            for val in turns_numbers[case]:
                self.costs[case].append(turn-val)

class Simulation():
    def __init__(self, layout_name, layout, circle):
        """
        Run simulations with simulate()
        Then check the results with print_results() or plot_results()
        """
        self.layout_name = layout_name # name of the layout, will be used for the plots
        self.simu_dice1 = Strategy("Dice 1", False, layout, circle, np.ones((15,1)))
        self.simu_dice2 = Strategy("Dice 2", False, layout, circle, 2*np.ones((15,1)))
        self.simu_random = Strategy("Random", True, layout, circle)
        [expec,dice] = markovDecision(layout, circle)
        self.simu_VI = Strategy("Value Iteration", False, layout, circle, dice)
        print("Theorical costs for "+self.simu_VI.name+" are "+str(expec)+"\n")

        self.nb_times = 0

    def simulate(self, nb_times):
        self.simu_dice1.run_experiments(nb_times)
        self.simu_dice2.run_experiments(nb_times)
        self.simu_random.run_experiments(nb_times)
        self.simu_VI.run_experiments(nb_times)

        self.nb_times = nb_times

    def print_results(self):
        print("Results for "+str(self.nb_times)+" simulations: \n")
        print("Average costs for "+self.simu_dice1.name+" are "+str(self.simu_dice1.average_costs)+"\n")
        print("Average costs for "+self.simu_dice2.name+" are "+str(self.simu_dice2.average_costs)+"\n")
        print("Average costs for "+self.simu_random.name+" are "+str(self.simu_random.average_costs)+"\n")
        print("Average costs for "+self.simu_VI.name+" are "+str(self.simu_VI.average_costs)+"\n")

    def plot_results(self):
        # -- Box plot of the average number of turns for each game
        data = [self.simu_dice1.turns, self.simu_dice2.turns, self.simu_random.turns, self.simu_VI.turns]
        fig, ax = plt.subplots()
        ax.set_title('Boxplot of the number of turns for different strategies, using '+self.layout_name)
        ax.boxplot(data,showfliers=False)
        ax.set_ylabel('Number of turns')
        ax.set_xticklabels([self.simu_dice1.name, self.simu_dice2.name, self.simu_random.name, self.simu_VI.name])
        plt.show()

        # -- Plot of the average costs found
        X = range(1,15)
        plt.plot(X,self.simu_dice1.average_costs)
        plt.plot(X,self.simu_dice2.average_costs)
        plt.plot(X,self.simu_random.average_costs)
        plt.plot(X,self.simu_VI.average_costs)
        plt.legend((self.simu_dice1.name, self.simu_dice2.name, self.simu_random.name, self.simu_VI.name),
           loc='upper right')
        axes = plt.gca()
        axes.xaxis.set_ticks(X)
        plt.title('Empirical average costs for different strategies, using '+self.layout_name)
        plt.xlabel('Square')
        plt.ylabel('Average cost')
        plt.show()

        # -- Comparaison between theorical and experimental costs for VI (Value Iteration)
        # -> with a table in the report

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

    Output : [new_square, skip_next, theorical_square]
        new_square:     (int) new position after one game step,
                        using the dice and starting at the square given as inputs
        skip_next:      (bool) True if step on prison trap
        theorical_square:(int) new position before going on the trap
                        (is the same as new_square if there is no trap)
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

    theorical_square = square

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

    return [square,skip_next,theorical_square]

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
            [square,skip_next,theorical_square] = gameTurn(layout, circle, square, policy[square-1])
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
            numbers2 += next_state_circle2[n]
        numbers = numbers2
    elif step == 2 and not circle:
        numbers2 = []
        for n in numbers:
            numbers2 += next_state2[n]
        numbers = numbers2

    if dice == 1:  # security dice
        return [[n, False] for n in numbers]

    else:  # normal dice
        ret = []
        for n in numbers:
            if layout[n] == 1:
                # Expec[n] = 0 if Expec_init[0] == np.inf else Expec_init[0]
                ret.append([0, False])  # back to the first square
            elif layout[n] == 2:
                #Expec[n] = 0 if Expec_init[three_backwards[n]] == np.inf else Expec_init[three_backwards[n]]
                ret.append([three_backwards[n], False])  # 3 squares backwards or 1
            elif layout[n] == 3:
                ret.append([n, True])  # wait one turn before playing again
            elif layout[n] == 4:
                rand = random.randint(1, 3)  # randomly applies the effect of 1 of the 3 previous traps, equal proba
                if rand == 1:
                    ret.append([0, False])
                elif rand == 2:
                    ret.append([three_backwards[n], False])
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

    return sorted(n_states, key=lambda x: x[1], reverse=True)
    #return n_states


def expected_cost(layout, current_state, dices, pass_turn, count, circle):
    """ Input :  - dices [1], [2] or [1,2] (1: security dice, 2: normal dice)
                - pass_turn : True if the player has to pass the next turn (trap3 prison), False otherwise
                - count : count of recusrive call for a given current_state
                - circle : True of board designed as a circle, False otherwise
        - add value of the expected cost in Expec[current_state] if not already done
        - add value of the dice in Dice[current_state] if not already done
        Output: - expected cost for the square "current_stare" """

    #print("curr : ", current_state, Expec)

    if current_state == end:  # V(d) = 0
        return 0

    if pass_turn:
        return 1 + expected_cost(layout, current_state, dices, False, count+1, circle)

    if count > 100:  # we stop the infinite recursive calls
        Expec[current_state] = Expec_init[current_state]
        return Expec_init[current_state]


    if Expec[current_state] != np.inf:
        return Expec[current_state]


    if len(dices) == 2:  # the two dices are available

        exp_cost1 = 1  # c(a|k)
        for [p, k_prim, next_pass_turn] in next_states(layout, current_state, 1, circle):
            if k_prim == current_state:
                exp_cost1 += p * expected_cost(layout, k_prim, dices, next_pass_turn, count + 1, circle)
            else:
                exp_cost1 += p * expected_cost(layout, k_prim, dices, next_pass_turn, 0, circle)

        exp_cost2 = 1
        for [p, k_prim, next_pass_turn] in next_states(layout, current_state, 2, circle):
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
    expected_cost(layout, current_state=0, dices=[1,2], pass_turn=False, count=0, circle=circle)
    for j in range(30):
        for i in range(len(Expec_init)):
            Expec_init[i] = Expec[i]
            Expec[i] = np.inf

        expected_cost(layout, current_state=0, dices=[1,2], pass_turn=False, count=0, circle=circle)
        if len(np.where(abs(np.subtract(Expec_init, Expec)) > 0.00001)[0]) < 1:
            break
    return [Expec, Dice]

def main():
    layout_zeros = np.zeros((15,1))
    layout_basic1 = np.array([0,1,0,0,0,0,0,0,0,0,0,0,0,0,0])
    layout_basic2 = np.array([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0])
    layout_basic3 = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    layout_test = np.array([0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0])
    circle = True


    simu = True
    markov = False

    if simu: # run simulations
        simu = Simulation("no traps", layout_zeros, circle)
        simu.simulate(1000)
        simu.print_results()
        simu.plot_results()

    if markov: # test Markov
        [ret1, ret2] = markovDecision(layout_zeros, circle)
        print("Expected costs (Markov process) : ", ret1)
        #print("Expected costs (Markov process) : ", [round(x, 5) for x in ret1])
        #print(ret2)


    # test basic strategies
    #policy_1 = np.ones((15,1))
    #policy_2 = 2*np.ones((15,1))

    #playGame(layout,circle,policy_1)


def test(layout, circle, dices):

    expected_cost(layout, current_state=0, dices=[1, 2], pass_turn=False, count=0, circle=circle)
    for j in range(30):
        for i in range(len(Expec_init)):
            Expec_init[i] = Expec[i]
            Expec[i] = np.inf

        expected_cost(layout, current_state=0, dices=[1, 2], pass_turn=False, count=0, circle=circle)
        if len(np.where(abs(np.subtract(Expec_init, Expec)) > 0.00001)[0]) < 1:
            break
    return [Expec, Dice]


if __name__ == "__main__":
    main()
