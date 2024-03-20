import random
from enum import Enum
from collections import namedtuple
import numpy as np
import sys


# Wheel Setup
wheelValues = [20, 1, 3, 1, 5, 1, 3, 1, 10, 1, 3, 1, 5, 1, 5, 3, 1, 10, 1, 3, 1, 5, 1, 3, 1]
bettingValues = [0, 0, 0, 0, 0]
payouts = {1: 2, 3: 4, 5: 6, 10: 11, 20: 21}
outcomes = list(payouts.keys())
balance = 10

def playGame():
    global bettingValues, balance
    while balance > 0:
        print('Starting Balance:', balance)
        bettingValues, balance = betting_inputs(bettingValues, balance)
        profit = wheelPayouts(bettingValues)
        balance += profit
        print('New Balance:', balance)
    print("Game Over. You've run out of balance.")




def betting_inputs(betting_values, balance):
    bet_options = [1, 3, 5, 10, 20]
    for index, option in enumerate(bet_options):
        while True:  # Keep asking until a valid bet is made
            try:
                print(f'Bet on {option}: ')
                bet_input = int(input())  # Convert input to integer
                if 0 <= bet_input <= balance:  # Check if the bet is non-negative and within the balance
                    betting_values[index] = bet_input
                    balance -= bet_input  # Update balance
                    break  # Exit the loop if a valid bet is made
                else:
                    print("Invalid bet. Please enter a value that is within your balance and non-negative.")
            except ValueError:  # Handle non-integer inputs
                print("Please enter a valid integer.")
    return betting_values, balance  # Return updated betting values and balance


    
    


def spinWheel():
    randomSpin = random.randint(0,24)
    print('Wheel Landed On:', wheelValues[randomSpin])
    return(wheelValues[randomSpin])


def wheelPayouts(bettingValues):
    wheelValue = spinWheel()
    winnings = 0
    if wheelValue in outcomes:
        payoutIndex = outcomes.index(wheelValue)
        winnings = bettingValues[payoutIndex] * payouts[wheelValue]
        print(f'You won: {winnings}')
    else:
        print('whomp whomp')
    return winnings


if __name__ == "__main__":
    playGame()




    




