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

Expec_init = np.zeros(end)

Expec = np.full(end, np.inf)
Dice = np.full(end, np.inf)


class Strategy():
    """Tools for simulating a given or random strategy of the
    Snakes and Ladders game and compute the costs of each square.
    """
    def __init__(self, name, random, layout, circle, policy=[]):
        """Initialise a simulation of a given strategy."""
        self.name = name                # name of the strategy, used for legends of figures
        self.random = random            # random=True: play without a policy, using random choices
        self.layout = layout
        self.circle = circle
        if random == False:             # not needed IF random=True
            self.policy = policy

        self.costs = [None]*14          # number of turns left for each case
        self.average_costs = [None]*14  # average number of turns left for each case
        for case in range(14):
            self.costs[case] = list()

        self.turns = list()             # number of turns of each simulated game

    def run_experiments(self, nb_times):
        """Launch <nb_times> simulations of the game"""
        for i in range(nb_times):
            self.play_game()

        for case in range(14):
            if len(self.costs[case]) != 0:
                self.average_costs[case] = sum(self.costs[case]) / len(self.costs[case])
            else:
                self.average_costs[case] = 0        # infinite costs are saved as "0"

    def play_game(self):
        """Play one round of the game and save each cost
        (number of turns before the end of the game)."""
        # -- initialise the game
        turns_numbers = [None]*14
        for case in range(14):
            turns_numbers[case] = list()

        square = 1
        theorical_suqare = 1
        turn = 1
        skip_next = False

        # -- play the game
        while (square < 15):
            turns_numbers[square-1].append(turn)    # add the turn to the list of turns of this case
            if skip_next == True:                   # IF the player is in prison, skip this turn
                skip_next = False
            else:
                if self.random == False:
                    [square,skip_next,theorical_suqare] = gameTurn(self.layout, self.circle, square, self.policy[square-1])
                else:
                    [square,skip_next,theorical_suqare] = gameTurn(self.layout, self.circle, square, random.randint(1,2))
            turn += 1

        # -- save the results
        self.turns.append(turn)                     # append the total number of turns of the actual game

        for case in range(14):
            for val in turns_numbers[case]:
                self.costs[case].append(turn-val)   # append each cost

