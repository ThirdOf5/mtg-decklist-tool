
from enum import Enum # for deck format enumeration
import json # for parsing json blobs returned by scryfall
import os # for passing system calls to Linux
import requests # for easy http request processing
import sys # for sys.argv
import time # for time.sleep

# Global definition of basic land types
basic_land_cards = ["plains", "island", "swamp", "mountain", "forest", "wastes"]
validate = True

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
    def __init__(self, deck_name="default", deck_format=DeckFormat.Standard):
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
        # validate card with scryfall first
        if validate:
            http_obj = http_processing()
            if not http_obj.validate_card(card):
                # print("ERROR: {} is not a real card!".format(card.title())) # FIXME
                print(card.title())
                return False

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
                return False
        return True

    def print_deck(self):
        ''' Print our decklist in a readable format. '''
        print("\n== " + self.deck_name.title() + " ==")
        print("Format: " + self.deck_format.name)
        print("Total number of cards: {}".format(sum(self.decklist.values())))
        for card in self.decklist:
            print("{}x {}".format(self.decklist[card], card.title()))

    def save_deck_txt(self):
        ''' Print our decklist to a file with the same name as the deck's name.
            CAUTION: this will over-write a file with the same name!
        '''
        with open(self.deck_name.title().replace(" ", "_") + ".txt", 'w') as f:
            f.write("== {} ==\n".format(self.deck_name.title()))
            f.write("Format: {}\n".format(self.deck_format.name))
            f.write("Total number of cards: {}\n".format(sum(self.decklist.values())))
            for card in self.decklist:
                f.write("{}x {}\n".format(self.decklist[card], card.title()))

    def save_deck_proxies(self):
        ''' Prints the deck to a pdf as images for proxying. '''

        # helpful message aimed at impatient users :P
        print("Exporting to PDF. This might take a minute!")

        http = http_processing()
        fname = self.deck_format.name + '-' + self.deck_name.title().replace(' ', '-')
        image_list = list()
        counter = 0
        with open(fname + '.tex', 'w') as f:
            f.write('\\documentclass[11pt] {article}\n')
            f.write('\\usepackage[margin=0.3in]{geometry}\n')
            f.write('\\usepackage{graphicx}\n')
            f.write('\\usepackage{pdflscape}\n\n')
            f.write('\\begin{document}\n')
            f.write('\\begin{landscape}\n\n')
            for card in self.decklist:
                card_path = http.get_card_image(card)
                image_list.append(card_path)
                for i in range(self.decklist[card]):
                    # because of card size, we can only fit 4 per row in our pdf
                    if counter == 4:
                        counter = 0
                        f.write('\n')
                    counter += 1
                    f.write('\\includegraphics[width=6.3cm]{' + card_path + '}\n')
            f.write('\n')
            f.write('\\end{landscape}\n')
            f.write('\\end{document}\n')

        # if the os call executes with a return status of 0
        if not os.system('pdflatex -halt-on-error -interaction=nonstopmode ' + fname + ' >> /dev/null'):
            print("PDF created")
        else:
            print("Something broke... No output file created")

        # clean up all of the images we downloaded
        for img in image_list:
            os.system('rm ' + img)

        os.system('rm {}.aux {}.log'.format(fname, fname)) # clean up auxilary files
        os.system('rm {}.tex'.format(fname)) # clean up the tex file

    def load_csv(self, path, index):
        index = int(index)
        with open(path, 'r') as f:
            try:
                for line in f:
                    #self.add_card(1, line.strip().split(',')[index].strip()) # FIXME
                    self.add_card(1, line.strip())
            except:
                print("There was an unexpected error processing the file")
                return
        self.save_deck_proxies()

class http_processing:
    def __init__(self):
        self.scryfall_url = "https://api.scryfall.com/cards/search?q="

    def validate_card(self, card):
        ''' Uses scryfall.com's API to validate a card name. '''
        card_info = requests.get(self.scryfall_url + card)
        if card_info.status_code == 200:
            c = card_info.json()['data']
            for i in range(len(c)):
                if c[i]['name'].lower() == card.lower():
                    return True
        return False

    def get_card_image(self, card):
        ''' Uses scryfall to pull a png image of a card for printing later.
            Returns the path to the downloaded image.
        '''
        img_url = ""
        card_info = requests.get(self.scryfall_url + card)
        if card_info.status_code == 200:
            c = card_info.json()['data']
            for i in range(len(c)):
                if c[i]['name'].lower() == card.lower():
                    img_url = c[i]['image_uris']['large']
                else:
                    continue
        path = "./images/" + card.replace(' ', '_').replace("'", "") + ".jpg"
        time.sleep(0.005) # don't let scryfall lock us out
        img_file = open(path, 'wb')
        img_file.write(requests.get(img_url).content)
        img_file.close()
        return path


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
        if input_tmp == "QUIT" or input_tmp == "Q" or input_tmp == "":
            break

        input_lst = input_tmp.split()
        try:
            number = int(input_lst[0])
        except:
            number = 1
            input_lst.insert(0, 1)

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
    # TODO eventually we'll want to create some sort of argument handler class
    print_deck = False
    save_txt = False
    save_pdf = False
    list_path = ""
    index = -1
    if len(sys.argv) > 1:
        if '-p' in sys.argv or '--print' in sys.argv:
            print_deck = True
        if '-s' in sys.argv or '--save' in sys.argv:
            save_txt = True
        if '-pdf' in sys.argv or '--proxies' in sys.argv:
            save_pdf = True
        if '-v' in sys.argv or '--no-validation' in sys.argv:
            validate = False
        if '-l' in sys.argv:
            try:
                list_path = sys.argv[sys.argv.index('-l') + 1]
            except:
                print("You need to specify a file to load from!")
                sys.exit(1)
        if '--csv' in sys.argv:
            try:
                list_path = sys.argv[sys.argv.index('--csv') + 1]
                index = sys.argv[sys.argv.index('--csv') + 2]
            except:
                print("You need to specify a file and index to load!")
                sys.exit(1)

    d = Deck()
    if not list_path == "" and not index == -1:
        d.load_csv(list_path, index)
    else:
        d = create_deck()
        if print_deck:
            d.print_deck()
        if save_txt:
            d.save_deck_txt()
        if save_pdf:
            d.save_deck_proxies()


