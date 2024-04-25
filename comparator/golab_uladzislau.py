import numpy as np
from player import Player

class GolabUladzislau(Player):
    def __init__(self, name):
        super().__init__(name)
        self.previous_card = None

    def putCard(self, declared_card):

        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"

        card = min(self.cards, key=lambda x: x[0])

        declaration = (card[0], card[1])

        if declared_card is None:
            return card, declaration
        else:
            declared_value = declared_card[0]
            if card[0] < declared_value:
                if declared_value + 1 > 14:
                    declaration = (14, declaration[1])
                else:
                    declaration = (declared_value + 1, declaration[1])
                
                for crd in self.cards:
                    if crd[0] in [declaration[0], declaration[0] + 1]:
                        declaration = crd

            return card, declaration

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards:
            return True
    
        
        return False
