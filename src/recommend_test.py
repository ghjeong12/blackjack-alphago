import os
import Cards
import numpy as np


def playerProbBust(face, player_has_ace):
    total = 0
    isSoft = 1

    for i in range(2, 11 + 1, 1):
        if(i == 10):
            tmp = 16/52
        else:
            tmp = 4/52

        if(player_has_ace):
            while(face + i > 21 and player_has_ace):
                player_has_ace -= 1
                face -= 10
        
        delta = 21 - face - i

        if(i == 11 and tmp > 0):
            player_has_ace += 1
            if(face > 10 and face <= 20):
                player_has_ace -= 1
                delta += 10
                isSoft = 0
        
        if(tmp > 0 and delta < 0):
            total += tmp

    return total

def playerProb(face, dest, player_has_ace, table):
    total = 0
    isSoft = 1

    if(table[face][dest][player_has_ace] != 0):
        return table[face][dest][player_has_ace]

    if(dest == face):
        return 1

    for i in range(2, 11 + 1, 1):
        if(i == 10):
            tmp = 16/52
        else:
            tmp = 4/52

        if(player_has_ace):
            while(face + i > 21 and player_has_ace):
                player_has_ace -= 1
                face -= 10
        
        delta = dest - face - i
        
        if(i == 11 and tmp > 0):
            player_has_ace += 1
            if(face > 10 and face <= 20):
                player_has_ace -= 1
                isSoft = 0
                delta += 10
        
        if(tmp > 0 and delta >= 0):
            if(i == 11 and isSoft == 0):
                total += tmp * playerProb(face + 1, dest, player_has_ace, table)
            else:
                total += tmp * playerProb(face + i, dest, player_has_ace, table)
        elif(i == 11):
            player_has_ace -= 1

    table[face][dest][player_has_ace] = total
    return total

def dealerProb(face, dest, dealer_has_ace, table):
    total = 0
    isSoft = 1

    if(table[face][dest][dealer_has_ace] != 0):
        return table[face][dest][dealer_has_ace]

    if(dest == face):
        return 1

    if(face >= 17):
        return 0

    for i in range(2, 11 + 1, 1):
        if(i == 10):
            tmp = 16/52
        else:
            tmp = 4/52
        
        if(dealer_has_ace):
            while(face + i > 21 and dealer_has_ace):
                dealer_has_ace -= 1
                face -= 10
        
        delta = dest - face - i
        
        if(i == 11 and tmp > 0):
            dealer_has_ace += 1
            if(face > 10 and face <= 20):
                dealer_has_ace -= 1
                isSoft = 0
                delta += 10
        
        if(tmp > 0 and delta >= 0):
            if(i == 11 and isSoft == 0):
                total += tmp * dealerProb(face + 1, dest, dealer_has_ace, table)
            else:
                total += tmp * dealerProb(face + i, dest, dealer_has_ace, table)
        elif(i == 11):
            dealer_has_ace -= 1

    table[face][dest][dealer_has_ace] = total

    return total

def prob_win(player_face, dealer_face, player_has_ace, dealer_has_ace):
    dealer_table = np.zeros((21 + 1, 21 + 1, 21 + 1))
    player_table = np.zeros((21 + 1, 21 + 1, 21 + 1))

    prob_dealer = [0,0,0,0,0]
    prob_player = [0,0,0,0]

    for i in range(17, 22, 1):
        prob_dealer[i - 17] = dealerProb(dealer_face, i, dealer_has_ace, dealer_table)

    for i in range(18, 22, 1):
        if(player_face < i):
            prob_player[i - 18] = playerProb(player_face, i, player_has_ace, player_table)
        else:
            prob_player[i - 18] = 0
    
    prob_player_bust = playerProbBust(player_face, player_has_ace)
    
    prob_dealer_sum = prob_dealer[0]
    prob_greater = prob_player[0] * prob_dealer_sum
    prob_dealer_sum += prob_dealer[1]
    prob_greater += prob_player[1] * prob_dealer_sum
    prob_dealer_sum += prob_dealer[2]
    prob_greater += prob_player[2] * prob_dealer_sum
    prob_dealer_sum += prob_dealer[3]
    prob_greater += prob_player[3] * prob_dealer_sum
    prob_dealer_sum += prob_dealer[4]

    prob_dealer_bust = 1 - prob_dealer_sum
    #when player hit
    p_hit = (1 - prob_player_bust) * (prob_dealer_bust + prob_greater)
    #when player stand
    p_stand = prob_dealer_bust
    
    if(player_face <= 21):
        if(player_face > 17):
            p_stand += prob_dealer[0]
        if(player_face > 18):
            p_stand += prob_dealer[1]
        if(player_face > 19):
            p_stand += prob_dealer[2]
        if(player_face > 20):
            p_stand += prob_dealer[3]
    
    return p_hit, p_stand

