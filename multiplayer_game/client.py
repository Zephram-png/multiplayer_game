import pygame
import random
import socket
import pickle
from player import Player
from network import Network

#window
SCREEN_WIDTH = 1540
SCREEN_HEIGHT = 800
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Client')
pygame.font.init()

#colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
DEEP_RED = (114,24,10)
LIGHT_RED = (211, 78, 43)
LIGHT_YELLOW = (247, 176, 58)

#define font
coolfont = pygame.font.Font('fonts/EncodeSansNarrow-Bold.ttf', 80)
extra_coolfont = pygame.font.Font('fonts/EncodeSansNarrow-Bold.ttf', 40)
arialfont = pygame.font.SysFont("Arial", 60)

class Button():
    def __init__(self, color, text_color, x, y, width, height, text=''):
        self.color = color
        self.text_color = text_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = extra_coolfont.render(self.text, 1, (self.text_color))
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

# drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x,y))

def generate_disc(num):
    final_disc_stats = []

    # Number of values possibilities
    num_value_poss = [1, 2, 2, 2, 2, 3, 3]

    # Final disc number possibilities
    f_disc_num_poss = []

    num_values_f = num

    if num_values_f == 1:
        f_disc_num_poss = [3, 3, 3, 4, 4, 4, 5]
    else:
        f_disc_num_poss = [1, 2, 3, 4, 5, 6]

    percentage = 10

    for i in range(num_values_f, 0, -1):
        if i != (1):
            if i == 5:
                appended_percentage = 2
            else:
                temp_percentage_max = percentage - ((i - 1) * 2)
                appended_percentage = random.randint(2, temp_percentage_max)
        else:
            appended_percentage = percentage

        percentage -= appended_percentage

        append_value = random.randint(0, len(f_disc_num_poss) - 1)
        if append_value >= 5:
            append_value = random.randint(0, len(f_disc_num_poss) - 1)
        disc_value = f_disc_num_poss[append_value]
        f_disc_num_poss.remove(disc_value)

        final_disc_stats.append((disc_value, (appended_percentage*10)))

    return final_disc_stats, num_values_f


def roll_disc(disc_dataa):
    new_disc_data = []
    percentage = 0
    for i in range(0, len(disc_dataa)):
        disc_data_end = disc_dataa[i][1]
        percentage += disc_data_end
        new_disc_data.append([disc_dataa[i][0], (percentage)])

    percent = random.randint(0, 100)
    the_winner_num = 0
    for i in range(0, len(new_disc_data)):
        if new_disc_data[i][1] >= percent:
            the_winner_num = new_disc_data[i][0]
            break

    return the_winner_num

def roll_discs():

    global round_over, pot, current_player_turn, p1, p2, game_over
    p1_result = roll_disc(p1.disc_data)
    p2_result = roll_disc(p2.disc_data)
    if p2_result > p1_result:
        print("p2 wins")
        if (p2.overall_bet * 2) < pot:
            p2.player_balance += p2.overall_bet * 2
            p1.player_balance += pot - (p2.overall_bet * 2)
        else:
            p2.player_balance += pot
        p2.player_bet = 0
        p1.player_bet = 0

    elif p1_result > p2_result:
        print("p1 wins")
        if (p1.overall_bet * 2) < pot:
            p1.player_balance += p1.overall_bet * 2
            p1.player_balance += pot - (p1.overall_bet * 2)
        else:
            p1.player_balance += pot
        p1.player_bet = 0
        p2.player_bet = 0

    else:
        print("tie")
        p1.player_balance += p1.overall_bet
        p1.player_bet = 0
        p2.player_balance += p2.overall_bet
        p2.player_bet = 0

    pot = 0
    round_over = True

    if p1.player_balance == 0 or p2.player_balance == 0:
        p1.player_balance = 40
        p2.player_balance = 40

    return p1_result, p2_result


def calculate_win(disc1, disc2):
    c0 = 0.00
    c1 = 0.00
    c2 = 0.00
    for i in range(len(disc1)):
        for j in range(len(disc2)):
            if disc1[i][0] > disc2[j][0]:
                winner = 1
            elif disc1[i][0] < disc2[j][0]:
                winner = 2
            else:
                winner = 0
            res = round((((disc1[i][1]) / 100) * ((disc2[j][1]) / 100)), 2)

            if winner == 1:
                c1 += res
            elif winner == 2:
                c2 += res
            else:
                c0 += res

    c0 = round(c0, 2)
    c1 = round(c1, 2)
    c2 = round(c2, 2)

    return c0, c1, c2



