# Write your code here
import random
from collections import Counter


domino_snake = []


def who_start(computer, player):
    highest_computer = -1
    highest_player = -1
    i_c = 0
    i_p = 0
    for i, d in enumerate(computer):
        if d[0] == d[1] and d[0] > highest_computer:
            highest_computer = d[0]
            i_c = i
    for i, d in enumerate(player):
        if d[0] == d[1] and d[0] > highest_player:
            highest_player = d[0]
            i_p = i

    if highest_computer > highest_player :
        return ["computer", i_c]
    elif highest_computer < highest_player:
        return ["player", i_p]
    else:
        return None


def check_if_draw(d):
    k = 0
    if d[0][0] == d[len(d)-1][1]:
        for v in d:
            if d[0][0] in v:
                k += 1
        if k == 8:
            return True
    return False


def snake_printer(s):
    if len(s) > 6:
        print(*s[:3], "...", *s[-3:], sep="", end="\n")
    else:
        print(*s, sep="", end="\n")


def domino_counter(list_a, list_b):
    return Counter([el[0] for el in list_a + list_b] + [el[1] for el in list_a + list_b])


while True:
    dominoes_full_set = [[2, 5], [1, 2], [3, 6], [0, 0], [0, 2], [5, 6], [3, 5], [2, 4], [3, 4], [1, 5], [0, 4], [2, 6],
                     [3, 3], [1, 1], [1, 4], [1, 3], [2, 3], [4, 5], [2, 2], [0, 3], [0, 6], [5, 5], [4, 4], [4, 6],
                     [0, 1], [0, 5], [1, 6], [6, 6]]
    computer_dominoes = []
    player_dominoes = []

    for i in range(7):
        computer_dominoes.append(dominoes_full_set.pop(random.randint(0, len(dominoes_full_set) - 1)))
        player_dominoes.append(dominoes_full_set.pop(random.randint(0, len(dominoes_full_set) - 1)))

    who_turn = who_start(computer_dominoes, player_dominoes)
    if who_turn[0] == "computer" or who_turn[0] == "player":
        break

if who_turn[0] == "computer":
    domino_snake.append(computer_dominoes.pop(who_turn[1]))
elif who_turn[0] == "player":
    domino_snake.append(player_dominoes.pop(who_turn[1]))

while True:
    print(70 * "=")
    print("Stock size: {}".format(len(dominoes_full_set)))
    print("Computer pieces: {}\n".format(len(computer_dominoes)))
    snake_printer(domino_snake)
    print("Your pieces:")
    for i, p in enumerate(player_dominoes):
        print("{}: {}".format(i + 1, p))

    # check game result
    if len(player_dominoes) == 0:
        print("\nStatus: The game is over. You won!")
        break
    elif len(computer_dominoes) == 0:
        print("\nStatus: The game is over. The computer won!")
        break
    elif check_if_draw(domino_snake):
        print("\nStatus: The game is over. It's a draw!")
        break

    if who_turn[0] == "computer":
        who_turn[0] = "player"
        print("\nStatus: It's your turn to make a move. Enter your command.")
        while True:
            player_choice = 0
            try:
                player_choice = int(input())
            except ValueError:
                print("\nInvalid input. Please try again.")
                continue
            if not(player_choice > len(player_dominoes) or player_choice < -len(player_dominoes)):
                if player_choice > 0 and domino_snake[-1][1] in player_dominoes[player_choice - 1]:
                    break
                elif player_choice < 0 and domino_snake[0][0] in player_dominoes[-player_choice - 1]:
                    break
                elif player_choice == 0:
                    break
                else:
                    print("Illegal move. Please try again")
            else:
                print("\nInvalid input. Please try again.")

        if player_choice > 0:
            if domino_snake[-1][1] == player_dominoes[player_choice - 1][0]:
                domino_snake.append(player_dominoes.pop(player_choice - 1))
            else:
                domino_snake.append(list(reversed(player_dominoes.pop(player_choice - 1))))
        elif player_choice < 0:
            if domino_snake[0][0] == player_dominoes[-player_choice - 1][1]:
                domino_snake.insert(0, player_dominoes.pop(-player_choice - 1))
            else:
                domino_snake.insert(0, list(reversed(player_dominoes.pop(-player_choice - 1))))
        elif player_choice == 0 and len(dominoes_full_set) > 0:
            player_dominoes.append(dominoes_full_set.pop(random.randint(0, len(dominoes_full_set) - 1)))

    elif who_turn[0] == "player":
        who_turn[0] = "computer"
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        pass_game = input()
        len_c = len(computer_dominoes) - 1
        if len_c > 0:
            possible_moves_right = [el + 1 for el in list(range(0, len_c + 1)) if domino_snake[-1][1] in computer_dominoes[el]]
            possible_moves_left = [-el - 1 for el in list(range(0, len_c + 1)) if domino_snake[0][0] in computer_dominoes[el]]
            all_possible_moves = possible_moves_right + possible_moves_left
            if len(all_possible_moves) > 0:
                nums_counted = domino_counter(domino_snake, computer_dominoes)
                dominos_score = {}
                for el in all_possible_moves:
                    if el > 0:
                        dominos_score[el] = nums_counted[computer_dominoes[el - 1][0]] + nums_counted[computer_dominoes[el - 1][1]]
                    else:
                        dominos_score[el] = nums_counted[computer_dominoes[-el - 1][1]] + nums_counted[computer_dominoes[-el - 1][0]]
                best_choice = max(dominos_score, key=dominos_score.get)

                if best_choice > 0 and domino_snake[-1][1] in computer_dominoes[best_choice - 1]:
                    if domino_snake[-1][1] == computer_dominoes[best_choice - 1][0]:
                        domino_snake.append(computer_dominoes.pop(best_choice - 1))
                    else:
                        domino_snake.append(list(reversed(computer_dominoes.pop(best_choice - 1))))
                elif best_choice < 0 and domino_snake[0][0] in computer_dominoes[-best_choice - 1]:
                    if domino_snake[0][0] == computer_dominoes[-best_choice - 1][1]:
                        domino_snake.insert(0, computer_dominoes.pop(-best_choice - 1))
                    else:
                        domino_snake.insert(0, list(reversed(computer_dominoes.pop(-best_choice - 1))))
            elif len(all_possible_moves) == 0 and len(dominoes_full_set) > 0:
                computer_dominoes.append(dominoes_full_set.pop(random.randint(0, len(dominoes_full_set) - 1)))
        else:
            domino_snake.append(computer_dominoes.pop(0))
