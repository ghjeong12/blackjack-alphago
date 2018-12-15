import os
import player
from recommend_test import *

def check_bust(user):
    if user.get_score() > 21:
        return 1
    else:
        return 0

def game():
    dealer = player.Dealer()
    user = player.Player()

    user_win = -1

    dealer.draw_card()
    dealer.draw_card()
    #dealer.show_first()
    
    user.draw_card()
    user.draw_card()
    #user.print_cards()
    choice = "begin"
    while 1:
        player_sum, dealer_sum, action, p_hit, p_stand = recommend(user.cards, dealer.cards)
        if action == "HIT":
            user.hit()
            #if check_bust(user)==0:
            #    print("Score : " + str(user.get_score()))
        elif action == "STAND":
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

        if check_bust(user)==1:
            user_win = 0
            break
    #user.print_cards()

    #dealer.print_cards()
    
    user.cards.clear()
    dealer.cards.clear()
    if user_win == 0:
        return 0
    if user_win == 1:
        return 1
    if user_win == 2:
        return 2
if __name__ == "__main__" :
    w = 0
    l = 0
    d = 0
    for i in range(100000):
        result = game()
        if(result == 0):
            l += 1
        elif(result == 1):
            w += 1
        elif(result == 2):
            d += 1
    print(w)
    print(l)
    print(d)
    
    