#buttons
betMoney = Button(LIGHT_RED, DEEP_RED, 25, 675, 200, 100, "Bet")
unbetMoney = Button(LIGHT_RED, DEEP_RED, 250, 675, 200, 100, "unBet")
confirmTurn = Button(LIGHT_RED, DEEP_RED, 475, 675, 300, 100, "confirm")

round_over = True
current_player_turn = 0

p1 = 0
p2 = 0

pot = 0
p1_win = 0
p2_win = 0
draw_pos = 0

def redrawWindow(win, player1, player2, round_status, p1_win, p2_win, draw_pos, game_over1):
    global num_pauses
    win.fill(DEEP_RED)




    if (player1.id == current_player_turn):
        betMoney.draw(win)
        unbetMoney.draw(win)
        confirmTurn.draw(win)

    # Display statuses
    draw_text(f"YOU ARE PLAYER {player1.id+1}", extra_coolfont, LIGHT_RED, 1125, 25)

    draw_text("Your Disc Probabilities", extra_coolfont, LIGHT_RED, 300, 200)
    draw_text(f"p{player2.id+1} Disc Probabilities", extra_coolfont, LIGHT_RED, 800, 200)
    if p1.rev > 0:
        draw_text(f"{str(player1.disc_data[0][0])}: {str(player1.disc_data[0][1])}%", extra_coolfont, LIGHT_RED, 300, 250)
    if p1.rev > 1:
        draw_text(f"{str(player1.disc_data[1][0])}: {str(player1.disc_data[1][1])}%", extra_coolfont, LIGHT_RED, 300, 300)
    if p1.rev > 2:
        draw_text(f"{str(player2.disc_data[0][0])}: {str(player2.disc_data[0][1])}%", extra_coolfont, LIGHT_RED, 800, 250)
    if p1.rev > 3:
        draw_text(f"{str(player2.disc_data[1][0])}: {str(player2.disc_data[1][1])}%", extra_coolfont, LIGHT_RED, 800, 300)

    # Display balances
    draw_text(f"ur balance: ${player1.player_balance}", extra_coolfont, LIGHT_RED, 25,600)
    draw_text(f"p{player2.id+1} balance: ${player2.player_balance}", extra_coolfont, LIGHT_RED, 1025,650)

    draw_text(f"amount bet: ${player1.player_bet}", extra_coolfont, LIGHT_RED, 425, 600)
    draw_text(f"p{player2.id+1} amount bet: ${player2.player_bet}", extra_coolfont, LIGHT_RED, 1025, 725)

    draw_text(f"pot: ${pot}", extra_coolfont, LIGHT_RED, 25, 25)
    draw_text(f"To call: ${player2.overall_bet - player1.overall_bet}", extra_coolfont, LIGHT_RED, 25, 75)
    draw_text(f"{round_status}", extra_coolfont, LIGHT_RED, 325, 25)

    pygame.display.update()

true_current_player_turn = 0
game_over = 1

num_pauses = 0

