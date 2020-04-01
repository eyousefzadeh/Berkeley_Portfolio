
class Deck:

    def __init__(self, cards = []):
        self.cards=cards

    def create_deck(self):
        """Creates the deck to play"""
        # suit = '♠♥♦♣'   Commenting out original suit since may run into encoding errors in command prompt since these are non-ascii characters
        suit = "SHDC"  #creating suits in single letter initials to make ASCII friendly
        #S = Spades, H = hearts, D = diamonds, C = clubs
        num= range(2,11)
        face=10
        ace = 11
        cardface=[(val, suit1) for val in num for suit1 in suit]*6 + [(10, suit1) for suit1 in suit]*18 + [(ace, suit1) for suit1 in suit]*6
        self.cards = [x[0] for x in cardface]



    def shuffle_deck(self):
        """ Shuffles deck that was created"""
        from random import shuffle
        shuffle(self.cards)


class Deal:

    def __init__ (self, pc = [], d= [], p = [], p_val = [], d_val=[], s1 = [], s2 = [], chips=1000, bet = 1, ace = 11, true_count = 0, main = 1):
        self.pc = pc
        self.d = d
        self.p = p
        self.s1 = s1
        self.s2 = s2
        self.chips = chips
        self.bet = bet
        self.ace = ace
        self.true_count = true_count
        self.p_val=p_val
        self.d_val=d_val
        self.main = main

    def clear(self):
        """Clears cards after every hand is dealt."""
        self.p.clear()
        self.d.clear()
        self.s1.clear()
        self.s2.clear()

    def bet_initial(self):
            """Main betting screen that comes at the beginning of each new hand."""
            while True:
                try:
                    print("Current bet: ", self.bet)
                    bet_screen = int(input("Enter bet:\n1)Current bet 2)Enter bet 3)Leave table"))
                    if bet_screen == 1:
                        self.bet = self.bet
                        break
                    if bet_screen == 2:
                        while True:
                            try:
                                    self.bet = int(input("Enter new bet: "))
                                    if self.bet>=1 and self.bet<=self.chips:
                                        break
                                    if self.bet < 1:
                                        print("Bet must be at least 1 chip")
                                    if self.bet>self.chips:
                                        print("Cannot bet more than chip count.")


                            except ValueError:
                                print("Bet must be a valid number")
                        break
                    if bet_screen == 3:
                        self.main = 0
                        break
                    if bet_screen <1 or bet_screen>3:
                        print("Invalid entry. Please enter a valid option.")
                except ValueError:
                    print("Invalid entry. Please enter a valid number.")

    def ace_adjustment(self,x):
        """Ace adjustment function reduces the value of the Ace from 11 to 1 if the card hand is greater than 21"""
        i=0
        while i < len(x):
            if x[i]==11 and sum(x)>21:
                x[i]=1
                i= i+1
            else:
                i+=1

    def game_over(self):
        """Game over screen"""
        print("Out of chips. Thanks for playing!")
        self.bet = 0
    def deal_card(self,x):
        """This is the main game engine.
            Cards are dealt to player and dealer and player has several options from there.
            """

        while self.main == 1:
            if self.chips == 0:
                self.game_over()
                self.main = 0
            from random import shuffle
            p=[]
            d=[]
            print("Chip count: ", self.chips)
            print("Cards left in deck: ", len(x.cards))
            if len(x.cards)<12:
                x.create_deck()
                x.shuffle_deck()
            self.clear()
            self.bet_initial()
            if self.bet <= 0:
                self.game_over()
                self.main = 0
            if self.main == 1:
                self.d.append(x.cards.pop(0))
                self.p.append(x.cards.pop(0))
                self.p.append(x.cards.pop(0))
                print("Dealer total: ", sum(self.d))
                self.display_card(self.d[0])
                print("Player total: ", sum(self.p))
                self.initial_player_display_card(self.p[0],self.p[1])


            game = 1


            while game ==1 and self.main ==1:
                print("Current bet: ", self.bet)
                if sum(self.p) == 21 and sum(self.d) !=21 and len(self.p)==1:
                    print("Blackjack!")
                    self.chips += self.bet*1.5
                    game = 0
                    break

                if sum(self.d) == 21 and sum(self.p) !=21:
                    print("House blackjack. You lost.")
                    self.chips += self.bet*1.5
                    game = 0
                    break

                try:
                    a = input("What would you like to do? 1) Hit 2) Stand 3) Double Down 4) Split")

                    if a == "1":
                        self.p.append(x.cards.pop(0))
                        self.ace_adjustment(self.p)
                        self.display_card(self.p[-1])
                        print("Dealer total: ", sum(self.d))
                        print("Player total: ", sum(self.p))


                        if sum(self.p)>21:
                            print("Bust")
                            self.chips -= self.bet
                            game = 0
                            break


                    if a == "2":
                        while sum(self.d)<=21:
                            self.d.append(x.cards.pop(0))
                            self.ace_adjustment(self.d)
                            self.display_card(self.d[-1])
                            print("Dealer total: ", sum(self.d))
                            print("Player total: ", sum(self.p))
                            if sum(self.d)>sum(self.p) and sum(self.d)>=17 and sum(self.d)<=21:
                                print("You lost.")
                                game = 0
                                self.chips -= self.bet
                                break
                            if sum(self.d)==sum(self.p) and sum(self.d)>=17:
                                print("Push.")
                                game = 0
                                break
                            if sum(self.d)>21:
                                print("You won.")
                                game =0
                                self.chips += self.bet
                                break

                    if a == "3":
                        self.p.append(x.cards.pop(0))
                        self.ace_adjustment(self.p)
                        self.display_card(self.p[-1])
                        print("Dealer total: ", sum(self.d))
                        print("Player total: ", sum(self.p))
                        while sum(self.d)<=21:
                            self.d.append(x.cards.pop(0))
                            self.ace_adjustment(self.d)
                            self.display_card(self.d[-1])
                            print("Dealer total: ", sum(self.d))
                            print("Player total: ", sum(self.p))
                            if sum(self.d)>sum(self.p) and sum(self.d)>=17 and sum(self.d)<=21:
                                print("You lost.")
                                game = 0
                                self.chips -= self.bet*2
                                break
                            if sum(self.d)==sum(self.p) and sum(self.d)>=17:
                                print("Push.")
                                game = 0
                                break
                            if sum(self.d)>21:
                                print("You won.")
                                game =0
                                self.chips += self.bet*2
                                break

                    if a == "4" and self.p[0]==self.p[1]:
                        self.s1=[0]
                        self.s2=[0]
                        self.s1[0] = self.p[0]
                        self.s2[0] = self.p[1]
                        split1=1
                        split2=1
                        self.s1.append(x.cards.pop(0))
                        self.s2.append(x.cards.pop(0))
                        print("1st hand card: ")
                        self.display_card(self.s1[-1])
                        print("2nd hand card: ")
                        self.display_card(self.s2[-1])
                        print("Dealer total: ", sum(self.d))
                        print("Player 1st hand total: ", sum(self.s1))
                        print("Player 2st hand total: ", sum(self.s2))

                        while split2 ==1:
                            while split1 ==1:
                                b = input("What would you like to do for 1st hand? 1) Hit 2) Stand 3) Double Down")
                                if b == "1":
                                    self.s1.append(x.cards.pop(0))
                                    self.ace_adjustment(self.s1)
                                    self.display_card(self.s1[-1])
                                    print("Dealer total: ", sum(self.d))
                                    print("Player 1st hand total: ", sum(self.s1))
                                    print("Player 2st hand total: ", sum(self.s2))
                                    if sum(self.s1)>21:
                                        split1=0

                                if b == "2":
                                    split1=0

                                if a == "3":
                                    self.s1.append(x.cards.pop(0))
                                    self.ace_adjustment(self.s1)
                                    self.display_card(self.s1[-1])
                                    print("Dealer total: ", sum(self.d))
                                    print("Player 1st hand total: ", sum(self.s1))
                                    print("Player 2st hand total: ", sum(self.s2))
                                    split1 = 0

                            c = input("What would you like to do for 2nd hand? 1) Hit 2) Stand 3) Double Down")
                            if c =="1":
                                self.s2.append(x.cards.pop(0))
                                self.ace_adjustment(self.s2)
                                self.display_card(self.s2[-1])
                                print("Dealer total: ", sum(self.d))
                                print("Player 1st hand total: ", sum(self.s1))
                                print("Player 2st hand total: ", sum(self.s2))
                                if sum(self.s2)>21:
                                    split2=0

                            if c == "2":
                                split2=0

                            if c == "3":
                                self.s2.append(x.cards.pop(0))
                                self.ace_adjustment(self.s2)
                                self.display_card(self.s2[-1])
                                print("Dealer total: ", sum(self.d))
                                print("Player 1st hand total: ", sum(self.s1))
                                print("Player 2st hand total: ", sum(self.s2))
                                split2 = 0

                        split3=1
                        while split3==1:
                            self.d.append(x.cards.pop(0))
                            self.ace_adjustment(self.d)
                            self.display_card(self.d[-1])
                            print("Dealer total: ", sum(self.d))
                            print("Player 1st hand total: ", sum(self.s1))
                            print("Player 2st hand total: ", sum(self.s2))

                            if sum(self.d)<=21 and sum(self.d)>=17:

                                if sum(self.s1)>=21:
                                    print("1st hand bust.")
                                    self.chips -= self.bet

                                if sum(self.s2)>=21:
                                    print("2nd hand bust.")
                                    self.chips -= self.bet

                                if sum(self.s1)> sum(self.d) and sum(self.s1)<=21:
                                    print("1st hand won.")
                                    self.chips += self.bet

                                if sum(self.s2)> sum(self.d) and sum(self.s2)<=21:
                                    print("2nd hand won.")
                                    self.chips += self.bet

                                if sum(self.d)>sum(self.s1):
                                    print("You lost 1st hand.")
                                    self.chips -= self.bet

                                if sum(self.d)==sum(self.s1):
                                    print("Push 1st hand.")

                                if sum(self.d)>sum(self.s2):
                                    print("You lost 2nd hand.")
                                    self.chips -= self.bet

                                if sum(self.d)==sum(self.s2):
                                    print("Push 2nd hand.")

                                split3=0
                                game=0

                            if sum(self.d)>21:
                                print("Dealer bust.")
                                split3=0
                                game=0
                                self.chips += self.bet*2
                except ValueError:
                    print("Invalid entry. Please enter a valid number.")


    def initial_player_display_card(self, x, y):
        """This is the initial player hand card display since player starts with 2 cards"""
        import random
        # suit = ["♠","♥","♦","♣"]     These are non-ascii characters and if displayed on command prompt then may run into encoding errors.
        suit = ["S", "H", "D", "C"]   #entering suits into ascii format
        face = [10, "J", "Q", "K"]
        ace_display = "A"
        a = x
        b = y
        if x == 10:
            a = random.choice(face)
        if x == 11:
            a = "A"
        if y == 10:
            b = random.choice(face)
        if y == 11:
            b = "A"
        print("---------", "---------")
        print("| {:<2}    |".format(a),"| {:<2}    |".format(b))
        print("|       |","|       |")
        print("|   {}   |".format(random.choice(suit)),"|   {}   |".format(random.choice(suit)))
        print("|       |","|       |")
        print("|    {:>2} |".format(a),"|    {:>2} |".format(b))
        print("---------","---------")

    def display_card(self, x):
        """This is the single hand card display for each individual card dealt."""
        import random
        # suit = ["♠","♥","♦","♣"]     These are non-ascii characters and if displayed on command prompt then may run into encoding errors.
        suit = ["S", "H", "D", "C"]   #entering suits into ascii format
        face = [10, "J", "Q", "K"]
        ace_display = "A"
        a = x
        if x == 10:
            a = random.choice(face)
        if x == 11:
            a = "A"
        print("---------")
        print("| {:<2}    |".format(a))
        print("|       |")
        print("|   {}   |".format(random.choice(suit)))
        print("|       |")
        print("|    {:>2} |".format(a))
        print("---------")


#=====================================================================================
# This is the main user-prompt

print("Welcome to Blackjack!")

while True:

    x1 = input("What would you like to do?\n1)Play 2)Exit")
    if x1 =="1":
        deck = Deck()
        deck.create_deck()
        deck.shuffle_deck()
        deal = Deal()
        deal.deal_card(deck)
    if x1 =="2":
        break
