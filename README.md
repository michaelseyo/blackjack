# blackjack
A simple text-based game to apply what I've learnt in the online course from MIT: Introduction to Computer Science and Programming in Python that I took back in June 2020.

This is against a randomized computer player, based on the random module. 
Players have an initial amount of money that they start with, and they choose to bet a certain amount for each round. There are several outcomes for every round (this is based on the Singaporean adaptation of the cardgame Blackjack); 1-3 are special combinations. 1 is the highest tier, 2/3 I'm not very sure which comes first.

1. Banban (Double Ace: where you get 2 Aces; 3x multiplier to your initial bet) 
2. Banluck (Blackjack: where you get an Ace and Jack/Queen/King; 2x multiplier to your initial bet in both ways: win/lose) 
3. Wulong (When you are able to draw 5 cards and it is less than or equal to 21; 2x multiplier to your initial bet)
4. Exceed (When you exceed 21 points for total number obtained; 1x multiplier of loss)
5. Win (When you get more points than the computer for a non-special combination; 1x multiplier of win)
6. Draw (When same points OR both exceeds OR both same-tier special combination; no loss/win)

Player can continue to play as long as there is adequate money.
