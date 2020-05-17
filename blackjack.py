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
    
    #Lose half of the bet. Called when player doesn't like first 2 cards at hand
    def surrender(self):
        self.total -= self.bet/2

#To determine if player's turn and game ended or not
player_playing = True
game_on = True

#Ask player the amount he wants to bet
def take_a_bet(chip):
    while True:
        try:
            chip.bet = int(input("Enter the amount you want to bet: "))
        except:
            print("The amount must be an integer value!")
        else:
            if chip.bet < 10:
                print("Sorry. The minimum you can bet is 10!")
            elif chip.bet > chip.total:
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
    print("<< Card Hidden >>")
    print(dealer.hand_cards[1])

#Show all cards of dealer
def show_dealer_all(dealer):
    print("\nThe dealer has:")
    for card in dealer.hand_cards:
        print(card)

move = 0
#Askes player if he wants to take a card from deck or end turn
def player_moves(player):
    global player_playing, choice, move, hand1, hand2
    while True:
        if move == 0:
            #At player's initial move, this is asked
            choice = input("Do you want to hit, stand, double down or surrender? Enter 'h', 's', 'dd' or 'sur': ")
            if choice == "h" or choice == "s" or choice == "sur" or choice == "dd":
                move = 1
                break
            else:    
                print("Please enter either 'h', 's', 'dd' or 'sur'!")
        else:
            #At player's remaining moves, this is asked
            choice = input("Do you want to hit or stand? Enter 'h' or 's': ")
            move = 2
            if choice == "h" or choice == "s":
                break
            else:    
                print("Please enter either 'h' or 's'!")
        
    if choice == "h":
        hit(player)
        player.adjust_for_ace()
        show_player(player)
        return
    elif choice == "dd" and move == 1:
        hit(player)
        player.adjust_for_ace()
        player_chips.bet *= 2
        show_player(player)
        player_playing, hand1, hand2 = False, False, False
        return
    else:
        player_playing, hand1, hand2 = False, False, False

#takes a card from deck for the person's turn in account
def hit(person):
    person.add_a_card(deck.deal())

#functions (4 below) to determine if player won or lost
def player_win():
    print("Player has won the round!")
    player_chips.win_bet()

def player_bust():
    player_chips.lose_bet()

def player_win_blackjack():
    player_chips.blackjack_win()

def dealer_win():
    print("Dealer has won the round!")
    player_chips.lose_bet()

def dealer_bust():
    print("Player has won the round!")
    player_chips.win_bet()

def win_check(player):
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
        print("It's a Draw!")
        return

def rules():
    print('''
The rules of the game are given below:
1. The player is given 2 cards, face-up(revealed) in the beginning.
2. The dealer is given 2 cards, one face-up(revealed) and other face-down(hidden).
3. The cards from 2-10 has face value, Jack, King, Queen has value of 10, Ace can be either 1 or 11.
4. You cannot have chips less than 10 and also you cannot bet any amount less than 10.
5. The player goes first. Has option to hit(take 1 card from deck), stand(end turn), double down(take only 1 more card 
   from deck, double the bet and end turn) or surrender(forfeit the game).
6. If both initial cards of player have same value, then player has option to split hand into 2 and play with equal initial
   bet on each hands, essentially doubling the bet.
7. If the player doesn't like the initial two cards, then has option to surrender and get back half of the bet amount.
8. The dealer will have to take cards from deck until hand value becomes atleast 17.
9. If the hand value is more than 21 then it is 'bust'. Meaning the other person wins.
10. Whoever has the highest hand value within 21 wins.
11. If the player has hand value 21 at beginning and if the dealer's hand value is not 21 then player wins by blackjack.
    Player gets 1.5 times of the bet. Otherwise, it's a draw.
12. After all moves are done, if both hand value are equal, it's a draw.
    ''')

