from enum import Enum

class DeckFormat(Enum):
    Standard = 1
    Modern = 2
    EDH = 3

class Card:
    def __init__(self, card_name):
        self.card_name = card_name

    def print_card(self):
        print(self.card_name)

class Deck:
    def __init__(self, deck_name, deck_format=DeckFormat.Standard):
        self.deck_name = deck_name
        self.deck_format = deck_format
        self.decklist = dict()

    def print_deck(self):
        print("== " + self.deck_name + " ==")
        print("Format: " + self.deck_format.name)
        for card in self.decklist:
            print("{}x {}".format(self.decklist[card], card))

def create_deck():
    ''' Create and run a REPL to read card names and quantities from the user.'''
    # ask the user for a deck name
    my_name = input("Please give a name for your deck: ")
    # take deck format
    print("Select a number for what format you would like: ")
    print("\t1. Standard\n\t2. Modern\n\t3. Commander/EDH\n")
    f = input(">")
    if f == '1':
        my_format = DeckFormat.Standard
    elif f == '2':
        my_format = DeckFormat.Modern
    elif f == '3':
        my_format = DeckFormat.EDH
    else:
        print("ERROR: That wasn't an option! Assuming Standard")
        my_format = DeckFormat.Standard
    # create a decklist object
    my_deck = Deck(my_name, my_format)
    # read cards from user
    for i in range(5): #TODO change this end condition!!
        card = input("Add a card to the deck: ")
        my_deck.decklist[card] = my_deck.decklist.get(card, 0) + 1

    # return our deck object
    return my_deck

if __name__ == '__main__':
    # TODO take command line flags
    d = create_deck()
    d.print_deck()


