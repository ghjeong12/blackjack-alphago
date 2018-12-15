import os
import player
import recommend_test

def check_bust(user):
    if user.get_score() > 21:
        return 1
    else:
        return 0

def game():
    print("[SYSTEM] Game starts")
    dealer = player.Dealer()
    user = player.Player()

    user_win = -1

    print("Dealer cards")
    dealer.draw_card()
    dealer.draw_card()
    dealer.show_first()
    print("unknown")
    
    print("Player cards")
    user.draw_card()
    user.draw_card()
    user.print_cards()
    print("Score : " + str(user.get_score()))
    player_sum, dealer_sum, action, p_hit, p_stand = recommend(user.cards, dealer.cards)
    choice = "begin"
    while choice != "q":
        choice = input("Enter [H]it, [S]tand, or [Q]uit\n").lower()
        if choice == "h":
            user.hit()
            if check_bust(user)==0:
                print("Score : " + str(user.get_score()))
        elif choice == "s":
            while dealer.get_score() < 17:
                dealer.draw_card()
            print("Dealer score: " + str(dealer.get_score())) 
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
            print("[SYSTEM] Lose: User busted")
            user_win = 0
            break
    print("USER")
    user.print_cards()
    print("Total: " + str(user.get_score()))

    print("DEALER")
    dealer.print_cards()
    print("Total: " + str(dealer.get_score()))
    if user_win == 0:
        print("[SYSTEM] Lose")
    if user_win == 1:
        print("[SYSTEM] Win")
    if user_win == 2:
        print("[SYSTEM] Draw")
if __name__ == "__main__" :
    game()
    
    
