from unittest import TestCase

from Main import *


class Test(TestCase):
    def test_number_next_state(self, layout, current_state, step, dice, circle, true_next_state):
        pred_next_state = []
        for [n, b] in number_next_state(layout, current_state, step, dice, circle):
            pred_next_state.append(n)
        print(pred_next_state)
        self.assertEqual(pred_next_state, true_next_state)

    def test_next_states(self, layout, current_state, dice, circle, true_next_states):
        pred_next_states = next_states(layout, current_state, dice, circle)
        self.assertEqual(true_next_states, pred_next_states,)

    def text_exp_cost(self, layout, circle, dices, Expec_pred):
        [Expec, Dice] = test(layout, circle=circle, dices=dices)
        Expec = list(Expec)
        for i in range(len(Expec)):
            self.assertEqual(round(Expec_pred[i], 4), round(Expec[i], 4))

    def test_number_next_state1(self):
        layout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        current_state = 2
        step = 1
        dice = [1]
        circle = False
        self.test_number_next_state(layout, current_state, step, dice, circle, [3,10])

    def test_number_next_state2(self):
        layout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        current_state = 2
        step = 2
        dice = [2]
        circle = False
        self.test_number_next_state(layout, current_state, step, dice, circle, [4,11])

    def test_number_next_state3(self):
        layout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        current_state = 14
        step = 2
        dice = [2]
        circle = True
        self.test_number_next_state(layout, current_state, step, dice, circle, [1])

    def test_number_next_state4(self):
        layout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        current_state = 14
        step = 1
        dice = [2]
        circle = True
        self.test_number_next_state(layout, current_state, step, dice, circle, [0])

    def test_number_next_state5(self):
        layout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        current_state = 14
        step = 2
        dice = [2]
        circle = False
        self.test_number_next_state(layout, current_state, step, dice, circle, [14])

    def test_number_next_state6(self):
        layout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        current_state = 7
        step = 2
        dice = [2]
        circle = False
        self.test_number_next_state(layout, current_state, step, dice, circle, [9])


    def test_next_states1(self):
        layout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        current_state = 7
        dice = 1
        circle = False
        pred = [[0.5, 7, False], [0.5, 8, False]]
        self.test_next_states(layout,current_state, dice, circle, pred)


    def test_next_states2(self):
        layout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        current_state = 2
        dice = 1
        circle = False
        pred = [[0.5, 2, False], [0.25, 3, False], [0.25, 10, False]]
        self.test_next_states(layout,current_state, dice, circle, pred)

    def test_next_states3(self):
        layout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        current_state = 2
        dice = 2
        circle = False
        pred = [ [1/3, 2, False], [1/6, 3, False], [1/6, 10, False], [1/6, 4, False], [1/6, 11, False]]
        self.test_next_states(layout,current_state, dice, circle, pred)


    """Tests suivants avec :
        next_state = [[1,3], [2], [4], [4], [4]]
        next_state2 = [[1], [2], [4], [4], [4]]
        next_state_circle = [[1,3], [2], [4], [4], [0]]
        next_state_circle2 = [[1,3], [2], [4], [4], [0]]
        three_backwards = [0,0,0,0]
        end = 4
        """

    def test_exp_cost1(self):
        layout = [0, 0, 0, 0, 0]
        dices = [1]
        circle = False
        Expec_pred = [5, 4, 2, 2]
        self.text_exp_cost(layout, circle, dices, Expec_pred)

    def test_exp_cost2(self):
        layout = [0, 0, 0, 0, 0]
        dices = [2]
        circle = False
        Expec_pred = [2.8125, 2.25, 1.5, 1.5]
        self.text_exp_cost(layout, circle, dices, Expec_pred)

    def test_exp_cost3(self):
        layout = [0, 0, 0, 0, 0]
        dices = [2]
        circle = True
        Expec_pred = [45/11, 36/11, 39/11, 39/11]
        self.text_exp_cost(layout, circle, dices, Expec_pred)
