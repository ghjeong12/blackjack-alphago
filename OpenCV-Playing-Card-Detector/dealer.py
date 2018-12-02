# this is for dealer action
from recommend_test import *

def get_score(player_cards_content):
    score = 0
    num_ace = 0
    
    for i in range(len(player_cards_content)):
        if(player_cards_content[i] != 11):
            score += player_cards_content[i]

        if(player_cards_content[i] == 11):
            num_ace += 1

    score += num_ace
    print(num_ace)
    print(score)
    for i in range(num_ace):
        if(score+10 > 21):
            break
        else:
            score = score+10

    return score

def get_dealer_action(player_cards, dealer_cards):
    dealer_action =  'hit'
    player_cards_content, dealer_cards_content, player_has_ace, delaer_has_ace = draw_cards_content(player_cards, dealer_cards)
    
    dealer_sum = get_score(dealer_cards_content)

    if dealer_sum >= 17:
        dealer_action = 'break'
    return dealer_action, dealer_sum
