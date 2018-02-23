from random import randint
import math
import os

# global variables
dealt_cards = {'dealer': [], 'player': []}
money = {'dealer': 100000, 'player': 1000}

def clr():
    """TO Clear dealt_card data structure"""
    global dealt_cards
    dealt_cards['dealer'] = []
    dealt_cards['player'] = []

def play():
    """Game starts from here and end here."""
    dealer()

    while True:
        try:
            # os.system('clear')
            game_in = str(raw_input('Do You want play another round\t'))
            if game_in in ['yes', 'y', 'YES', 'Y']:
                if money['player'] > 0:
                    dealer()
                else:
                    print 'No money left in your account please come back later'.upper()
                    break
            elif game_in in ['no', 'NO', 'n', 'N']:
                print "Thank for playing!!!\n"
                break
            else:
                print 'please enter correct input\n'
                continue

        except:
            print 'please enter correct input\n'

class Deck(object):
    card_number = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'King', 'Queen', 'Jack']
    card_type = [' of club', ' of spade ', ' of diamond', ' of heart']
    value = 0
    val = 'null'

    def __init__(self):
        pass

    # To get a random card from deck
    def get_card(self):
        # to generate a random int
        num = randint(0, 51)

        # to genrate card from the random number, row is seleccted by card_number[x] and coloumn by card_type[y]
        self.card = self.card_number[(num % 13)] + self.card_type[int(math.floor(num / 13))]

        # making a tuple of card and its face value
        self.val = self.card_number[(num % 13)]
        self.value = self.card_value()
        self.card_tuple = (self.card, self.value)

        # print self.card_tuple
        return (self.card_tuple)

    def card_value(self):
        if self.val == 'Ace':
            return 11
            # ace_choice()
        elif self.val in str(range(2, 11)):
            return int(self.val)
        elif self.val == 'King' or self.val == 'Queen' or self.val == 'Jack':
            return 10
        else:
            print "Invalid card"
            print self.val

# global instance of Deck object
d1 = Deck()

class Player(object):
    no_of_cards = 0
    p_choice = 'null'
    global dealt_cards
    global money

    def __init__(self, bet_money=0):
        self.bet_money = bet_money

    def player_choice(self):
        while True:
            while True:
                try:
                    self.p_choice = str(raw_input("Do you want to hit or stand? h/s\t"))
                    os.system('clear')
                    if self.p_choice == 'h' or self.p_choice == 's':
                        break
                    else:
                        print 'Enter a valid input !!!\n'
                        continue
                except:
                    print "please enter a valid input !!!\n"
                    continue

            if self.p_choice == 'h':
                dealt_cards['player'].append(d1.get_card())

                if check_bust('player'):
                    # to deduct the bet_money from player's account
                    debit_money('player', 'dealer', self.bet_money)
                    break
                else:
                    # showing cards as in case of bust check_bust will show the cards
                    self.p_show_cards()

            elif self.p_choice == 's':
                check_win(self.bet_money)
                break

            elif self.p_choice == 'null':
                print "you have reached null choice"
            else:
                print "you have reached else of player_choice"

    def p_show_cards(self):
        show_card('player', 52)
        return sum_b(dealt_cards['player'])


def dealer():
    clr()
    sum_dealer = sum_player = 0
    global dealt_cards

    os.system('clear')
    print "Hey There ! I'm dealer I'll dealt cards for you\n"
    # instance of object Deck and player for single player
    print 'Initially Money Given from house to {x}\nYou have {y} amount now'.format(x='player',
                                                                                    y=money['player']).title()

    while True:
        try:
            b_money = int(raw_input("Enter your bet money. Be Carefull!!!\t"))
            if 0 < b_money <= money['player']:
                p1 = Player(b_money)
            else:
                print "please enter money within [0-{x}]\n".format(x=money['player'])
                continue
            break
        except ValueError:
            print 'Please an integer value\n'

    print 'Dealting cards......\n'
    for p in range(0, 2):
        dealt_cards['dealer'].append(d1.get_card())
        dealt_cards['player'].append(d1.get_card())

    # to print Dealer first card
    times_i_want_to_print = 1
    for e in dealt_cards['dealer']:
        if times_i_want_to_print > 0:
            print "one of the cards of dealer is {x}".format(x=e[0]).title()
            times_i_want_to_print -= 1

        # Initally show both cards of player
    p1.p_show_cards()
    # Intial check is player is busted or has won a blackjack
    if check_bust('player'):
        # to deduct the bet_money from player's account
        debit_money('player', 'dealer', bet_money)

        return

    if blackjack('player'):
        # to deduct the bet_money from dealer's account
        debit_money('dealer', 'player', bet_money)
        print 'Current Money of {x} is : {y}'.format(x='player', y=money['player'])

        return

    # to check to what player has chosen
    p1.player_choice()
    print "Round over"
    return


def check_win(bet_money):
    # we will reach to check_win only when player choose to stand
    # and now it time that house dealer will show its cards
    # and check who has won

    while sum_b(dealt_cards['dealer']) < 17:
        dealt_cards['dealer'].append(d1.get_card())

    if check_bust('dealer'):
        # to deduct the bet_money from dealer's account
        debit_money('dealer', 'player', bet_money)
        return
    # to check how has won on basis of sum of their card values.
    if sum_b(dealt_cards['dealer']) < sum_b(dealt_cards['player']):
        os.system('clear')
        # to deduct the bet_money from dealer's account
        show_card('dealer')
        show_card('player')
        print 'You won this round\n'.title()
        debit_money('dealer', 'player', bet_money)




    elif sum_b(dealt_cards['dealer']) == sum_b(dealt_cards['player']):

        os.system('clear')
        show_card('dealer')
        show_card('player')
        print 'this round is tie\n'.title()
        print 'Current Money of {x} is : {y}'.format(x='player', y=money['player'])



    else:
        os.system('clear')
        # to deduct the bet_money from player's account

        show_card('dealer')
        show_card('player')
        print 'Dealer has won this round\n'.title()
        debit_money('player', 'dealer', bet_money)


def debit_money(whoes, to_whom, how_much):
    """To debit money amount 'how_much' from 'whoes' and add to 'to_whom' """
    global money
    money[whoes] -= how_much
    money[to_whom] += how_much

    # recharge dealer if his money become zero
    if money['dealer'] <= 0:
        money['dealer'] += 10000
    print 'Current Money of {x} is : {y}'.format(x='player', y=money['player'])


def check_bust(who):
    if sum_b(dealt_cards[who]) > 21:
        show_card(who)
        print '[{x} is busted. {x} has lost his bet money!!!]\n'.format(x=who).title()
        # might be errorness in multiplayer re-check logic at that time
        return True


def blackjack(who):
    if sum_b(dealt_cards[who]) == 21:
        print '[{x} has won a BLACKJACK!!!\n]'.format(x=who).title()
        return True

def sum_b(list):
    sum_all = 0
    for element in list:
        sum_all += element[1]
    return sum_all

def show_card(whoes, no_of_cards=52):
    s_cards = []
    for e in dealt_cards[whoes]:
        if no_of_cards > 0:
            s_cards.append(e[0])
            no_of_cards -= 1
    print '\n'
    print whoes, s_cards
    print 'Current Sum of {w} is {x}\n'.format(x=sum_b(dealt_cards[whoes]), w=whoes).title()

# Your Game starts from here
play()