class Simulation():
    """Tools for simulating multiple strategies of the Snakes and Ladders
    game and displaying or saving the results of the simulations.
    """
    def __init__(self, layout_name, layout, circle):
        """Initialise the simulations."""
        self.layout_name = layout_name                                                  # name of the layout, will be used for the plots
        self.simu_dice1 = Strategy("Dice 1", False, layout, circle, np.ones((15,1)))    # 1st strategy: use only dice 1
        self.simu_dice2 = Strategy("Dice 2", False, layout, circle, 2*np.ones((15,1)))  # 2nd strategy: use only dice 2
        self.simu_random = Strategy("Random", True, layout, circle)                     # 3rd strategy: random dices
        [expec,dice] = markovDecision(layout, circle)
        self.VI_expec = expec
        self.VI_dices = dice
        self.simu_VI = Strategy("Value Iteration", False, layout, circle, dice)         # 4th strategy: Markov optimal strategy
        self.nb_times = 0

    def simulate(self, nb_times):
        """ Run a simulation <nb_times> times"""
        self.simu_dice1.run_experiments(nb_times)
        self.simu_dice2.run_experiments(nb_times)
        self.simu_random.run_experiments(nb_times)
        self.simu_VI.run_experiments(nb_times)
        self.nb_times = nb_times # save the number of runs of the simulations

    def print_results(self):
        """Print the theorical and average costs for the Markov policy
        and the average costs for the other strategies."""
        print("Theorical costs for "+self.simu_VI.name+" are "+str(self.VI_expec)+"\n")
        print("Dices for "+self.simu_VI.name+" are "+str(self.VI_dices)+"\n")
        print("Results for "+str(self.nb_times)+" simulations: \n")
        print("Average costs for "+self.simu_dice1.name+" are "+str(self.simu_dice1.average_costs)+"\n")
        print("Average costs for "+self.simu_dice2.name+" are "+str(self.simu_dice2.average_costs)+"\n")
        print("Average costs for "+self.simu_random.name+" are "+str(self.simu_random.average_costs)+"\n")
        print("Average costs for "+self.simu_VI.name+" are "+str(self.simu_VI.average_costs)+"\n")

    def plot_results(self):
        """Plot the results of the simulations."""
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

    def export_array(self, filename):
        """Save the theorical and empirical costs in the file <filename>.csv"""
        X = range(1,15)
        Table = np.asarray([X,self.VI_expec,self.simu_VI.average_costs])
        Table.shape = (3,14)
        Table = Table.transpose()
        print(Table)
        np.savetxt(filename+".csv", Table)

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
            lane = random.randint(0,1)          # (0: slow lane, 1: fast lane)
            square += (7*lane + step)
        elif square == 10:
            square = 14 + step
        elif (square == 9 and step == 2):
            square = 15
        else:
            square += step

    if (square == 16 and circle == True):       # in case of circular plate
        square = 1

    theorical_square = square

    # -- Triggers
    if (dice == 2 and square != 16):
        if layout[square-1] == 4:               # take random trap
            trap = random.randint(1,3)
        else:
            trap = layout[square-1]

        if trap == 1:                           # go back to square 1
            square = 1
        elif trap == 2:                         # go back 3 steps
            if (square == 11 or square == 12 or square == 13):
                square -= (7 + 3)
            elif (square == 2 or square == 3):  # IF can not go back 3 steps
                square = 1
            else:
                square -= 3
        elif trap == 3:                         # go to prison
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
    """returns a list of [next_square, pass_next_turn]
    input :
        layout : vector (numpy.ndarray) representing the layout of the game
        current_state : index of the current square
        step : 0, 1 or 2, represents the number given by the dice
        dice : 1 for the security dice, 2 for the normal dice
        circle : boolean representing if the board is circular or not
    Output : list of [next_square, pass_next_turn], one for each possible next state
        next_square : index of a following square
        pass_next_turn : boolean, True if we have to skip the next turn, False otherwise"""


    # compute the next state
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

    # taking account the traps
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
    Input:
        layout : vector (numpy.ndarray) representing the layout of the game
        current_state : index of the current square
        dice : 1 for the security dice, 2 for the normal dice
        circle : boolean representing if the board is circular or not
    Output : list of [p, k_prim, pass_next_turn]
        p : p(k_prim | k, a) a
        k_prim :  index of a following square
        pass_turn : boolean, True if we have to skip the next turn, False otherwise"""
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


def expected_cost(layout, current_state, dices, pass_turn, count, circle):
    """ Input : - dices [1], [2] or [1,2] (1: security dice, 2: normal dice)
                - pass_turn : True if the player has to pass the next turn (trap3 prison), False otherwise
                - count : count of recusrive call for a given current_state
                - circle : True of board designed as a circle, False otherwise
        - add value of the expected cost in Expec[current_state]
        - add value of the dice in Dice[current_state]
    Output:
        - expected cost for the square "current_stare" """

    #print("curr : ", current_state, Expec)

    if current_state == end:  # final square
        return 0

    if pass_turn:   # we skip a turn
        return 1 + expected_cost(layout, current_state, dices, False, count+1, circle)

    if count > 100:  # we stop the infinite recursive calls
        Expec[current_state] = Expec_init[current_state]
        return Expec_init[current_state]


    if Expec[current_state] != np.inf: # We avoid to compute expected costs already computed
        return Expec[current_state]


    if len(dices) == 2:  # the two dices are available

        exp_cost1 = 1  # c(dice1|k)
        for [p, k_prim, next_pass_turn] in next_states(layout, current_state, 1, circle):
            if k_prim == current_state:
                exp_cost1 += p * expected_cost(layout, k_prim, dices, next_pass_turn, count + 1, circle)
            else:
                exp_cost1 += p * expected_cost(layout, k_prim, dices, next_pass_turn, 0, circle)

        exp_cost2 = 1 # c(dice2|k)
        for [p, k_prim, next_pass_turn] in next_states(layout, current_state, 2, circle):
            if k_prim == current_state:
                exp_cost2 += p * expected_cost(layout, k_prim, dices, next_pass_turn, count + 1, circle)
            else:
                exp_cost2 += p * expected_cost(layout, k_prim, dices, next_pass_turn, 0, circle)

        if exp_cost1 < exp_cost2: # we choose the dice with the minumum cost
            Expec[current_state] = exp_cost1
            Dice[current_state] = 1
            return exp_cost1
        else:
            Expec[current_state] = exp_cost2
            Dice[current_state] = 2
            return exp_cost2

    else:  # only one dice available (for tests)
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

    for j in range(30): # iterations to converge to a good final expected costs
        for i in range(len(Expec_init)):
            Expec_init[i] = Expec[i]
            Expec[i] = np.inf

        expected_cost(layout, current_state=0, dices=[1,2], pass_turn=False, count=0, circle=circle)
        if len(np.where(abs(np.subtract(Expec_init, Expec)) > 0.00001)[0]) < 1: # if convergence, we stop the iteration
            break
    return [Expec, Dice]

def main():
    layout_zeros = np.zeros((15,1)) # first analysis in the report
    layout_basic1 = np.array([0,1,0,0,0,0,0,0,0,0,0,0,0,0,0])
    layout_basic2 = np.array([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0])
    layout_basic3 = np.array([0,0,0,1,0,0,0,0,0,0,0,0,0,0,0])
    layout_basic4 = np.array([0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]) # 2nd analysis in the report
    layout_basic5 = np.array([0,0,0,0,0,0,0,0,0,0,1,1,1,1,0]) # 3rd analysis in the report
    layout_complex1 = np.array([0,3,3,3,3,3,3,2,3,4,3,3,3,1,0]) # 4th analysis in the report

    circle = False

    simu = True # run the simulation ?
    markov = False # run Markov Process ?

    if simu: # run simulations
        simu = Simulation("trap 1 on square 8", layout_basic4, circle)
        simu.simulate(10000)
        simu.print_results()
        #simu.export_array("cost_trap_1_case_8_False")
        #simu.plot_results()

    if markov: # test Markov
        [ret1, ret2] = markovDecision(layout_zeros, circle)
        print("Expected costs (Markov process) : ", ret1)
        print("Dices (Markov process) : ", ret2)

if __name__ == "__main__":
    main()
