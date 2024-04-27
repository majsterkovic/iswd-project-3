import random

import numpy as np
from player import Player


class Hybiak(Player):

    def __init__(self, name, p85=0.85, p80=0.80, p75=0.75, p70=0.70, p60=0.60, p50=0.50):
        super().__init__(name)
        self.moves_counter = 0
        self.played_cards = [] # TODO update -> na podstawie dobierania kart przez przeciwnika?
        self.opponent_cards_amount = None
        self.moves = 0
        self.p85 = p85
        self.p80 = p80
        self.p75 = p75
        self.p70 = p70
        self.p60 = p60
        self.p50 = p50

    def startGame(self, cards):
        self.cards = cards
        self.opponent_cards_amount = len(cards) # na wszelki wypadek jakby w testach było inaczej niż 8 kart

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
                                my_declaration = (needed_value, my_declaration[1]) # "draw" ?

        self.played_cards.append(min_card)
        return min_card, my_declaration

    def checkCard(self, opponent_declaration):
        self.opponent_cards_amount -= 1

        if opponent_declaration is None:
            return False

        # jesli deklaracja przeciwnika jest w naszych kartach lub przeciwnik kładzie ostatnią kartę to sprawdzamy
        if opponent_declaration in self.cards or self.opponent_cards_amount == 0:
            return True
        
        # jesli przeciwnik deklaruje asa
        if opponent_declaration[0] == 14:
            random = np.random.choice([True, False], p=[self.p50, 1-self.p50])
            if random:
                return True
            # jesli zostala nam jedna karta
            elif len(self.cards) == 1:
                if self.cards[0][0] == 14 and self.opponent_cards_amount > 1: # wygrywamy w nastepnym ruchu
                    return False
                return np.random.choice([True, False], p=[self.p85, 1-self.p85])

        # jesli przeciwnik deklaruje karte o min 3 wieksza od naszej zawsze sprawdzamy
        if opponent_declaration[0] > self.cards[0][0] + 2:
            return True

        # jesli przeciwnik deklaruje karte o 2 wieksza od naszej to sprawdzamy z p85
        if opponent_declaration[0] > self.cards[0][0] + 1:
            return np.random.choice([True, False], p=[self.p85, 1-self.p85])
        
        # jesli przeciwnik deklaruje karte o 1 wieksza od naszej
        if opponent_declaration[0] > self.cards[0][0]:
            if len(self.cards) > 1:
                # jesli zostaly nam 2 karty sprawdzamy
                if len(self.cards) == 2:
                    return True
                # jesli zostaly nam 3 karty sprawdzamy z p85
                if len(self.cards) == 3:
                    return np.random.choice([True, False], p=[self.p85, 1-self.p85])
                # jesli zostaly nam 4 karty sprawdzamy z p80
                if len(self.cards) == 4:
                    return np.random.choice([True, False], p=[self.p80, 1-self.p80])
            else:
                # jesli zostala nam jedna karta
                # if self.opponent_cards_amount > 1: # wygrywamy w nastepnym ruchu - no nie bo mamy za małą kartę
                #     return False
                return np.random.choice([True, False], p=[self.p70, 1-self.p70])

        # jesli deklaracja przeciwnika w zbiorze zagranych przez nas kart
        if opponent_declaration in self.played_cards:
            if self.moves < 2:
                return True
            if self.moves < 3:
                return np.random.choice([True, False], p=[self.p60, 1-self.p60])
            else:
                return np.random.choice([True, False], p=[1-self.p75, self.p75])
        return False

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if iChecked and not iDrewCards:
            self.opponent_cards_amount += noTakenCards
            self.played_cards.pop()  # ostatnia karta która zagraliśmy jest teraz u przeciwnika

        if log: print("Feedback = " + self.name + " : checked this turn = " + str(checked) +
              "; I checked = " + str(iChecked) + "; I drew cards = " +
                      str(iDrewCards) + "; revealed card = " +
                      str(revealedCard) + "; number of taken cards = " + str(noTakenCards) +
                      " opponent cards count: " + str(self.opponent_cards_amount))

        # self.moves_counter += 1
