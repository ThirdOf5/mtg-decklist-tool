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
        self.max_copies = 1 if self.deck_format == DeckFormat.EDH else 4

    def add_card(self, card):
        ''' Add a card to the deck.

            INPUT:
                card: a card name to be added to the deck.

            OUTPUT:
                True if adding the card was successful.
                False if adding the card failed for any reason.
        '''
        self.decklist[card] = self.decklist.get(card, 0) + 1
        if self.decklist[card] > self.max_copies:
            self.decklist[card] = self.max_copies
            if self.max_copies == 1:
                print("ERROR: You can't have more than 1 copy of a card in your deck!")
            else:
                print("ERROR: You can't have more than {} copies of a card in your deck!".format(self.max_copies))
            return False
        return True

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
    f = input("> ")
    if f == '1':
        my_format = DeckFormat.Standard
    elif f == '2':
        my_format = DeckFormat.Modern
    elif f == '3':
        my_format = DeckFormat.EDH
    else:
        print("ERROR: That wasn't an option! Assuming standard as the format of choice.")
        my_format = DeckFormat.Standard

    # create a decklist object
    my_deck = Deck(my_name, my_format)

    # read cards from user
    i = 0
    while i < 5: # TODO change this end condition!!
        i += 1
        # TODO add card name checking
        card = input("Add a card to the deck: ")
        if not my_deck.add_card(card):
            i -= 1

    # return our deck object
    return my_deck

if __name__ == '__main__':
    d = create_deck()
    d.print_deck()

