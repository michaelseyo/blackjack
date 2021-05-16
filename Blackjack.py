#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:05:13 2020

@author: Mike
"""
import random
from random import shuffle
#create BLACKJACK, play against the com. OOP? How do i incorporate classes/methods/inheritance

class Deck:
    def __init__(self):
        '''Creates an instance of a list of shuffled deck of cards'''
        self.contents = []
        
        #using OOP + list comprehension
        self.contents = [Cards(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.contents)
        
    #don't manipulate the content directly, GET them then manipulate instead    
    def getDeck(self):
        '''gets contents of the Deck in the form of a list'''
        return self.contents
    
    def draw(self):
        '''return: get the top card in the deck(aka last)'''
        try:
            return self.getDeck().pop()
        
        #when we have no more cards left to draw
        except IndexError:
            
            #recreate a new, shuffled Deck
            current = Deck()
            return self.getDeck().pop()
                        
    
#create a deck of cards (Google: use OOP and list comprehension to make life easier)
class Cards(Deck):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        #so instances of Cards have attributes of rank and suit.
    
    def getRank(self):
        return self.rank
    
    def getSuit(self):
        return self.suit
    
    def __str__(self):
        return str(self.rank) + ' of ' + str(self.suit)
        
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
  
#class of player: Deck > Cards > Player (Dealer can be in class Player)
        #can we make it such that capital is updated after every bet outcome?
        
class Player(Cards):
    def __init__(self, name, capital):
        ''' 
        input: name: str, capital: int (how much money you decide to play with) 
        creates an instance of a player
        '''
        
        self.name = name
        self.capital = capital
        self.hand = []
        #list of RANK of the cards in hand, to be check for their combination(e.g banluck)
        self.combiRank = []
        self.points = 0 #since this is an instance variable, diff instances have diff value!
        
    def __str__(self):
        return 'Name: ' + str(self.name) + ', ' + 'Capital: ' + str(self.capital)
    
    def getName(self):
        return self.name
    
    def getHand(self):
        return self.hand
    
    def getCapital(self):
        return self.capital
    
    def showHand(self):
        print(self.name, 'hand: ')
        for card in self.hand:
            
             #print card out using class Cards's __str__, since they are instances of Cards
            print(card)
           
    def draw(self):
        '''
        Uses Deck's draw method to return a drawnCard, which is appended to hand
        return: drawn card OUTCOME
        '''
               
        #need put the variables of the method, we can't put self here because Player has no 'contents' attribute, it belongs to DECK.
        drawnCard = Deck.draw(current)
        self.getHand().append(drawnCard)
        
        #count point after draw
        self.pointCounter(drawnCard)
        
        #inherrited str method from Cards class    
        print('\nYou drew:', drawnCard)
        
        #ultimately the value returned for draw is what is returned by combination method.
        return self.combination(drawnCard)
    
    def capitalMovement(self, amount):
        '''
        input: amount, an int (from bet: win/loss)
        return: str(result), the capital left 
        '''
        result = self.getCapital() - amount
        return 'Current capital: ' + str(result)
    
    def pointCounter(self, drawnCard): 
        '''
        input: drawnCard(instance of Cards class)
        Updates points based on ADDITION of drawnCard
        '''        
        #why we made list comp of INSTANCES and not print them readable, sto call the methods
        if drawnCard.getRank() in ['Jack', 'Queen', 'King']:
            self.points += 10
                
        elif drawnCard.getRank() == 'Ace': #expansion: choice of 1 or 11s
            self.points += 1
                
        else:
            self.points += int(drawnCard.getRank())
        
    
    def combination(self, drawnCard): #how to SHORTEN?
        '''
        return: result(str), used for outcome function.
        '''
        #add drawnCard to the combiRank (list of number of the cards in hand)
        self.combiRank.append(drawnCard.getRank())
        
        if len(self.combiRank) >= 2: #so we can integrate this with draw, where once 2 cards drawn, can check.
            
            if (self.combiRank[0], self.combiRank[1]) == ('Ace', 'Ace'):
                print('\nBANBAN\n')
                self.showHand()
                return 'banban'    
            
            elif (self.combiRank[0], self.combiRank[1]) in combiList:
                print('\nBANLUCK\n')
                self.showHand()
                return 'banluck'
                    
            elif self.points <= 21 and len(self.getHand()) == 5:
                print('\nWULONG\n')
                self.showHand()
                return 'wulong'
        
            elif self.points > 21 and len(self.getHand()) == 5:
                print('\nWULONG BUT EXCEED\n')
                self.showHand()
                return 'wulongExceed'
            
            elif self.points < 16:
                if type(self) == Player:
                    print('\nNot enough points!')
                return 'lacking' 
               
            elif self.points > 21: #user can hide first
                if type(self) == Player:
                    print('\nEXCEED, but dealer still dont know...')
                if type(self) == Dealer:
                    print('DEALER EXCEED!')
                return 'exceed'
                
            elif 16 <= self.points <= 21:
                return 'clear'

    def outcome(self, other, userResult, comResult): 
        #must differentiate the win type, because we running through multiplier.
        '''
        input: (self) instance of Player: user, (other)instance of Dealer: com
        return result, str win/lose/draw user against com
        '''
        
        #16<points<=21, higher points than other - win (rep in dictionary: clear, clear)
        if (userResult, comResult) == ('clear', 'clear'):
            if self.points > other.points:
                return 'win'
            elif self.points < other.points:
                return 'lose'
            elif self.points == other.points:
                return 'draw'
            
        #must follow this tuple order for Dict key.
        else:
            return outcomeDict[(userResult, comResult)] #gives value of key
        
    def capitalOutcome(self, other, result, amount, multiplierDict): 
        #how do we differentiate when player wins or dealer wins, n settle their capital?
        #printing what kind of win for user
        
        '''
        Input: result(str) and multiplierReturnsDict(Dict) of outcome map to multiplier
        return: int, bet multiplied effect.
        '''
        change = multiplierDict[result]*amount
        
        userWin = ['bbWin', 'blWin', 'wlWin', 'win']
        userLose = ['bbLose', 'blLose', 'wlLose', 'lose', 'draw']
        
        if result in userWin:    
            print()                  
            print('YOU WON: $', change)
            self.capital += change
            print('Current capital: $', self.capital)
            other.capital -= change
            print('Dealer capital: $', other.capital)
            
        elif result in userLose:        
            print()
            print('YOU LOSE: $', change)
            self.capital -= change
            print('Current capital: $', self.capital)
            other.capital += change
            print('Dealer capital: $', other.capital)
        
        

combiList = []
for rank in ['10', 'Jack', 'Queen', 'King']:
    combiList.append(('Ace', rank))
    combiList.append((rank, 'Ace'))
combiList.append(('Ace', 'Ace'))    


outcomeDict = {('clear', 'clear') : 'compare', 
               
               ('banban', 'clear'): 'bbWin', 
               ('banban', 'lacking'): 'bbWin', #lacking arises because com can't draw yet/com straight win you
               ('banban', 'banluck'): 'bbWin',                
               ('banluck', 'clear'): 'blWin',
               ('banluck', 'lacking'): 'blWin',
               ('wulong', 'clear'): 'wlWin', 
               ('wulong', 'lacking'): 'wlWin', 
               ('clear', 'wulongExceed'): 'wlWin', 
               ('clear', 'exceed'): 'win',
               
               ('clear', 'banban'): 'bbLose',
               ('lacking', 'banban'): 'bbLose',
               ('banluck', 'banban'): 'bbLose', 
               ('clear', 'banluck'): 'blLose',
               ('lacking', 'banluck'): 'blLose',
               ('clear', 'wulong'): 'wlLose', 
               ('exceed', 'wulong'): 'wlLose',
               #i won't have ('lacking', 'wulong') because i have to draw
               ('wulongExceed', 'clear'): 'wlLose',
               ('wulongExceed', 'lacking'): 'wlLose',
               ('exceed', 'clear'): 'lose',
                             
               ('banban', 'banban'): 'draw', ('banluck', 'banluck'): 'draw',
               ('exceed', 'wulongExceed'): 'draw', ('exceed', 'exceed'): 'draw'}       
        

multiplierDict = {'bbWin': 3, 'bbLose': 3, 'blWin': 2, 'blLose': 2, 'wlWin': 2, 
                  'wlLose': 2, 'win': 1, 'lose': 1, 'draw': 0}    

class Dealer(Player):
    def draw(self): #no print of drawnCard
        '''
        Uses Deck's draw method to return a drawnCard, which is appended to hand
        return: drawn card
        '''
               
        #need put the variables of the method, we can't put self here because Player has no 'contents' attribute, it belongs to DECK.
        drawnCard = Deck.draw(current)
        self.getHand().append(drawnCard)
        
        #count point after draw
        self.pointCounter(drawnCard)
        
        return self.combination(drawnCard)

    
def playGame(): #dealer is hidden until the player is done(exception: banluck/banban)
    '''main game function''' 
    #do a reset for every match
    user.points = 0
    user.hand = []
    user.combiRank = []
    com.points = 0 
    com.hand = []
    com.combiRank = []
    
    #place bet, capital left
    #2 card to each, alternating, we want to hide dealer action, thats why draw function was made return instead of print.
    amount = int(input('Place your bet: '))
    print('Dealer matches your bet.')
    user.capitalMovement(amount)
    com.capitalMovement(amount)
    user.draw()
    com.draw()
    userResult = user.draw()
        
    #announce your points once you've got your deck
    print('Your points:', user.points)
    comResult = com.draw()
    
    #testing integration of user input aft 2 cards drawn
    endGame = ['banban', 'banluck', 'wulong', 'wulongExceed']

    #unless user/com gets banban/banluck/wulong/wulongExceed; ask input
    while userResult not in endGame and comResult not in endGame:
        answer = input('Press d to draw a card, press n to pass your turn: ')
        if answer == 'd':
            userResult = user.draw()
            print('Your points:', user.points)
                       
        elif answer == 'n':
            break 
        
        else:
            print('Invalid input. Please try again!')
          
    #dealer action (if user/com get special combis, don't draw for com)
    if userResult not in endGame and comResult not in endGame:
        print('\nDealer is choosing his actions..\n')
        while com.points < 16:
            comResult = com.draw()
    
        if comResult != 'wulong':
            com.showHand()
        print('com points:', com.points)
        print('Your points:', user.points)
    result = user.outcome(com, userResult, comResult)

    #gives change in capital aft result
    user.capitalOutcome(com, result, amount, multiplierDict)

#run game:
#intro initialisation
print('Welcome to BLACKJACK')
name = input('Whats your name? ')
capital = int(input('How much money do you wanna start with? '))
print('\nNice, lets play with the com dealer\n')
user = Player(name, capital)
com = Dealer('Dealer', capital)
current = Deck()

while user.capital > 0 and com.capital > 0:           
    playGame()  
    gameInput = input('Press p to play again\nPress e to end the game: ')
    
    while gameInput != 'p' and gameInput != 'e':
        gameInput = input('Please press a valid letter: ')
    
    if gameInput == 'e':
        print('Thanks for playing!')
        break

if user.capital <= 0:
    print(user.getName, 'has no money left to play!')
    
elif com.capital <= 0:
    print('Dealer has no money left to play!')