

from tkinter import *
from tkinter import ttk
import random

root = Tk()
root.title("Blackjack")

# ---------- CARD SYSTEM ----------

class Card:
    def __init__(self, suit, rank):
        # Initialiserer et kort med kulør (suit) og værdi (rank)
        self.suit = suit   # Fx ♥, ♠, ♦, ♣
        self.rank = rank   # Fx 2-10, J, Q, K, A

    def value(self):
        # Returnerer kortets værdi i Blackjack
        if self.rank in ["J","Q","K"]:
            return 10  # Billedkort har værdien 10
        elif self.rank == "A":
            return 11  # Es starter som 11 (kan senere blive 1 i Hand-klassen)
        else:
            return int(self.rank)  # Tal-kort (2-10) returneres som deres værdi

    def __str__(self):
        # Returnerer en tekst-repræsentation af kortet
        # Fx "A♠" eller "10♥"
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self, num_decks=6):
        suits = ["♥️","♦️","♣️","♠️"]
        ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        # lav flere decks
        self.cards = [Card(s,r) for s in suits for r in ranks for _ in range(num_decks)]
        random.shuffle(self.cards)

    def draw(self):
        # reshuffle hvis færre end 3 decks tilbage
        if len(self.cards) < 52*3:
            self.shuffle_shoe()
        return self.cards.pop()

    def shuffle_shoe(self):
        shufle_var.set("Blander kortene…")   # opdaterer label
        root.update_idletasks()               # tving GUI til at opdatere straks
        random.shuffle(self.cards)
        shufle_var.set("")                    # nulstil efter shuffle

    """
    START Deck

    OPRET liste af kulører
    OPRET liste af værdier

    OPRET kortliste:
        FOR hver kulør
            FOR hver værdi
                GENTAG antal decks gange
                    tilføj nyt kort til listen
                SLUT
            SLUT
        SLUT
    bland kortene
    SLUT

    START draw
        IF antal kort < 3 decks THEN
            bland kortene igen
        END IF
        returnér øverste kort
    SLUT

    START shuffle_shoe
        vis "Blander kortene…" i GUI
        opdater GUI
        bland kortene
        fjern besked
    SLUT
    """




class Hand:
    def __init__(self, bet):
        # Initialiserer en hånd med en indsats (bet)
        self.cards = []   # Liste der indeholder kortene i hånden
        self.bet = bet    # Spillerens indsats på denne hånd

    def add_card(self, card):
        self.cards.append(card)# Tilføjer et kort til hånden

    def value(self):
        # Beregner den samlede værdi af hånden (Blackjack regler)
        total = 0   # Samlet værdi af kort
        aces = 0    # Antal esser (fordi de kan være 1 eller 11)
        # Gennemløber alle kort i hånden
        for card in self.cards:
            total += card.value()  # Lægger kortets værdi til totalen
            # Tæller antal esser
            if card.rank == "A":
                aces += 1
        # Hvis total er over 21 og der er esser,
        # omregnes et es fra 11 → 1 (trækker 10 fra)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total  # Returnerer den endelige værdi

    def show_cards(self):
        # Returnerer en tekststreng med alle kort i hånden
        # Fx: "10♠ A♥"
        return " ".join(str(c) for c in self.cards)

class DealerHand(Hand):
    # DealerHand arver fra Hand (inheritance)
    def show_cards(self, hide_second=True):
        # Metoden er en override af Hand.show_cards (polymorfisme)
        # Hvis dealerens andet kort skal skjules
        if hide_second and len(self.cards) > 1:
            return f"{self.cards[0]} ?"  # Viser kun første kort
        # Ellers vises alle kort
        return " ".join(str(c) for c in self.cards)

class Player:
    def __init__(self):
        self.balance = 1000
        self.hands = []

    def can_split(self):
        # kun muligt hvis første hånd har 2 kort af samme værdi
        hand = self.hands[0]
        return len(hand.cards) == 2 and hand.cards[0].value() == hand.cards[1].value()

    def split_hand(self, deck):
        if not self.can_split():
            return False  # kan ikke splitte

        hand = self.hands[0]
        card1 = hand.cards[0]
        card2 = hand.cards[1]

        # hver hånd får samme bet som originalen
        if hand.bet > self.balance:
            return False  # ikke nok penge til at splitte

        self.balance -= hand.bet

        hand1 = Hand(hand.bet)
        hand2 = Hand(hand.bet)

        hand1.add_card(card1)
        hand2.add_card(card2)

        # træk ét kort til hver hånd
        hand1.add_card(deck.draw())
        hand2.add_card(deck.draw())

        self.hands = [hand1, hand2]

        return True


# ---------- GAME ----------


