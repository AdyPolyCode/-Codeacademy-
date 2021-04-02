# python 3.8

# cards module includes the cards + values to be able to play\handle the game
# random for random card choices and shuffle
# time to delay the game time a little bit
# pyinputplus to avoid some tedious input coding

# Before you look at the code I want you to know that this is not a
# 'tryhard' game I just wanted something easier to make


import cards
import random
import time
import pyinputplus as pyip

# Importing all the stuff from the cards script
CARDS = [cards.Q, cards.K, cards.J, cards.A, cards.TEN, cards.NINE, cards.EIGHT, cards.SEVEN, cards.SIX, cards.FIVE,
         cards.FOUR, cards.THREE, cards.TWO]
VALUES = cards.card_values


class Deck:

    def __init__(self, player_cards):
        self.player_cards = player_cards

    def print_cards(self):
        '''
        basically printing the cards that the player
        currently holds
        '''
        merged_cards = self.merge_cards()
        time.sleep(1)
        for r in range(len(merged_cards)):
            for c in range(len(merged_cards[0])):
                print(merged_cards[r][c], end='')
            print()

    def merge_cards(self):
        '''
        method to merge one or more listOflist card to one single listOflist
        this helps to print cards in one line
        '''
        temp = [[],
                [],
                [],
                [],
                []]
        for card in self.player_cards:
            for i in range(len(card)):
                temp[i].append(card[i][0] + ' ' * 4)
        return temp


class Player:

    def __init__(self, name, new_cards):
        self.name = name
        self.owned_cards = []
        self.owned_cards += new_cards
        self.score = 0
        self.total_wins = 0

    def clear_score(self):
        '''
        to clear/delete the players current score
        '''
        self.score = 0

    def throw_cards(self):
        '''
        to remove the players current cards
        '''
        self.owned_cards.clear()


class Dealer:

    def __init__(self, card_pack, values):
        self.card_pack = card_pack
        self.values = values

    def shuffle_cards(self):
        '''
        to shuffle the entire card pack
        '''
        return random.shuffle(self.card_pack)

    def get_value(self, player_cards):
        '''
        to loop trough the all the cards that the player is currently
        holding and then if the particular card is found then adding its
        value to the total variable
        '''
        total = 0
        for key, value in self.values.items():
            for card in player_cards:
                if key in card[2][0]:
                    if key == 'A':
                        one_or_zero = random.randint(0, 1)
                        total += value[one_or_zero]
                    else:
                        total += value
        return total

    def give_cards(self):
        '''
        to give two random cards to the player at the start of each round
        '''
        give = [random.choice(self.card_pack) for x in range(2)]
        return give

    def give_new_card(self):
        '''
        to give a new card to the player
        if the player wants to get
        '''
        choice = pyip.inputYesNo(prompt='Would you like a card?: ')
        if choice == 'yes':
            give_new = random.choice(self.card_pack)
            return give_new

    def give_turn(self):
        '''
        randomly choose a player who will start the game at the beginning
        '''
        turn = random.randint(0, 1)
        return turn

    def ready(self):
        '''
        ready check at the beginning
        '''
        print()
        rdy = pyip.inputYesNo(prompt='Are you ready?: ', blockRegexes=[
                              ('no', 'Enter \'yes\' when you will be ready.')])
        if rdy == 'yes':
            return True

    def rounds(self):
        '''
        with this method players can choose how many
        rounds they want to play
        '''
        total = pyip.inputInt(prompt='How many round do you want to play?: ', min=3, max=10)
        return total

    def round_win_check(self, name1, name2, score1, score2):
        '''
        to check if one of the players has won the round or not
        '''
        if score1 and score2:
            if score1 < score2 <= 21:
                return name2
            if score2 < score1 <= 21:
                return name1
            if score1 > 21 and score2 > 21:
                return None
            if score1 <= 21 < score2:
                return name1
            if score2 <= 21 < score1:
                return name2

    def game_win_check(self, name1, name2, score1, score2, rounds):
        '''
        to check if one of the players has won the game or not
        '''
        if rounds == 0:
            if score1 > score2:
                return name1
            else:
                return name2

    def pause(self):
        '''
        this is just a randomly made method to pasue the game
        '''
        play = pyip.inputStr(prompt='< Press ENTER to continue > ', blank=True,
                             blockRegexes=[(r'[a-zA-Z0-9]', 'ONLY ENTER!')])
        return play

    def play_again(self):
        '''
        players can choose either to play again or not
        '''
        again = pyip.inputYesNo(prompt='Do you want to play again?: ')
        return again