def game__over(win, p1, p2, p1_win, p2_win, draw_pos, p1_res, p2_res):
    win.fill(DEEP_RED)

    draw_text(f"GAME OVER!", coolfont, LIGHT_RED, 500, 25)

    draw_text(f"Your chances of winning: {p1_win}%", extra_coolfont, LIGHT_RED, 400, 225)
    draw_text(f"p{p2.id+1} chance of winning: {p2_win}%", extra_coolfont, LIGHT_RED, 400, 325)
    draw_text(f"Your result: {p1_res}", extra_coolfont, LIGHT_RED, 600, 425)
    draw_text(f"p{p2.id+1} result: {p2_res}", extra_coolfont, LIGHT_RED, 600, 525)
    if p1_res > p2_res:
        draw_text(f"winner: u", extra_coolfont, LIGHT_RED, 400, 625)
    elif p2_res > p1_res:
        draw_text(f"winner: no u", extra_coolfont, LIGHT_RED, 400, 625)
    else:
        draw_text(f"winner: tie", extra_coolfont, LIGHT_RED, 400, 625)
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    global current_player_turn, round_over, true_current_player_turn, pot, p1, p2, game_over, p1_win, p2_win, draw_pos, num_pauses
    run = True
    n = Network()
    p1,  current_player_turn = n.getInformation()

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 , current_player_turn = n.send(p1, true_current_player_turn)
        if p2.rev > p1.rev and round_over == False:
            p1.rev = p2.rev

        if p2.player_confirmed:
            pot += p2.player_bet
        if p1.player_confirmed:
            p1.player_confirmed = 0

            p1.player_bet = 0

        if (p1.player_ready == 1) and (p2.player_ready == 1):
            if current_player_turn == p1.id:

                round_status = f"               Its your turn!"
            else:
                round_status = f"        Waiting for player {p2.id+1}..."
            draw_pos, p1_win, p2_win = calculate_win(p1.disc_data, p2.disc_data)

            if (p1.player_balance == 0 or p2.player_balance == 0) and game_over == 1:
                p1.player_balance = 40
                p2.player_balance = 40
                game_over = 0
                print("reset1")

        #     do a game over thing?
        else:
            if current_player_turn == p1.id:
                round_status = "       Press confirm to start the game!"
            else:
                round_status = f"Waiting for player {p2.id+1} to start the game!"


        if p1.done == 1 or p2.done == 1:
            new_player_1_res, new_player_2_res = roll_discs()
            round_over = True
            # game over
            game__over(win, p1, p2, p1_win, p2_win, draw_pos, new_player_1_res, new_player_2_res)
            p1.done = 0
            p2.done = 0
            p1.player_ready = 0
            p2.player_ready = 0
            p1.overall_bet = 0
            p2.overall_bet = 0
            p1.player_bet = 0
            p2.player_bet = 0
            p1.rev = 3
            p2.rev = 3



        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if confirmTurn.isOver(mouse_pos):

                    if current_player_turn == p1.id:

                        if p1.player_ready == 0:
                            p1.player_ready = 1
                            wat_num_discs = random.randint(2,2)
                            if wat_num_discs == 2:
                                num_pauses = 4
                            else:
                                num_pauses = 6
                            p1.disc_data, p1.disc_num_values = generate_disc(wat_num_discs)
                            round_over = False

                            # Tells user player hit confirm button
                            if p1.player_confirmed == 0:
                                p1.player_confirmed = 1

                            # Switches the current player turn to the other one
                            current_player_turn = 1 - current_player_turn
                            true_current_player_turn = current_player_turn
                            # Returns this through the server

                        else:
                            if ((p1.overall_bet + p1.player_bet) >= p2.overall_bet) or p1.player_balance == 0:
                                p1.overall_bet += p1.player_bet
                                pot += p1.player_bet

                                if ((p1.overall_bet == p2.overall_bet) or (p1.player_balance == 0 and p2.overall_bet > p1.overall_bet)):

                                    if p2.has_bet == 1:
                                        if (p1.overall_bet == p2.overall_bet):
                                            if p1.rev == num_pauses:
                                                p1.done = 1
                                            else:
                                                p1.rev += 1

                                            p1.has_bet = 0


                                        if p1.player_balance == 0:
                                            p1.rev = num_pauses
                                            p1.done = 1
                                            p1.has_bet = 0

                                    else:
                                        p1.has_bet = 1


                                # Tells user player hit confirm button
                                if p1.player_confirmed == 0:
                                    p1.player_confirmed = 1



                                # Switches the current player turn to the other one
                                current_player_turn = 1 - current_player_turn
                                true_current_player_turn = current_player_turn
                                # Returns this through the server


                            else:
                                draw_text(f"Invalid bet", extra_coolfont, RED, 25,
                                          500)
                                pygame.display.update()
                                pygame.time.delay(1000)




                if betMoney.isOver(mouse_pos):

                    if p1.player_ready == 1 and p2.player_ready == 1:
                        if current_player_turn == p1.id:

                            if (p1.player_balance - 1) >= 0:
                                p1.player_bet += 1
                                p1.player_balance -= 1

                            print("bet")


                if unbetMoney.isOver(mouse_pos):
                    if p1.player_ready == 1 and p2.player_ready == 1:
                        if current_player_turn == p1.id:

                            if (p1.player_bet - 1) >= 0:
                                p1.player_bet -= 1
                                p1.player_balance += 1
                        print("bet")

        # cool stuff
        redrawWindow(win, p1, p2, round_status, p1_win, p2_win, draw_pos, 0)

main()