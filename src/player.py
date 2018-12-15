import random

class User:
    def __init__(self):
        self = self
    #s should be integer from 1 ~ 13
    def draw_card(self):
        card = random.randint(1,13)
        if(card == 1):
            self.cards.append(11)
        elif(card >= 10):
            self.cards.append(10)
        else:
            self.cards.append(card)
    
    def add_card(self, s):
        self.cards.append(s)

    def print_cards(self):
        print_string = ""
        self.cards.sort()
        for i in range(len(self.cards)):
            if(self.cards[i] == 11):
                print_string += ("A ")
            elif(self.cards[i] <= 10):
                print_string += (str(self.cards[i]) + " ")
            elif (self.cards[i] == 11):
                print_string += ("J ")
            elif (self.cards[i] == 12):
                print_string += ("Q ")
            elif (self.cards[i] == 13):
                print_string += ("K ")
        print(print_string)

    def get_score(self):
        score = 0
        num_ace = 0
        for i in range(len(self.cards)):
            if(self.cards[i] > 10):
                score += 10
            elif(self.cards[i] > 1):
                score += self.cards[i]
            if(self.cards[i] == 1):
                num_ace += 1
        
        score += num_ace
        for i in range(num_ace):
            if(score+10 > 21):
                break
            else:
                score = score + 10
        return score
        
class Player(User):
    cards = []
    def __init__(self):
        self = self 
    def hit(self):
        self.draw_card()

class Dealer(User):
    cards = []
    def __init__(self):
        self = self
    def show_first(self):
        if(self.cards[0] == 1):
            print ("A ")
        elif(self.cards[0] <= 10):
            print (str(self.cards[0]))
        elif (self.cards[0] == 11):
            print ("J ")
        elif (self.cards[0] == 12):
            print ("Q ")
        elif (self.cards[0] == 13):
            print ("K ")