def getNames():
    '''
    to get each player name to be used in the main game
    '''
    a = pyip.inputStr(prompt='Player-1 enter your name: ', blockRegexes=[r'[0-9]|[!@#~$%^&*()_+\]\[\'\":/><?]'],
                      default='Enter a string not a digit!')
    b = pyip.inputStr(prompt='Player-2 enter your name: ', blockRegexes=[r'[0-9]|[!@#~$%^&*()_+\]\[\'\":/><?]'],
                      default='Enter a string not a digit!')
    return a, b


# Main function
def main():
    # Dealer
    dealer = Dealer(CARDS, VALUES)
    dealer.shuffle_cards()
    # Player objects + getName func
    name1, name2 = getNames()
    player1 = Player(name1, dealer.give_cards())
    player2 = Player(name2, dealer.give_cards())
    # Decks
    player1deck = Deck(player1.owned_cards)
    player2deck = Deck(player2.owned_cards)

    player_turn = dealer.give_turn()
    rounds = dealer.rounds()
    play = dealer.ready()
    print(f'Player1: {player1.name}, Player2: {player2.name}')
    print()
    while play:
        if dealer.game_win_check(player1.name, player2.name, player1.total_wins, player2.total_wins, rounds):
            game_winner = dealer.game_win_check(
                player1.name, player2.name, player1.total_wins, player2.total_wins, rounds)
            print()
            print(f'{game_winner} has won the game.')

            one_more_game = dealer.play_again()
            if one_more_game == 'yes':
                main()
            else:
                print('Bye...')
                break
        else:
            if dealer.round_win_check(player1.name, player2.name, player1.score, player2.score):
                print('\n' * 100)

                round_winner = dealer.round_win_check(
                    player1.name, player2.name, player1.score, player2.score)
                if round_winner:
                    print()
                    print(f'{round_winner} has won the round.')
                    time.sleep(2)
                    if round_winner == player1:
                        player1.total_wins += 1
                    else:
                        player2.total_wins += 1
                else:
                    print('It\'s a tie!')
                player1.clear_score()
                player2.clear_score()

                rounds -= 1
                if player1.owned_cards and player2.owned_cards:
                    player1.throw_cards()
                    player2.throw_cards()
                    player1.owned_cards += dealer.give_cards()
                    player2.owned_cards += dealer.give_cards()
            else:
                if player_turn == 0:
                    player1.score = dealer.get_value(player1.owned_cards)
                    print(f'{player1.name}\'s turn, Score: {player1.score}')
                    player1deck.print_cards()
                    player1_new_card = dealer.give_new_card()
                    if player1_new_card:
                        player1.owned_cards += [player1_new_card]
                        player1deck.print_cards()
                        player1.score = dealer.get_value(player1.owned_cards)
                        print(f'Your new score: {player1.score}')
                        print()
                    dealer.pause()

                    player_turn = 1
                elif player_turn == 1:
                    player2.score = dealer.get_value(player2.owned_cards)
                    print(f'{player2.name}\'s turn, Score: {player2.score}')
                    player2deck.print_cards()
                    player2_new_card = dealer.give_new_card()
                    if player2_new_card:
                        player2.owned_cards += [player2_new_card]
                        player2deck.print_cards()
                        player2.score = dealer.get_value(player2.owned_cards)
                        print(f'Your new score: {player2.score}')
                        print()
                    dealer.pause()

                    player_turn = 0


main()
