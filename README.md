# BlackJack
This is a very simplified terminal version of the blackjack game. The game for now is played between 1 player and an automated dealer.



## Rules of the game:
1. The player is given 2 cards, face-up(revealed) in the beginning.
2. The dealer is given 2 cards, one face-up(revealed) and other face-down(hidden).
3. The cards from 2-10 has face value, Jack, King, Queen has value of 10, Ace can be either 1 or 11.
4. You cannot have chips less than 10 also you cannot bet any amount less than 10.
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
