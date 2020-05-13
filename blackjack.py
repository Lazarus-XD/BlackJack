import random

suits = ("Spades", "Clubs", "Hearts", "Diamonds")
ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace")
value = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

class Card():
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    #prints the specific card's ranks and suits
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    #prints all the cards in the deck
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has:" + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    #takes one card from the deck
    def deal(self):
        return self.deck.pop()

class Hand():
    def __init__(self):
        self.hand_cards = []
        self.hand_value = 0
        self.has_ace = 0

    def add_a_card(self, card):
        #card is taken from Deck() class by calling deal method
        self.hand_cards.append(card)
        self.hand_value += value[card.rank]
        if card.rank == "Ace":
            self.has_ace += 1

    #Ace value can be either 1 or 11. This method checks which one is befecial for the person
    def adjust_for_ace(self):
        if self.hand_value > 21 and self.has_ace:
            self.hand_value -= 10
            self.has_ace -= 1

class Chips():
    def __init__(self, total):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet 

    #This method is called when player's hand value is 21 at beginning and dealer's hand value is not     
    def blackjack_win(self):
        self.total += self.bet*1.5 

#To determine if player's turn and game ended or not
playing = True
game_on = True

#Ask player the amount he wants to bet
def take_a_bet(chip):
    while True:
        try:
            chip.bet = int(input("Enter the amount you want to bet: "))
        except:
            print("The amount must be an integer value!")
        else:
            if chip.bet > chip.total:
                print("Your bet amount is greater than your chip amount. You have {} chips.".format(chip.total))
            else:
                break

#Show all cards of player
def show_player(player):
    print("\nThe player has:")
    for card in player.hand_cards:
        print(card)

#Show one card of dealer
def show_dealer_some(dealer):
    print("\nThe dealer has:")
    print("<Card Hidden>")
    print(dealer.hand_cards[1])

#Show all cards of dealer
def show_dealer_all(dealer):
    print("\nThe dealer has:")
    for card in dealer.hand_cards:
        print(card)

#Askes player if he wants to take a card from deck or end turn 
def hit_or_stand():
    global playing
    while True:
        value = input("Do you want to hit or stand? Enter h or s: ")
        if value == "h" or value == "s":
            break
        else:    
            print("Please enter either h or s!")
    if value == "h":
        hit(player)
        player.adjust_for_ace()
        show_player(player)
        print("\nThe player hand value is {}\n".format(player.hand_value))
        return
    elif value == "s":
        playing = False

#takes a card from deck for the person's turn in account
def hit(person):
    person.add_a_card(deck.deal())

#functions (4 below) to determine if player won or lost
def player_win():
    print("Player has won the round!")
    player_chips.win_bet()

def player_bust():
    print("Dealer has won the round!")
    player_chips.lose_bet()

def player_win_blackjack():
    print("Player has won the round by blackjack!")
    player_chips.blackjack_win()

def dealer_win():
    print("Dealer has won the round!")
    player_chips.lose_bet()

def dealer_bust():
    print("Player has won the round!")
    player_chips.win_bet()

def rules():
    print('''
The rules of the game are given below:
1. The player is given 2 cards-face up in the beginning.
2. The dealer is given 2 cards, one face-up and other face-down.
3. The cards from 2-10 has face value, Jack, King, Queen has value of 10, Ace can be either 1 or 11.
4. The player goes first. Has option to hit(take 1 card from deck) or stand(end turn).
5. The dealer will have to take cards from deck until hand value becomes atleast 17.
6. If the hand value is more than 21 then it is 'bust'. Meaning the other person wins.
7. Whoever has the highest hand value within 21 wins.
8. If the player has hand value 21 at beginning then player wins by blackjack if the dealer's hand value is not also 21. Gets 1.5 times of the bet.
9. After all moves are done, if both hand value are equal, it's a draw.
    ''')

#main game
def game():
    global game_on, player, dealer, player_chips
    while True:
        #player 1
        player = Hand()
        player.add_a_card(deck.deal())
        player.add_a_card(deck.deal())

        #dealer
        dealer = Hand()
        dealer.add_a_card(deck.deal())
        dealer.add_a_card(deck.deal())

        #Asks player to take a reasonable bet
        take_a_bet(player_chips)

        #call function to show the cards and also player's hand value
        show_dealer_some(dealer)
        show_player(player)
        print("\nThe player hand value is {}\n".format(player.hand_value))

        #check if player's hand value is 21 or not
        if player.hand_value == 21:
            if dealer.hand_value == 21:
                return "It's a Draw!"
            else:
                player_win_blackjack()
                return

        while playing:
            #Ask player if they want to hit or stand
            hit_or_stand()
            if player.hand_value > 21:
                player_bust()
                return

        if dealer.hand_value >= 17:
            show_dealer_all(dealer)
            print("\nThe dealer hand value is {}\n".format(dealer.hand_value))

        #Dealer's move
        while dealer.hand_value < 17:
            hit(dealer)
            show_dealer_all(dealer)
            print("\nThe dealer hand value is {}".format(dealer.hand_value))
            show_player(player)
            print("\nThe player hand value is {}\n".format(player.hand_value))

        if dealer.hand_value > 21:
            dealer_bust()
            return
        elif dealer.hand_value > player.hand_value:
            dealer_win()
            return
        elif dealer.hand_value < player.hand_value:
            player_win()
            return
        else:
            return "It's a Draw!"

print('''
 -------------------------------------
|                                     |
| Welcome to the Blackjack Card Game! |
|                                     |
 -------------------------------------
        ''')
while True:
    show_rules = input("Do you want to know the rules of the game? Enter y or no: ")
    if show_rules == "y" or show_rules == "n":
        break
    else:
        print("Please enter either y or n!")

if show_rules == "y":
    rules()
    
#Asks player the number of chips he/she has.   
while True:
    try:
        total = int(input("Player: How many chips do you have? "))
        break
    except:
        print("Enter an integer value!")
player_chips = Chips(total)

while game_on:
    #call Deck() and shuffle
    deck = Deck()
    deck.shuffle()
    
    #Call game() function
    game()
    print("You have {} chips.".format(player_chips.total))
    while True:
        if player_chips.total == 0:
            print("Sorry you can't play anymore!")
            play = "n"
            break
        play = input("Do you want to play again? Enter y or n: ")
        if play == "y" or play == "n":
            break
        else:
            print("Please enter either y or n!")   
    if play == "y":
        game_on = True
        playing = True
    else:
        print("You finished the game with {} chips!".format(player_chips.total))
        game_on = False 
