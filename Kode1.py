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

class Deck:
    def __init__(self):
        suits = ["Hjerter", "Ruder", "Klør", "Spar"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Hand:
    def __init__(self, bet):
        self.cards = []
        self.bet = bet  # Krævet indsats for hver hånd

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

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].value() == self.cards[1].value()

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

class Player:
    def __init__(self, bet):
        self.hands = [Hand(bet)]

    # Split hånd
    def split(self, hand_index, deck):
        hand = self.hands[hand_index]
        card1 = hand.cards[0]
        card2 = hand.cards[1]

        # Hver ny hånd får samme bet som originalen
        hand1 = Hand(hand.bet)
        hand2 = Hand(hand.bet)

        hand1.add_card(card1)
        hand2.add_card(card2)

        # Træk ét nyt kort til hver hånd
        hand1.add_card(deck.draw())
        hand2.add_card(deck.draw())

        self.hands[hand_index] = hand1
        self.hands.append(hand2)

class Game:
    def __init__(self):
        self.deck = Deck()
        bet = int(input("Hvor meget vil du satse? "))
        self.player = Player(bet)
        self.dealer = Hand(0)  # Dealer har dummy-bet

    # Start spillet med to kort til spiller og dealer
    def start(self):
        for _ in range(2):
            self.player.hands[0].add_card(self.deck.draw())
            self.dealer.add_card(self.deck.draw())
        self.show_hands(initial=True)

    # Vis hænder
    def show_hands(self, initial=False):
        for i, hand in enumerate(self.player.hands):
            print(f"Your hand {i+1}: {hand} (Value: {hand.value()})")
        if initial:
            # Vis kun dealerens første kort til start
            print(f"Dealer shows: {self.dealer.cards[0]} and ?")
        else:
            print(f"Dealer hand: {self.dealer} (Value: {self.dealer.value()})")

    # Spillerens tur
    def player_turn(self):
        hand_index = 0
        while hand_index < len(self.player.hands):
            hand = self.player.hands[hand_index]
            while hand.value() < 21:
                choice = input(f"Hand {hand_index+1} - Hit, Stand, Split, Double? ").lower()
                if choice == "hit":
                    hand.add_card(self.deck.draw())
                    print(f"Hand {hand_index+1}: {hand} (Value: {hand.value()})")
                    if hand.value() > 21:
                        print(f"Hand {hand_index+1} busted!")
                        break
                elif choice == "double":
                    hand.bet *= 2
                    hand.add_card(self.deck.draw())
                    print(f"Hand {hand_index+1} (after double): {hand} (Value: {hand.value()})")
                    break  # Turen slutter efter double
                elif choice == "split":
                    if hand.can_split():
                        self.player.split(hand_index, self.deck)
                        print("Hands after split:")
                        self.show_hands()
                        hand = self.player.hands[hand_index]  # opdater reference til nuværende hånd
                    else:
                        print("Cannot split this hand.")
                else:  # stand
                    break
            hand_index += 1

    # Dealers tur
    def dealer_turn(self):
        print("\nDealer's turn:")
        self.show_hands()
        while self.dealer.value() < 17:
            self.dealer.add_card(self.deck.draw())
            print(f"Dealer hits: {self.dealer} (Value: {self.dealer.value()})")
        if self.dealer.value() > 21:
            print("Dealer busted!")

    # Afslutning og resultat
    def ending(self):
        dealer_value = self.dealer.value()
        print("\n--- RESULTS ---")
        for i, hand in enumerate(self.player.hands):
            player_value = hand.value()
            print(f"Hand {i+1}: {hand} (Value: {player_value}) Bet: {hand.bet}")
            if player_value > 21:
                print(f"Hand {i+1}: You busted! Lose {hand.bet}")
            elif dealer_value > 21 or player_value > dealer_value:
                print(f"Hand {i+1}: You won! Win {hand.bet}")
            elif player_value < dealer_value:
                print(f"Hand {i+1}: You lost! Lose {hand.bet}")
            else:
                print(f"Hand {i+1}: Even. Bet returned {hand.bet}")

    # Kør hele spillet
    def play(self):
        self.start()
        self.player_turn()
        self.dealer_turn()
        self.ending()

if __name__ == "__main__":
    game = Game()
    game.play()