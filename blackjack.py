'''
DOCSTRING: BlackJack game
INPUT: The goal of the game is to beat the dealer's hand without going over 21.
       Each player starts with two cards, one of the dealer's cards is hidden
       until the end. If you go over 21 you bust, and the dealer wins
       regardless of the dealer's hand.
OUTPUT: Calculation of the value of the cards
'''


import time
import random

suits = ('Hearts', 'Diamons', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
          'Ace': 11}

playing = True

print('LET`S START THE GAME!!!')
player_name = input('Enter your name: ')
deposit = int(input(f'{player_name}, What`s your Deposit? '))
# INTRO TO THE GAME
def intro():

    # Intro to the game
    print('Welcome to BlackJack game \n'
          'The goal of the game is to beat the dealer`s hand without going over 21.\n'
          'Each player starts with two cards, one of the dealer`s cards is hidden \n'
          'until the end. If you go over 21 you bust, and the dealer wins \n'
          'regardless of the dealer`s hand.')
    print('\n')
    time.sleep(3)


class Card:
    '''
    DOCSTRING: Card Class
               Colling full list of 'Ranks' and 'Suits'
    '''
    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks

    def __str__(self):
        return f'{self.ranks} of {self.suits}'


class Deck:
    '''
    DOCSTRING: Deck Class
               Creating Full deck of cards and
               picking a card from the deck ('deal' function)
    '''
    def __init__(self):
        self.new_deck = (list(set()))   # creating a list of full deck of cards
        self.suits = ''
        self.ranks = ''
        self.deck = []
        self.single_card = []

    def __str__(self):
        return self.new_deck

    # creating full deck of cards
    def full_deck(self):
        while True:
            while (len(self.new_deck)) != 52:
                self.suits = random.choice(suits)
                self.ranks = random.choice(ranks)
                self.deck = []
                self.new_card = ''
                self.single_card = []

                # verifing if the card is not in the deck of cards
                if (list(f'{self.ranks} of {self.suits}')) not in self.new_deck:
                    # Creating a card
                    new_card = self.deck + (list('{} of {}'.format(self.ranks, self.suits).split()))
                    new_deck = ' '.join(new_card)
                    self.new_deck.append(new_deck)
                    self.new_deck = list(set(self.new_deck))
            break
        return self.new_deck

    def deal(self):
        self.single_card = random.choice(self.new_deck)
        self.new_deck.remove(self.single_card) # to make sure card is not repeated
        return self.single_card


class OnHand:
    global player_name
    '''
    DOCSTRING: OnHand Class
               Calculation of the cards from hand of the player,
               Adjusting 'Ace' situation and BlackJack situation
    '''
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.card_string = 0
        self.card_value = []

    def add_card(self, card):
        self.cards.append(card)

        # taking value of the card
        self.card_string = ''
        for i in card:
            self.card_string += i
        self.card_value = self.card_string.split()[0]

        # finding value in the dictionary and adding to the
        # total value of the cards
        self.value += values[self.card_value]

        if self.card_value == 'Ace':
            self.aces += 1

    def adjust_ace(self):
        # Adjusting ACE situation
        if self.value > 21 and self.aces: # we can use as well "self.aces > 0"
            self.value -= 10
            self.aces -= 1


class Chips:
    global deposit
    '''
      DOCSTRING: Chips Class
                 Calculation of the winning_BET and lose_BET of the player,
                 Adjusting player balance
    '''
    def __init__(self):
        self.balance = deposit
        self.bet = 0


    def __str__(self):
        return f'{player_name}, Your balance is : $ ' + str(self.balance)

    def win_bet(self):
        self.balance += self.bet

    def lose_bet(self):
        self.balance -= self.bet


# FUNCTION DEFINING

