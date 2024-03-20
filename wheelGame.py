import random
from enum import Enum
from collections import namedtuple
import numpy as np
import sys


# Wheel Setup
wheelValues = [20, 1, 3, 1, 5, 1, 3, 1, 10, 1, 3, 1, 5, 1, 5, 3, 1, 10, 1, 3, 1, 5, 1, 3, 1]
payouts = {1: 2, 3: 4, 5: 6, 10: 11, 20: 21}
outcomes = list(payouts.keys())
balance = 10


class WheelGameAI:
    def __init__(self):
        self.balance = 10
        self.last_outcome = None  # Initialize the last_outcome attribute
        self.payouts = {1: 2, 3: 4, 5: 6, 10: 11, 20: 21}
        self.outcomes = list(payouts.keys())
        self.isOver = False
        self.zero_bet_count = 0
        self.bet_count = 0


    # spin the wheel
        
    def wheelSpin(self):
        wheelLand = random.choice(wheelValues)
        return wheelLand
    
    # bets should look like something lik this [0.00,1.00,2.00,0.00,3.00]
    def placeBets(self, bets):
        self.bet_count += 1

        total_bet = sum(bets)
        if total_bet > self.balance:
            print('invalid bet')
            print('SETTING TO TRUE 1')
            return self.balance, None, -10, True
        
        # Spin The Wheel
        outcome = self.wheelSpin()

        # Map Outcome to Index in Bets
        index = self.outcomes.index(outcome)

        #calculate earnings
        earnings = bets[index] * self.payouts[outcome]

        # calculate net gain
        profit = earnings - total_bet

        reward = profit ** 2

        self.balance += earnings - total_bet

        self.last_outcome = outcome

        # Check if the bets are all zero for five consecutive spins
        if all(b == 0 for b in bets):
            self.zero_bet_count += 1
            if self.zero_bet_count >= 5:
                print('SETTING TO TRUE 2')
                self.isOver = True  # Reset the counter
                print("BAD AI")
                return self.balance, None, -100000, True
        else:
            self.zero_bet_count = 0

        if self.balance <= 0:
            print('SETTING TO TRUE 3')
            self.isOver = True
            print("ON HO")
            return self.balance, self.last_outcome, reward, self.isOver
        elif self.bet_count >= 10:
            print('SETTING TO TRUE 4')
            self.isOver = True
            print("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO YOU DID IT YIPEEEEEEEE")
            return self.balance, self.last_outcome, reward + 40, self.isOver
        

        print("??????")
        print(self.isOver)
        return self.balance, self.last_outcome, reward, self.isOver





    def reset(self):
        print('RESET')
        # Reset game state to start a new game
        self.balance = 10  # Reset balance to initial value
        self.last_outcome = None  # Reset the last outcome
        self.bet_count = 0
        self.zero_bet_count = 0
        self.isOver = False
        # Any other state reset actions

















    




