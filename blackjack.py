suit_list = ('clubs','spade','hearts','diamonds')
rank_list = ('ace','two','three','four','five','six','seven','eight','nine','ten','jack','king','queen')
value = {'ace':11,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'jack':10,
         'king':10,'queen':10}

from random import shuffle

class Card():
    '''
    card class
    '''
    def __init__(self,suit,rank):
        self.suit = suit.lower()
        self.rank = rank.lower()
        self.value = value[self.rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck():
    '''
    deck class
    '''
    def __init__(self):
        self.card_deck = []
        for suit in suit_list:
            for rank in rank_list:
                self.card_deck.append(Card(suit,rank))

    def shuffle_deck(self):
        shuffle(self.card_deck)

    def deal_card(self):
        try:
            card = self.card_deck.pop(0)
        except:
            return 0
        else:
            return card

    def __len__(self):
        return len(self.card_deck)

class Dealer():
    '''
    computer dealer
    '''
    def __init__(self):
        self.amount = 10000

    def withdraw_amount(self,bet):
        self.amount -= bet

    def add_winnings(self,win):
        self.amount += win

    def current_sum(self,card_set):
        result = 0
        if type(card_set) == type([]):
            if len(card_set) == 0:
                pass
            else:
                result = self.calculate_sum(card_set)
        else:
            if card_set == 0:
                pass
            else:
                result = self.calculate_sum(card_set)
        return result

    def calculate_sum(self,card_set):
        result = 0
        for card in card_set:
            if card != 0:
                if card.rank == 'ace':
                    if (result+card.value) > 21:
                        result+=1
                    else:
                        result += card.value
                else:
                    result+=card.value
        return result

    def get_amount(self):
        return self.amount

class Player():
    '''
    player class
    '''
    def __init__(self):
        self.balance = 10000

    def place_bet(self):
        while True:
            try:
                stake = int(input(f'Player enter the amount you want to bet?(between 1 & {self.balance})'))
            except:
                print('incorrect bet value')
            else:
                if 0 < stake <= self.balance:
                    self.balance -= stake
                    break
                else:
                    print('incorrect bet value')
        return stake

    def current_sum(self,card_set):
        result = 0
        if type(card_set) == type([]):
            if len(card_set) == 0:
                pass
            else:
                result = self.calculate_sum(card_set)
        else:
            if card_set == 0:
                pass
            else:
                result = self.calculate_sum(card_set)
        return result

    def calculate_sum(self,card_set):
        result = 0
        for card in card_set:
            if card != 0:
                if card.rank == 'ace':
                    if (result+card.value) > 21:
                        result+=1
                    else:
                        result += card.value
                else:
                    result+=card.value
        return result

    def add_winnings(self,win):
        self.balance += win

    def get_balance(self):
        return self.balance

class BlackJack():
    '''
    game logic
    '''
    def __init__(self):
        self.game_deck = Deck()
        self.game_deck.shuffle_deck()
        self.computer = Dealer()
        self.player1 = Player()

    def start_game(self):
        game_round = 0
        while True:
            if len(self.game_deck) == 0:
                break
            player_deck = []
            dealer_deck = []
            bet = 0
            game_round +=1
            print(f'\nROUND {game_round}\n---------\n')
            bet = self.player1.place_bet()
            self.computer.withdraw_amount(bet)
            bet *= 2
            for i in range(0,2):
                dealer_deck.append(self.game_deck.deal_card())
                player_deck.append(self.game_deck.deal_card())
            print("dealer's hand:")
            print(f"['{dealer_deck[0]}']")
            print("player's hand")
            print(list(map(lambda card:str(card),player_deck)))
            print(f'current sum = {self.player1.current_sum(player_deck)}')
            while True:
                choice = self.player_choice()
                if choice == 'hit':
                    result,player_deck = self.perform_hit(player_deck,self.game_deck,self.player1)
                    if result == 0:
                        self.decide_winner(self.player1.current_sum(player_deck),self.computer.current_sum(dealer_deck))
                        break
                    elif result == 21:
                        self.perform_add_hand(self.player1,bet)
                        self.announce_winner('Player 1',game_round,player_deck)
                        break
                    elif result < 21:
                        continue
                    else:
                        self.perform_bust(self.computer,bet)
                        print(f'Player 1 lost round {game_round}')
                        self.display_hand(player_deck,dealer_deck)
                        break
                else:
                    while True:
                        comp,dealer_deck = self.perform_hit(dealer_deck,self.game_deck,self.computer)
                        if comp == 0:
                            self.decide_winner(self.player1.current_sum(player_deck),self.computer.current_sum(dealer_deck))
                            break
                        elif comp == 21:
                            self.perform_add_hand(self.computer,bet)
                            self.announce_winner('Dealer',game_round,dealer_deck)
                            break
                        elif comp < 21:
                            if comp >= 17:
                                self.decide_winner(self.player1.current_sum(player_deck),self.computer.current_sum(dealer_deck))
                                break
                            else:
                                continue
                        else:
                            self.perform_bust(self.player1,bet)
                            print(f'Dealer lost round {game_round}')
                            self.display_hand(player_deck,dealer_deck)
                            break
                    break
        self.end_game(self.player1,self.computer)

    def player_choice(self):
        while True:
            choice = input('Player: hit or stay ?')
            if choice.lower() == 'hit' or choice.lower() == 'stay':
                break
        return choice

    def perform_hit(self,card_set,deck,gamer):
        card = deck.deal_card()
        if card == 0:
            return (0,0)
        else:
            card_set.append(card)
            res = gamer.current_sum(card_set)
            return (res,card_set)

    def perform_add_hand(self,gamer,bet):
        gamer.add_winnings(bet)

    def perform_bust(self,gamer,bet):
        gamer.add_winnings(bet)

    def announce_winner(self,name,game_round,card_deck):
        print(f'{name} won round {game_round} with winning hand')
        print(list(map(lambda card:str(card),card_deck)))

    def decide_winner(self,player,dealer):
        if player > dealer:
            print('Player 1 won the round')
        else:
            print('Dealer won the round')

    def display_hand(self,player_deck,dealer_deck):
        print('Player 1 deck - ',*player_deck)
        print('Dealer deck - ',*dealer_deck)

    def end_game(self,player,dealer):
        player1 = player.get_balance()
        player2 = dealer.get_amount()
        if player1 > player2:
            name = 'Player 1'
            prize = player1 - 10000
        elif player1 < player2:
            name = 'Dealer'
            prize = player2 - 10000
        else:
            name = 'No one'
            prize = 0
        print(f'The overall winner is the {name} with winnings of {prize}USD')
        print('GAME OVER')

if __name__ = "__main__":
    bj = BlackJack()
    bj.start_game()