def recommend(player_cards_content, dealer_cards_content):
    player_has_ace = 0
    dealer_has_ace = 0

    for i in range(len(player_cards_content)):
        if(player_cards_content[i] == 11):
            player_has_ace += 1
            break

    for i in range(len(dealer_cards_content)):
        if(dealer_cards_content[i] == 11):
            dealer_has_ace += 1
            break

    player_sum = sum(player_cards_content)
    dealer_sum = sum(dealer_cards_content)
    
    if(player_sum == 0 or dealer_sum == 0):
        return 0,0,"HIT",0,0

    while player_has_ace and player_sum > 21:
        for i in range(len(player_cards_content)):
            if(player_cards_content[i] == 11):
                player_cards_content[i] = 1
                player_sum = sum(player_cards_content)
                break

    while dealer_has_ace and dealer_sum > 21:
        for i in range(len(dealer_cards_content)):
            if(dealer_cards_content[i] == 11):
                dealer_cards_content[i] = 1
                dealer_sum = sum(dealer_cards_content)
                break
    
    odd_p_hit = 0
    odd_p_stand = 0

    #if(player_sum <= 21 and dealer_sum <= 21):
    #    odd_p_hit, odd_p_stand = prob_win(player_sum, dealer_sum, player_has_ace, dealer_has_ace)
       
    delta = odd_p_hit - odd_p_stand
    
    action = basic_strategy(player_sum, dealer_sum, player_has_ace)
    if(action == 'hit' or action == 'double'):
        action = "HIT"
    else:
        action = "STAND"

    return player_sum, dealer_sum, action, round(odd_p_hit, 3), round(odd_p_stand, 3)

def basic_strategy(player_sum, dealer_value, isSoft):
    if 4 <= player_sum <= 8:
        return 'hit'
    if player_sum == 9:
        if dealer_value in [1,2,7,8,9,10]:
            return 'hit'
        return 'double'
    if player_sum == 10:
        if dealer_value in [1, 10]:
            return 'hit'
        return 'double'
    if player_sum == 11:
        if dealer_value == 1:
            return 'hit'
        return 'double'
    if isSoft:
        #we only double soft 12 because there's no splitting
        if player_sum in [12, 13, 14]:
            if dealer_value in [5, 6]:
                return 'double'
            return 'hit'
        if player_sum in [15, 16]:
            if dealer_value in [4, 5, 6]:
                return 'double'
            return 'hit'
        if player_sum == 17:
            if dealer_value in [3, 4, 5, 6]:
                return 'double'
            return 'hit'
        if player_sum == 18:
            if dealer_value in [3, 4, 5, 6]:
                return 'double'
            if dealer_value in [2, 7, 8]:
                return 'stand'
            return 'hit'
        if player_sum >= 19:
            return 'stand'

    else:
        if player_sum == 12:
            if dealer_value in [1, 2, 3, 7, 8, 9, 10]:
                return 'hit'
            return 'stand'
        if player_sum in [13, 14, 15, 16]:
            if dealer_value in [2, 3, 4, 5, 6]:
                return 'stand'
            return 'hit'

        if player_sum >= 17:
            return 'stand'