# Taking a bet from the player
def take_bet(beting):
    while True:
        try:
            beting.bet = int(input(f'{player_name}, How much would you like to bet? '))
            print('\n')

        except ValueError:
            print(f'Sorry {player_name}, a bet must be an integer!')
            continue
        if beting.bet > beting.balance:
            print(f'{player_name}, Your Balance is to low to make this BET!!!\n'
                  f'You can`t bet more than: $ {beting.balance}')
        else:
            break

# Taking HIT from the player
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_ace()


# Controlling Hit or Stand from the player
def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input(f"{player_name}, Would you like to Hit or Stand? Enter 'h' or 's' ").lower()

        if x.startswith('h'):
            hit(deck, hand)  # hit() function defined above


        elif x.startswith('s'):
            print('\n')
            print(f"{player_name} stands. Dealer is playing. ")
            playing = False

        else:
            print("Sorry, please try again, 'h' or 's' ")
            continue
        break


# Initial game with Dealer card Hidden
def show_some(player, dealer):
    print('\nDealer`s Hand: ')
    print('<card is hidden>')
    print(dealer.cards[1], '\n')
    print(f'{player_name} cards: ', *player.cards, sep='\n  ')
    print('\n')


# Situation when all cards are shown and value is calculated
def show_all(player, dealer):
    print('\n Dealer`s Cards: ', *dealer.cards, sep='\n  ')
    # * symbol is used to print every item in a collection
    # and the sep='\n ' argument prints each item on a separate line
    print('Dealer Value = $', dealer.value)
    print(f'\n{player_name} Cards: ', *player.cards, sep='\n  ')
    print(f'{player_name} cards Value =  ', player.value)



def push(player, dealer):
    print(f'\nDealer and {player_name} TIE! It`s a Push.')

###################### GAME ITSELF #############################

# Set up Player chips, to be able to save the amount deposit
player_chips = Chips()

def game_itself():
    global player_chips
    '''
    DOCSTRING: Game Logic
               Implementing all classes and function all together
    '''
    if player_chips.balance == 0:
        print(f'{player_name}, You don`t have money to bet.')
        new_deposit = (input('Would you like to deposit? Yes or No ')).lower()
        if new_deposit.startswith('y'):
            player_chips.balance = int(input(f'{player_name}, What`s your Deposit? '))
        elif new_deposit.startswith('n'):
            print('Thank`s for playing Black Jack')
            quit()
    # Creating full deck of cards
    deck = Deck()
    deck.full_deck()

    # Take a bet from the player
    take_bet(player_chips)

    # Set up the Player's cards
    player = OnHand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())

    # Dealer cards
    dealer = OnHand()
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    # Showing player cards but not 1 one of the dealer
    show_some(player,dealer)

    # recall this variable from our hit_or_stand function
    while playing:

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        player.adjust_ace()
        dealer.adjust_ace()
        if player.value > 21:
            show_all(player, dealer)
            print(f'{player_name} Bust!!!')
            player_chips.lose_bet()
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        while dealer.value < 17:
            hit(deck, dealer)

            # Show all cards
            show_some(player,dealer)

            # Run different winning scenarios
        if dealer.value > 21:
            show_all(player,dealer)
            print('\n')
            print('Dealer Bust!!!')
            player_chips.win_bet()

        elif dealer.value > player.value:
            show_all(player,dealer)
            print('\n')
            print('Dealer Won!!!')
            player_chips.lose_bet()

        elif dealer.value < player.value:
            show_all(player,dealer)
            print('\n')
            print(f'{player_name} Won!!!')
            player_chips.win_bet()

        else:
            push(player, dealer)

        # Inform Player of their chips total
    print(f'\n{player_name}, Your balance is:  $ {player_chips.balance}\n')
    replay()


def replay():
    global playing

    replay = input(f'{player_name}, do you want to play again? Yes or No ').lower()
    if replay.startswith('y'):
        playing = True # To restart the while loop from (game itself)
        game_itself()

    elif replay.startswith('n'):
        print('Thank`s for playing Black Jack')
        quit()

# PLAYING THE GAME
intro()
game_itself()
