import os

import player_recommend

def check_bust(user):
    if user.get_score() > 21:
        return 1
    else:
        return 0

def recommend(user, dealer):
    first_card = user.cards[0]
    second_card = user.cards[1]
    dealer_first_card = dealer.cards[0]
    if first_card == 1 and second_card == 7:
        if dealer_first_card == 2 or dealer_first_card == 7 or dealer_first_card == 8 or dealer_first_card == 1:
            return "s"
        else : return "h"
    score = user.get_score()
    if(score <= 16):
       return "h"
    elif(score <= 21):
        return "s"

def game():
    dealer = player_recommend.Dealer()
    user = player_recommend.Player()

    user_win = -1

    dealer.draw_card()
    dealer.draw_card()
    user.draw_card()
    user.draw_card()
    user.cards.sort()
    choice = "begin"
    while choice != "q":
        choice = recommend(user, dealer)
        if choice == "h":
            user.hit()
        elif choice == "s":
            while dealer.get_score() < 17:
                dealer.draw_card()
            if check_bust(dealer):
                user_win = 1
            elif dealer.get_score() > user.get_score():
                user_win = 0
            elif dealer.get_score() < user.get_score():
                user_win = 1
            else:
                user_win = 2 # Draw
            break
        elif choice == "q":
            print("Exit")
            exit()

        if check_bust(user)==1:
            user_win = 0
            break
    
    length = len(user.cards)
    for i in range(length):
        user.cards.pop()
    length = len(dealer.cards)
    for i in range(length):
        dealer.cards.pop()
    if user_win == 0:
        return -1
    if user_win == 1:
        return 1
    if user_win == 2:
        return 0
if __name__ == "__main__" :
    result = 0
    for i in range(1, 1000):
        result += game()
    print(result)
    
    
