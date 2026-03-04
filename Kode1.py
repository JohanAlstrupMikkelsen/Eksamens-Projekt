



import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
"""
card = Card("Hearts", "A")
print(card)
print(card.value())
"""


class Deck:
    def __init__(self):
        suits = ["Hjerter", "Ruder", "Klør", "Spar"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

deck=Deck()

print(len(deck.cards))



class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        total = 0
        aces = 0

        for card in self.cards:
            total += card.value()
            if card.rank == "A":
                aces += 1

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)
    


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Hand()
        self.dealer = Hand()

    def start(self):
        # Giv startkort
        for _ in range(2):
            self.player.add_card(self.deck.draw())
            self.dealer.add_card(self.deck.draw())

        print("Your hand:", self.player)
        print("Value:", self.player.value())
        
    def player_turn(self):
        while self.player.value() < 21:
            choice = input("Hit or stand? ").lower()
            if choice == "hit":
                self.player.add_card(self.deck.draw())
                print("Your hand:", self.player)
                print("Value:", self.player.value())
            else:
                break

game = Game()
game.start()
game.player_turn()




