import random
from unicards import unicard
import card_setup
import card_detect
import time

class Card:
    """Represents a standard playing card.

    Attributes:
      suit: integer 0-3
      rank: integer 1-13
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
              "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        """Initializes a Card with a suit and rank."""
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a unicard representation of the Card."""
        suit = self.suit
        rank = self.rank
        return convert_to_unicard(suit,rank)


    def __eq__(self, other):
        """Checks whether self and other have the same rank and suit.

        returns: boolean
        """
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        """Compares this card to other, first by suit, then rank.

        returns: boolean
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2




class Deck:
    """Represents a deck of cards.

    Attributes:
      cards: list of Card objects.
    """

    def __init__(self):
        """Initializes the Deck with 52 cards."""
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        """Returns a string representation of the deck.
        """
        res = []
        for card in self.cards:
            res.append(str(card))
        return ' '.join(res)

    def add_card(self, card):
        """Adds a card to the deck.

        card: Card
        """
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck or raises exception if it is not there.

        card: Card
        """
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):
    """Represents a hand of playing cards."""

    def __init__(self, label=''):
        self.cards = []
        self.label = label
        self.total = 0


class Game():
    """Represents a game of blackjack

    player: Hand object containing real cards
    dealer: Hand object of the computer's cards
    """

    def __init__(self):
        """Starts a new round of blackjack"""
        self.deck=Deck()
        self.deck.shuffle()
        self.player=Hand('Player')
        #self.player=card_detect.cards
        self.dealer=Hand('Dealer')

    def deal(self):
        """Deals 2 cards to the player and one to the dealer"""
        self.deck.move_cards(self.dealer,1)
        print("Dealer" + str(self.dealer) + " []")
        #self.deck.move_cards(self.player,2)
        #print("Player" + str(self.player))

        # Call mainloop function from card_detect.py and print resulting rank and suit
        print("Please show your first card to the camera")
        rank_name, suit_name = card_detect.mainloop()
        rank_name1 = rank_name
        suit_name1 = suit_name
        print("Player has:" + str(rank_name1),'of', str(suit_name1))
        suitInt1, rankInt1 = convert_card_to_int(suit_name1, rank_name1)
        print("Please show your second card to the camera (program will wait momentarily)")
        time.sleep(5)

        # Call mainloop function from card_detect.py and print resulting rank and suit
        rank_name, suit_name = card_detect.mainloop()
        rank_name2 = rank_name
        suit_name2 = suit_name
        print("Player has:" + str(rank_name2),'of', str(suit_name2))
        suitInt2, rankInt2 = convert_card_to_int(suit_name2, rank_name2)

        # Remove cards from deck and deal them to player
        p1 = Card(suitInt1, rankInt1)
        p2 = Card(suitInt2, rankInt2)
        self.deck.remove_card(p1)
        self.deck.remove_card(p2)
        self.player.add_card(p1)
        self.player.add_card(p2)
        print("Player" + str(self.player))



    def play(self):
        """Simulates the player's turn in a game of blackjack"""
        ans = input("Would you like to hit or stay?\n")
        if (ans == "hit"):
            self.deck.move_cards(self.player,1)
            print("Player" + str(self.player))
            self.play()
        elif (ans == "stay"):
            total = (self.get_player_total())
            if (total == 'BUST'):
                print("BUST\nDealer Wins")
            else:
                print(self.house())
        else:
            print("Error: End of Game")

    def house(self):
        """Simulates the dealer's turn in a game of blackjack

        returns: String containing the results of the game"""
        self.deck.move_cards(self.dealer,1)
        print("Dealer" + str(self.dealer))
        self.get_dealer_total()

        while(self.dealer.total<=17):
            (self.get_dealer_total())
            if(self.dealer.total>=self.player.total):
                return ("Dealer Wins")
            else:
                self.deck.move_cards(self.dealer,1)
                print("Dealer" + str(self.dealer))
                self.get_dealer_total()

        if(self.dealer.total>21):
            return ("Dealer Bust\n Player Wins")
        elif(self.dealer.total>=self.player.total):
            return ("Dealer Wins")
        return ("Player Wins")

    def get_dealer_total(self):
        """Calculates the current total points of the dealer.

        If there is an ace it will determine whether to be worth 11 or 1 point
        based on if the current total is less than or equal to 10"""
        values = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.dealer.cards.sort(reverse = True)
        self.dealer.total = 0
        for x in self.dealer.cards:
            if x.rank == 1:
                if self.dealer.total<=10:
                    self.dealer.total += 11
                else:
                    self.dealer.total += 1
            else:
                self.dealer.total += values[x.rank]


    def get_player_total(self):
        """Calculates the current total points of the player and gives the
        player the option to choose if an ace counts for 1 point or 11.

        returns: BUST if it is over 21 or it will return the total
        if it is less than 21"""
        values = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.player.cards.sort(reverse = True)
        for x in self.player.cards:
            if x.rank == 1:
                ace = int(input("11 or 1 \n"))
                while (ace != 1 and ace != 11):
                    ace = int(input("11 or 1\n"))
                self.player.total += ace
            else:
                self.player.total += values[x.rank]
        if self.player.total > 21:
            return "BUST"
        else:
            return self.player.total


def convert_to_unicard(suit=0, rank=2):
    unicard_suit = ['s','h','d', 'c']
    unicard_rank = [None, 'A','2','3','4','5','6','7','8','9','T','J','Q','K']
    if (suit == -1 or rank == -1):
        return "NaN"
    card = str(unicard_rank[rank])+str(unicard_suit[suit])
    return unicard(card)

def convert_card_to_int(suit,rank):
    """Converts the OpenCV card detected into integers so it is readable by
    the program"""

    if(suit == "Spades"):
        suitInt = 0
    elif(suit == "Hearts"):
        suitInt = 1
    elif(suit == "Diamonds"):
        suitInt = 2
    elif(suit == "Clubs"):
        suitInt = 3
    else:
        suitInt = -1

    if(rank == "Ace"):
        rankInt = 1
    elif(rank == "Two"):
        rankInt = 2
    elif(rank == "Three"):
        rankInt = 3
    elif(rank == "Four"):
        rankInt = 4
    elif(rank == "Five"):
        rankInt = 5
    elif(rank == "Six"):
        rankInt = 6
    elif(rank == "Seven"):
        rankInt = 7
    elif(rank == "Eight"):
        rankInt = 8
    elif(rank == "Nine"):
        rankInt = 9
    elif(rank == "Ten"):
        rankInt = 10
    elif(rank == "Jack"):
        rankInt = 11
    elif(rank == "Queen"):
        rankInt = 12
    elif(rank == "King"):
        rankInt = 13
    else:
        rankInt = -1

    return(suitInt,rankInt)

if __name__ == '__main__':
    round1 = Game()
    round1.deal()
    round1.play()
