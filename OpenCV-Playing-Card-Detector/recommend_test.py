import os
import Cards
import player_recommend
import numpy as np

def draw_cards_content(player_cards, dealer_cards):
    #calc current number
    player_cards_content = []
    dealer_cards_content = []
    dealer_has_ace = 0
    player_has_ace = 0

    for i in range(len(dealer_cards)):
        if(dealer_cards[i].best_rank_match == "Ace"):
            dealer_has_ace += 1
            dealer_cards_content.append(11)    
        elif(dealer_cards[i].best_rank_match == "Two"):
            dealer_cards_content.append(2)    
        elif(dealer_cards[i].best_rank_match == "Three"):
            dealer_cards_content.append(3)    
        elif(dealer_cards[i].best_rank_match == "Four"):
            dealer_cards_content.append(4)    
        elif(dealer_cards[i].best_rank_match == "Five"):
            dealer_cards_content.append(5)    
        elif(dealer_cards[i].best_rank_match == "Six"):
            dealer_cards_content.append(6)    
        elif(dealer_cards[i].best_rank_match == "Seven"):
            dealer_cards_content.append(7)    
        elif(dealer_cards[i].best_rank_match == "Eight"):
            dealer_cards_content.append(8)    
        elif(dealer_cards[i].best_rank_match == "Nine"):
            dealer_cards_content.append(9)    
        elif(dealer_cards[i].best_rank_match == "Ten"):
            dealer_cards_content.append(10)    
        elif(dealer_cards[i].best_rank_match == "Jack"):
            dealer_cards_content.append(10)    
        elif(dealer_cards[i].best_rank_match == "Queen"):
            dealer_cards_content.append(10)    
        elif(dealer_cards[i].best_rank_match == "King"):
            dealer_cards_content.append(10)    
    

    for i in range(len(player_cards)):
        if(player_cards[i].best_rank_match == "Ace"):
            player_has_ace += 1
            player_cards_content.append(11)
        elif(player_cards[i].best_rank_match == "Two"):
            player_cards_content.append(2)    
        elif(player_cards[i].best_rank_match == "Three"):
            player_cards_content.append(3)    
        elif(player_cards[i].best_rank_match == "Four"):
            player_cards_content.append(4)    
        elif(player_cards[i].best_rank_match == "Five"):
            player_cards_content.append(5)    
        elif(player_cards[i].best_rank_match == "Six"):
            player_cards_content.append(6)    
        elif(player_cards[i].best_rank_match == "Seven"):
            player_cards_content.append(7)    
        elif(player_cards[i].best_rank_match == "Eight"):
            player_cards_content.append(8)    
        elif(player_cards[i].best_rank_match == "Nine"):
            player_cards_content.append(9)    
        elif(player_cards[i].best_rank_match == "Ten"):
            player_cards_content.append(10)    
        elif(player_cards[i].best_rank_match == "Jack"):
            player_cards_content.append(10)    
        elif(player_cards[i].best_rank_match == "Queen"):
            player_cards_content.append(10)    
        elif(player_cards[i].best_rank_match == "King"):
            player_cards_content.append(10)
            
    return player_cards_content, dealer_cards_content, player_has_ace, dealer_has_ace

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

def prob_win(player_face, dealer_face, card_deck, player_has_ace, dealer_has_ace):
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

def recommend(player_cards, dealer_cards):
    player_cards_content, dealer_cards_content, player_has_ace, dealer_has_ace = draw_cards_content(player_cards, dealer_cards)

    card_deck = [11,11,11,11,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
    
    for i in range(len(player_cards_content)):
        if(player_cards_content[i] in card_deck):
            card_deck.remove(player_cards_content[i])

    for i in range(len(dealer_cards_content)):
        if(dealer_cards_content[i] in card_deck):
            card_deck.remove(dealer_cards_content[i])

    player_has_ace = 0
    dealer_has_ace = 0

    for i in range(len(player_cards_content)):
        if(player_cards_content[i] == 11):
            player_has_ace = 1
            break

    for i in range(len(dealer_cards_content)):
        if(dealer_cards_content[i] == 11):
            dealer_has_ace = 1
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

    if(player_sum <= 21 and dealer_sum <= 21):
        odd_p_hit, odd_p_stand = prob_win(player_sum, dealer_sum, card_deck, player_has_ace, dealer_has_ace)
       
    if(odd_p_hit > odd_p_stand):
        action = "HIT"
    else:
        action = "STAND"

    return player_sum, dealer_sum, action, round(odd_p_hit, 3), round(odd_p_stand, 3)
