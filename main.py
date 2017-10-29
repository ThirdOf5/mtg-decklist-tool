from enum import Enum # for deck format enumeration
import sys # for sys.argv

# Global definition of basic land types
basic_land_cards = ["plains", "island", "swamp", "mountain", "forest", "wastes"]

class DeckFormat(Enum):
    Standard = 1
    Modern = 2
    EDH = 3
    Pauper = 4
    Freeform = 5

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

    def add_card(self, number, card):
        ''' Add a card to the deck.

            INPUT:
                number: the number of a card to be added.
                card: a card name to be added to the deck.

            OUTPUT:
                True if adding the card was successful.
                False if adding the card failed for any reason.
        '''
        # TODO add scryfall card validation! --> it will get its own function, maybe its own class

        # the core of the function. Everything else is checking for deckbuilding restrictions
        self.decklist[card] = number

        # if the card is not a basic land
        if not basic_land_cards.count(card.lower()):
            # if we would have more than the max allowed number of that card
            if self.decklist[card] > self.max_copies:
                self.decklist[card] = self.max_copies
                if self.max_copies == 1:
                    print("ERROR: You can't have more than 1 copy of a card in your deck!")
                else:
                    print("ERROR: You can't have more than {} copies of a card in your deck!".format(self.max_copies))
                print("\tDefaulting to the maximum number of allowed copies")

    def print_deck(self):
        ''' Print our decklist in a readable format. '''
        print("\n== " + self.deck_name + " ==")
        print("Format: " + self.deck_format.name)
        print("Total number of cards: {}".format(sum(self.decklist.values())))
        for card in self.decklist:
            print("{}x {}".format(self.decklist[card], card.title()))

    def save_deck(self):
        ''' Print our decklist to a file with the same name as the deck's name.
            CAUTION: this will over-write a file with the same name!
        '''
        with open(self.deck_name + ".txt", 'w') as f:
            f.write("== {} ==\n".format(self.deck_name))
            f.write("Format: {}\n".format(self.deck_format.name))
            f.write("Total number of cards: {}\n".format(sum(self.decklist.values())))
            for card in self.decklist:
                f.write("{}x {}\n".format(self.decklist[card], card.title()))


def create_deck():
    ''' Create and run a REPL to read card names and quantities from the user.'''
    # ask the user for a deck name
    my_name = input("Please give a name for your deck: ")

    # take deck format
    print("Select a number for what format you would like: ")
    print("\t1. Standard\n\t2. Modern\n\t3. Commander/EDH\n\t4. Pauper\n\t5. Freeform")
    format_in = input("> ")
    if format_in == '1':
        my_format = DeckFormat.Standard
    elif format_in == '2':
        my_format = DeckFormat.Modern
    elif format_in == '3':
        my_format = DeckFormat.EDH
    elif format_in == '4':
        my_format = DeckFormat.Pauper
    elif format_in == '5':
        my_format = DeckFormat.Freeform
    else:
        print("ERROR: That wasn't an option! Assuming freeform.")
        my_format = DeckFormat.Freeform

    # create a decklist object
    my_deck = Deck(my_name, my_format)

    # read cards from user
    while True:
        input_tmp = input("Add a number of cards to the deck: ")
        # typing QUIT will take you out of the REPL
        if input_tmp == "QUIT" or input_tmp == "Q":
            break

        input_lst = input_tmp.split()
        # be able to accept "1 Shock" or just "Shock"
        try:
            number = int(input_lst[0])
        except:
            number = 1
            input_lst.insert(0, 1)

        # FIXME how to create a string from a list of words efficiently?
        card = ""
        for c in input_lst[1:]:
            card += c
            card += " "
        card = card.strip().lower()

        # actually add the card(s) to our decklist
        my_deck.add_card(number, card)

    # return our deck object
    return my_deck

if __name__ == '__main__':
    d = create_deck()
    # TODO eventually we'll want to create some sort of argument handler class
    if len(sys.argv) > 1:
        if sys.argv[1] == '-p' or sys.argv[1] == '--print':
            d.print_deck()
        elif sys.argv[1] == '-s' or sys.argv[1] == '--save':
            d.save_deck()

