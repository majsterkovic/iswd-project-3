import random

import numpy as np
from player import Player


class SimplePlayer(Player):
    def __init__(self, name, p=0.3):
        super().__init__(name)
        self.p = p


    ### player's simple strategy
    def putCard(self, declared_card):
        
        ### check if must draw
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"
        
        card = min(self.cards, key=lambda x: x[0])
        declaration = (card[0], card[1])
        if declared_card is not None:
            min_val = declared_card[0]
            if card[0] < min_val: declaration = (min(min_val + 1, 14), declaration[1])
        return card, declaration
    
    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards: return True
        return np.random.choice([True, False], p=[self.p, 1-self.p])
