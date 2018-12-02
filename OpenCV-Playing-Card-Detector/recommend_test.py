import os
import Cards
import player_recommend

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

def dealerProb(face, dest, deck, dealer_has_ace):
    total = 0
    isSoft = 1
    if(dest == face):
        return 1
    if(face >= 17):
        return 0

    for i in range(2, 11 + 1, 1):
        tmp = deck.count(i)/len(deck)
        
        if(dealer_has_ace):
            while(face + i > 21 and dealer_has_ace):
                dealer_has_ace -= 1
                face -= 10
        
        delta = dest - face - i
        
        if(i == 11):
            dealer_has_ace += 1
            if(face > 10 and face <= 20):
                dealer_has_ace -= 1
                isSoft = 0
                delta += 10
        
        if(tmp > 0 and delta >= 0):
            deck.remove(i)
            if(i == 11 and isSoft == 0):
                total += tmp * dealerProb(face + 1, dest, deck, dealer_has_ace)
            else:
                total += tmp * dealerProb(face + i, dest, deck, dealer_has_ace)
            deck.append(i)
        elif(i == 11):
            dealer_has_ace -= 1

    return total

def calc_dealer_bust(face, card_deck, dealer_has_ace):
    if(face == 0):
        return 0
    p = 0
    print(dealer_has_ace)
    for i in range(17, 22, 1):
        tmp = dealerProb(face, i, card_deck, dealer_has_ace)
        p += tmp
        print(str(i) + ": " + str(tmp))

    return 1 - p

def basic_strategy(player_sum, dealer_value, isSoft):
    if 4 <= player_sum <= 8:
        return "HIT"
    if player_sum == 9:
        if dealer_value in [1,2,7,8,9,10]:
            return "HIT"
        return "DOUBLE"
    if player_sum == 10:
        if dealer_value in [1, 10]:
            return "HIT"
        return "DOUBLE"
    if player_sum == 11:
        if dealer_value == 1:
            return "HIT"
        return "DOUBLE"
    
    if isSoft:
        #we only double soft 12 because there's no splitting
        if player_sum in [12, 13, 14]:
            if dealer_value in [5, 6]:
                return "DOUBLE"
            return "HIT"
        if player_sum in [15, 16]:
            if dealer_value in [4, 5, 6]:
                return "DOUBLE"
            return "HIT"
        if player_sum == 17:
            if dealer_value in [3, 4, 5, 6]:
                return "DOUBLE"
            return "HIT"
        if player_sum == 18:
            if dealer_value in [3, 4, 5, 6]:
                return "DOUBLE"
            if dealer_value in [2, 7, 8]:
                return "STAND"
            return "HIT"
        if player_sum >= 19:
            return "STAND"

    else:
        if player_sum == 12:
            if dealer_value in [1, 2, 3, 7, 8, 9, 10]:
                return "HIT"
            return "STAND"
        if player_sum in [13, 14, 15, 16]:
            if dealer_value in [2, 3, 4, 5, 6]:
                return "STAND"
            return "HIT"

        if player_sum >= 17:
            return "STAND"
    return "STAND"

def recommend(player_cards, dealer_cards):
    player_cards_content, dealer_cards_content, player_has_ace, dealer_has_ace = draw_cards_content(player_cards, dealer_cards)
    
    card_deck = [11,11,11,11,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
    
    for i in range(len(player_cards_content)):
        if(player_cards_content[i] in card_deck):
            card_deck.remove(player_cards_content[i])

    for i in range(len(dealer_cards_content)):
        if(dealer_cards_content[i] in card_deck):
            card_deck.remove(dealer_cards_content[i])

    player_sum = sum(player_cards_content)
    dealer_sum = sum(dealer_cards_content)

    while player_has_ace and player_sum > 21:
        for i in range(len(player_cards_content)):
            if(player_cards_content[i] == 11):
                player_has_ace -= 1
                player_sum -= 10
                break

    while dealer_has_ace and dealer_sum > 21:
        for i in range(len(dealer_cards_content)):
            if(dealer_cards_content[i] == 11):
                dealer_has_ace -= 1
                dealer_sum -= 10
                break

    odd_dealer_bust = calc_dealer_bust(dealer_sum, card_deck, dealer_has_ace)
    odd_dealer_bust = round(odd_dealer_bust, 2)

    action = basic_strategy(player_sum, dealer_sum, player_has_ace)
    
    return player_sum, dealer_sum, action, odd_dealer_bust

