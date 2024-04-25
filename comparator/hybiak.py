import random

import numpy as np
from player import Player


class Hybiak(Player):

    def __init__(self, name):
        super().__init__(name)
        self.played_cards = []
        self.moves = 0

    def _find_free_color(self, value):
        colors = [0, 1, 2, 3]
        for color in colors:
            if (value, color) not in self.played_cards:
                return color
        return None

    def putCard(self, declared_card):
        self.moves += 1

        if len(self.cards) == 1 and declared_card and self.cards[0][0] < declared_card[0]:
            return "draw"

        self.cards.sort(key=lambda x: x[0])
            
        min_card = self.cards[0]
        my_declaration = self.cards[0]

        # początek gry kładziemy najmniejszą kartę
        if declared_card is None:
            self.played_cards.append(min_card)
            return min_card, my_declaration
        
        # średnio mam karty mniejsze od zadeklarowanej
    
        # jeśli mamy kartę większą od zadeklarowanej to ją kładziemy        
        # jeśli nie mamy karty większej od zadeklarowanej to oszukujemy
        if my_declaration[0] < declared_card[0]:
            # if len(self.cards) == 2:
            #     return "draw"
            needed_value = min(14, declared_card[0])
            bigger_needed_value = min(14, needed_value + 1)
            for card in self.cards:
                if card[0] == needed_value or card[0] == bigger_needed_value:
                    my_declaration = card
                    break
                else:
                    my_declaration = (needed_value, my_declaration[1])
                    if my_declaration in self.played_cards:
                        color = self._find_free_color(needed_value)
                        if color is not None:
                            my_declaration = (needed_value, color)
                        else:
                            color = self._find_free_color(bigger_needed_value)
                            if color is not None:
                                my_declaration = (bigger_needed_value, color)
                            else:
                                my_declaration = (needed_value, my_declaration[1])

        self.played_cards.append(min_card)
        return min_card, my_declaration




    def checkCard(self, opponent_declaration):
        
        if opponent_declaration is None:
            return False

        if opponent_declaration in self.cards:
            return True
        
        if opponent_declaration[0] == 14:
            random = np.random.choice([True, False], p=[0.50, 0.50])
            if random:
                return True
            elif len(self.cards) == 1:
                return np.random.choice([True, False], p=[0.85, 0.15])
            
        
        if opponent_declaration[0] > self.cards[0][0] + 2:
            return True
        
        if opponent_declaration[0] > self.cards[0][0] + 1:
            return np.random.choice([True, False], p=[0.85, 0.15])
        
        if opponent_declaration[0] > self.cards[0][0]:
            if len(self.cards) > 1:
                if len(self.cards) == 2:
                    return True
                if len(self.cards) == 3:
                    return np.random.choice([True, False], p=[0.85, 0.15])
                if len(self.cards) == 4:
                    return np.random.choice([True, False], p=[0.80, 0.20])
            else:
                return np.random.choice([True, False], p=[0.70, 0.30])

        if opponent_declaration in self.played_cards:
            if self.moves < 2:
                return True
            if self.moves < 3:
                return np.random.choice([True, False], p=[0.60, 0.40])
            else:
                return np.random.choice([True, False], p=[0.250, 0.750])
        return False