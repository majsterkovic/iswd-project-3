class Card():
    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __str__(self):
        return f"{self.number} {self.color}"
    
    def to_tuple(self):
        return (self.number, self.color)
    
    
class Deck():
    def __init__(self, cards):
        self.deck = [Card(card[0], card[1]) for card in cards]
        self.deck.sort(key=lambda card: card.number)

    def first_card(self):
        return self.deck[0]
    
    def last_card(self):
        return self.deck[-1]
    
    def first_card_with_number_bigger_than(self, number):
        for card in self.deck:
            if card.number >= number:
                return card
        return None
    
    def length(self):
        return len(self.deck)