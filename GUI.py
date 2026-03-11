from tkinter import *
from tkinter import ttk

root = Tk()

def hent_bet():
    tekst = entry.get()
    print(tekst)
    frame2.tkraise()   # skifter til side 2


# ----- Frame 1 (startside) -----
betframe = ttk.Frame(root, padding=20)
betframe.grid(row=0, column=0, sticky="nsew")

entry = Entry(betframe)
entry.grid(row=0, column=0, pady=10)

knap = Button(betframe, text="Bet", command=hent_bet)
knap.grid(row=1, column=0)


# ----- Frame 2 (ny side) -----
frame2 = ttk.Frame(root, padding=20)
frame2.grid(row=0, column=0, sticky="nsew")

label = Label(frame2, text="Velkommen til spillet!")
label.grid(row=0, column=0)



def show_hands(self, initial=False):
    for i, hand in enumerate(self.player.hands):
        print(f"Your hand {i+1}: {hand} (Value: {hand.value()})")
        ttk.Label(root, text=f"Your hand {i+1}: {hand} (Value: {hand.value()})").grid(column=0, row=3)
    if initial:
        # Vis kun dealerens første kort til start
        print(f"Dealer shows: {self.dealer.cards[0]} and ?")
    else:
        print(f"Dealer hand: {self.dealer} (Value: {self.dealer.value()})")




# start på frame1
betframe.tkraise()

root.mainloop()