class Game:

    def __init__(self):
        self.player = Player()
        self.deck = Deck(num_decks=6)
        self.current_hand = 0

    def start_round(self,bet):

        if bet > self.player.balance:
            result.set("Not enough money!")
            return

        result.set("")

        self.deck = Deck()

        self.player.hands = [Hand(bet)]
        self.current_hand = 0

        self.dealer = DealerHand(0)


        self.player.balance -= bet
        balance_var.set(self.player.balance)

        for _ in range(2):
            self.player.hands[0].add_card(self.deck.draw())
            self.dealer.add_card(self.deck.draw())

        self.update_gui(initial=True)

    """
    START start_round(bet)

    IF bet er større end spillerens balance THEN
        vis besked "Not enough money!" i result
        STOP funktionen
    END IF

    nulstil resultatbesked

    opret nyt deck ud fra deck number

    opret en liste med én hånd til spilleren med indsatsen bet
    sæt current_hand til 0

    opret dealer hånd

    træk bet fra spillerens balance med balance.var
    opdater balance på skærmen med

    GENTAG 2 gange
        giv et kort til spillerens hånd
        giv et kort til dealerens hånd
    SLUT GENTAG

    opdater brugergrænseflade (initial visning)

    SLUT
    """

    def update_gui(self, initial=False):
        text = ""
        for i, hand in enumerate(self.player.hands):

            marker = "◀" if i == self.current_hand else ""

            text += f"Hånd {i+1}: " + " ".join(str(c) for c in hand.cards) + f" (Value: {hand.value()}) {marker}\n"

        player_cards.set(text.strip())

        if initial:
            dealer_cards.set(self.dealer.show_cards(True))
            dealer_value.set("")
        else:
            dealer_cards.set(self.dealer.show_cards(False))
            dealer_value.set(self.dealer.value())



    def hit(self):

        hand = self.player.hands[self.current_hand]
        hand.add_card(self.deck.draw())

        if hand.value() > 21:

            if self.current_hand < len(self.player.hands) - 1:
                self.current_hand += 1
                result.set("Bust! Next hand.")
                self.update_gui(initial=True)
                return

            else:
                result.set("Bust! Dealer wins.")
                self.update_gui()
                return

        self.update_gui(initial=True)

    def stand(self):

        if self.current_hand < len(self.player.hands) - 1:
            self.current_hand += 1
            result.set("Next hand")
            self.update_gui(initial=True)
            return

        while self.dealer.value() < 17:
            self.dealer.add_card(self.deck.draw())

        self.update_gui()
        self.check_result()


    def double(self):

        hand = self.player.hands[self.current_hand]

        if hand.bet > self.player.balance:
            result.set("Not enough money to double")
            return

        self.player.balance -= hand.bet
        balance_var.set(self.player.balance)

        hand.bet *= 2
        hand.add_card(self.deck.draw())

        if hand.value() > 21:
            result.set("Bust after double!")

        self.stand()


    def split(self):
        if self.player.split_hand(self.deck):
            result.set("Hand splitted!")
            self.update_gui(initial=True)   # skjul dealer kort
        else:
            result.set("Cannot split!")



    def check_result(self):

        dealer_val = self.dealer.value()
        message = ""

        if dealer_val > 21:
            message = "Dealer bust! You win!"

        for hand in self.player.hands:

            player_val = hand.value()

            if player_val > 21:
                continue

            if dealer_val > 21 or player_val > dealer_val:
                self.player.balance += hand.bet * 2
                message = "You win!"

            elif player_val == dealer_val:
                self.player.balance += hand.bet
                message = "Push."

            else:
                message = "Dealer wins!"

        result.set(message)
        balance_var.set(self.player.balance)


game = Game()


# ---------- PAGE SYSTEM ----------

betframe = ttk.Frame(root,padding=40)
betframe.grid(row=0,column=0,sticky="nsew")

gameframe = ttk.Frame(root,padding=40)
gameframe.grid(row=0,column=0,sticky="nsew")


# ---------- BET PAGE ----------

ttk.Label(betframe,text="Enter your bet").grid(row=0,column=0,pady=10)

entry = Entry(betframe)
entry.grid(row=1,column=0,pady=10)

def hent_bet():

    bet = int(entry.get())
    game.start_round(bet)

    gameframe.tkraise()

ttk.Button(betframe,text="Start Game",command=hent_bet).grid(row=2,column=0,pady=10)

balance_var = IntVar(value=game.player.balance)


ttk.Label(betframe,text="Balance").grid(row=3,column=0)
ttk.Label(betframe,textvariable=balance_var,font=("Arial",14)).grid(row=4,column=0)

# ---------- GAME PAGE ----------

player_cards = StringVar()
player_value = IntVar()

dealer_cards = StringVar()
dealer_value = IntVar()

result = StringVar()

shufle_var = StringVar()



ttk.Label(gameframe,text="Dealer").grid(row=2,column=0,pady=(20,0))
ttk.Label(gameframe,textvariable=dealer_cards,font=("Arial",18)).grid(row=3,column=0)
ttk.Label(gameframe,textvariable=dealer_value).grid(row=4,column=0)

ttk.Label(gameframe,text="Player").grid(row=5,column=0,pady=(20,0))
ttk.Label(gameframe,textvariable=player_cards,font=("Arial",18)).grid(row=6,column=0)
ttk.Label(gameframe,textvariable=player_value).grid(row=7,column=0)

ttk.Label(gameframe, textvariable=shufle_var, font=("Arial",12), foreground="red").grid(row=5,column=5)

ttk.Label(gameframe,text="Balance").grid(row=0,column=0)
ttk.Label(gameframe,textvariable=balance_var,font=("Arial",14)).grid(row=1,column=0)


# ---------- BUTTONS ----------

buttonframe = ttk.Frame(gameframe)
buttonframe.grid(row=8,column=0,pady=20)

ttk.Button(buttonframe,text="Hit",command=game.hit).grid(row=0,column=0,padx=5)
ttk.Button(buttonframe,text="Stand",command=game.stand).grid(row=0,column=1,padx=5)
ttk.Button(buttonframe,text="Double",command=game.double).grid(row=0,column=2,padx=5)
ttk.Button(buttonframe,text="Split",command=game.split).grid(row=0,column=3,padx=5)

ttk.Label(gameframe,textvariable=result,font=("Arial",14)).grid(row=9,column=0,pady=10)


# ---------- NEXT ROUND ----------

def next_round():

    entry.delete(0,END)
    result.set("")
    player_cards.set("")
    dealer_cards.set("")
    player_value.set(0)
    dealer_value.set(0)

    betframe.tkraise()

ttk.Button(gameframe,text="Next Round",command=next_round).grid(row=10,column=0,pady=10)


# start page
betframe.tkraise()

root.mainloop()