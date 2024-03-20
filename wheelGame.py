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
        total_bet = sum(bets)
        if total_bet > self.balance:
            print('invalid bet')
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
                self.zero_bet_count = 0  # Reset the counter
                return self.balance, None, -100000, True
        else:
            self.zero_bet_count = 0

        if self.balance <= 0:
            self.isOver = True
            return self.balance, self.last_outcome, reward, self.isOver
        elif self.bet_count >= 10:
            bonus = reward + 4000
            self.isOver = True
            self.bet_count += 1
            print("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO YOU DID IT YIPEEEEEEEE")
            return self.balance, self.last_outcome, bonus, self.isOver
        else:
            return self.balance, self.last_outcome, reward, self.isOver





    def reset(self):
        # Reset game state to start a new game
        self.balance = 10  # Reset balance to initial value
        self.last_outcome = None  # Reset the last outcome
        self.bet_count = 0
        # Any other state reset actions

















    