#main game
def game():
    global game_on, player, dealer, player_chips, move
    while True:
        #player
        player = Hand()
        #Add two cards from the deck for player
        player.add_a_card(deck.deal())
        player.add_a_card(deck.deal())

        #dealer
        dealer = Hand()
        #Add two cards from the deck for dealer
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
                print("It's a Draw!")
                return
            else:
                player_win_blackjack()
                print("Player has won the round by blackjack!")
                return

        card1 = player.hand_cards[0]
        card2 = player.hand_cards[1]
        
        #Asked if player wants to split or not
        if value[card1.rank] == value[card2.rank]:
            while True:
                ask = input("Do you want to split? Enter y or n: ")
                if ask == "y" or ask == "n":
                    break
            else:
                print("Please enter either y or n!")
            
            #The following code occurs when player split's hand
            if ask == "y":
                #1st hand
                player_hand1 = Hand()
                player_hand1.add_a_card(card1)
                player_hand1.add_a_card(deck.deal())
                #2nd hand
                player_hand2 = Hand()
                player_hand2.add_a_card(card2)
                player_hand2.add_a_card(deck.deal())

                hand1, hand2 = True, True
                surrendered1, surrendered2 = False, False
                dd1, dd2, bj1, bj2 = False, False, False, False
                print("\nThe player has splitted their hand and now has 2 hands to play with.")

                show_dealer_some(dealer)
                show_player(player_hand1)
                print("\nThe player's 1st hand value is {}".format(player_hand1.hand_value))
                show_player(player_hand2)
                print("\nThe player's 2nd hand value is {}\n".format(player_hand2.hand_value))

                if player_hand1.hand_value == 21:
                    if dealer.hand_value == 21:
                        pass
                    else:
                        player_win_blackjack()
                        bj1 = True
                    hand1 = False

                if player_hand2.hand_value == 21:
                    if dealer.hand_value == 21:
                        pass
                    else:
                        player_win_blackjack()
                        bj2 = True
                    hand2 = False
                
                #Actions for the 1st hand
                move = 0
                print("<< 1st Hand >>")
                while hand1:
                    player_moves(player_hand1)
                    if player_hand1.hand_value > 21:
                        player_bust()
                        hand1 = False
                
                    #Checks if player surrendered or not
                    if choice == "sur":
                        player_chips.surrender()
                        surrendered1 = True
                        hand1 = False
                    elif choice == "h":
                        print("\nThe player's 1st hand value is {}".format(player_hand1.hand_value))
                    elif choice == "dd":
                        print("\nThe player's 1st hand value is {}".format(player_hand1.hand_value))
                        hand1, dd1 = False, True
                    elif choice == "s":
                        print("Player's 1st hand move has ended!")
                        hand1 = False
            
                if player_hand2.hand_value != 21:
                    hand2 = True

                #Actions for the 2nd hand
                move = 0
                print("\n<< 2nd Hand >>")
                show_player(player_hand2)
                print("\nThe player's 2nd hand value is {}\n".format(player_hand2.hand_value))
                while hand2:
                    player_moves(player_hand2)
                    if player_hand2.hand_value > 21:
                        player_bust()
                        hand2 = False

                    if choice == "sur":
                        player_chips.surrender()
                        surrendered2 = True
                        hand2 = False
                    elif choice == "h":
                        print("\nThe player's 2nd hand value is {}\n".format(player_hand2.hand_value))
                    elif choice == "dd":
                        print("\nThe player's 2nd hand value is {}\n".format(player_hand2.hand_value))
                        hand2, dd2 = False, True
                    elif choice == "s":
                        print("Player's 2nd hand move has ended!")
                        hand2 = False

                if dealer.hand_value >= 17:
                    show_dealer_all(dealer)
                    print("\nThe dealer hand value is {}\n".format(dealer.hand_value))

                #Dealer's move
                while dealer.hand_value < 17:
                    hit(dealer)
                    show_player(player)
                    print("\nThe player's 1st hand value is {}".format(player_hand1.hand_value))
                    show_player(player_hand2)
                    print("\nThe player's 2nd hand value is {}".format(player_hand2.hand_value))
                    show_dealer_all(dealer)
                    print("\nThe dealer hand value is {}\n".format(dealer.hand_value))
                
                #Check each hand to decide who won
                print("<< 1st Hand >>")
                if player_hand1.hand_value > 21:
                    print("Dealer has won the round!")
                elif surrendered1:
                    print("Player surrendered. Half of the bet was returned!")
                elif bj1:
                    print("You won your first hand by blackjack!!!")
                else:
                    if dd2:
                        player_chips.bet = player_chips.bet / 2
                    win_check(player_hand1)
                    if dd2:
                        player_chips.bet = player_chips.bet * 2
                print("<< 2nd Hand >>")
                if player_hand2.hand_value > 21:
                    print("Dealer has won the round!")
                elif surrendered2:
                    print("Player surrendered. Half of the bet was returned!")
                elif bj2:
                    print("You won your second hand by blackjack!!!")
                else:
                    if dd1:
                        player_chips.bet = player_chips.bet / 2
                    win_check(player_hand2)
                return
        
        #following code occurs when player doesn't split hand
        while player_playing:
            #Ask player if they want to hit or stand
            player_moves(player)
            if choice == "h":
                print("\nThe player hand value is {}\n".format(player.hand_value))
            if player.hand_value > 21:
                player_bust()
                print("\nThe player hand value is {}\n".format(player.hand_value))
                print("Dealer has won the round!")
                return
            elif choice == "dd":
                print("\nThe player hand value is {}\n".format(player.hand_value))
                print("The player's turn has ended.")
                
        #Checks if player surrendered or not
        if choice == "sur":
            player_chips.surrender()
            print("\nYou have surrendered the game. Half of the bet amount was returned to you.")
            return 

        if dealer.hand_value >= 17:
            show_dealer_all(dealer)
            print("\nThe dealer hand value is {}\n".format(dealer.hand_value))

        #Dealer's move
        while dealer.hand_value < 17:
            hit(dealer)
            show_player(player)
            print("\nThe player hand value is {}".format(player.hand_value))
            show_dealer_all(dealer)
            print("\nThe dealer hand value is {}\n".format(dealer.hand_value))
        
        #To check whether player or dealer wins
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
            print("It's a Draw!")
            return

print('''
 -------------------------------------
|                                     |
| Welcome to the Blackjack Card Game! |
|                                     |
 -------------------------------------
        ''')
while True:
    show_rules = input("Do you want to know the rules of the game? Enter y or n: ")
    if show_rules == "y" or show_rules == "n":
        break
    else:
        print("Please enter either y or n!")

if show_rules == "y":
    rules()
    
#Asks player the number of chips he/she has.   
while True:
    try:
        total = int(input("Player: How many chips do you have? (Preferably 100): "))
        if 0 <= total < 10:
            print("You cannot play the game with less that 10 chips!")
            continue
        elif total < 0:
            print("Please enter a positive value!")
            continue
        else:
            break
    except:
        print("Enter an integer value!")

player_chips = Chips(total)

while game_on:
    #call Deck() and shuffle
    deck = Deck()
    deck.shuffle()
    deck.shuffle()
    move = 0
    #Call game() function
    game()
    print("\nYou have {} chips.\n".format(player_chips.total))

    if player_chips.total < 10:
        print("Sorry, you can't play anymore!")
        break

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
        player_playing = True
    else:
        print("You finished the game with {} chips!".format(player_chips.total))
        game_on = False 
