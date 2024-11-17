import pygame
import random
from button import Button
from network import Network
from player import Player

#window
SCREEN_WIDTH = 1540
SCREEN_HEIGHT = 800
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Client')

#colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
DEEP_RED = (114,24,10)
LIGHT_RED = (211, 78, 43)
LIGHT_YELLOW = (247, 176, 58)

#define font
coolfont = pygame.font.Font('fonts/EncodeSansNarrow-Bold.ttf', 60)
extra_coolfont = pygame.font.Font('fonts/EncodeSansNarrow-Bold.ttf', 40)
arialfont = pygame.font.SysFont("Arial", 60)

# drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x,y))

def generate_disc():
    final_disc_stats = []

    # Number of values possibilities
    num_value_poss = [1, 1, 2, 2, 2, 3, 3, 4, 5]

    # Final disc number possibilities
    f_disc_num_poss = []

    num_values_index = random.randint(0, len(num_value_poss) - 1)
    num_values_f = num_value_poss[num_values_index]

    if num_values_f == 1:
        f_disc_num_poss = [3, 3, 3, 4, 4, 4, 5]
    else:
        f_disc_num_poss = [1, 2, 3, 4, 5, 6]

    percentage = 100

    for i in range(num_values_f, 0, -1):
        if i != (1):
            if i == 5:
                appended_percentage = 20
            else:
                temp_percentage_max = percentage - ((i - 1) * 20)
                appended_percentage = random.randint(20, temp_percentage_max)
        else:
            appended_percentage = percentage

        percentage -= appended_percentage

        append_value = random.randint(0, len(f_disc_num_poss) - 1)
        disc_value = f_disc_num_poss[append_value]
        f_disc_num_poss.remove(disc_value)

        final_disc_stats.append((disc_value, appended_percentage))

    return final_disc_stats, num_values_f

#buttons
betMoney = Button(LIGHT_RED, DEEP_RED, 25, 675, 200, 100, "Bet")
unbetMoney = Button(LIGHT_RED, DEEP_RED, 250, 675, 200, 100, "unBet")
confirmTurn = Button(LIGHT_RED, DEEP_RED, 475, 675, 300, 100, "confirm")

round_over = True
current_player_turn = 0

def redrawWindow(win, player1, player2, round_status):
    win.fill(DEEP_RED)

    betMoney.draw(win)
    unbetMoney.draw(win)
    confirmTurn.draw(win)

    # Display statuses
    draw_text(f"Round: {round_status}", extra_coolfont, LIGHT_RED, 25, 25)
    draw_text(f"p1: {player1.player_ready}", extra_coolfont, LIGHT_RED, 25, 75)
    draw_text(f"p2: {player2.player_ready}", extra_coolfont, LIGHT_RED, 25, 125)
    draw_text(f"Id: {player1.id}", extra_coolfont, LIGHT_RED, 25, 175)

    draw_text(f"Current: {current_player_turn}", extra_coolfont, LIGHT_RED, 1225, 25)


    # Draw discs
    draw_text(f"You: {str(player1.disc_data)}", extra_coolfont, LIGHT_RED, 325, 200)
    draw_text(f"Them: {str(player2.disc_data)}", extra_coolfont, LIGHT_RED, 325, 300)

    # Display balances
    draw_text(f"ur balance: ${player1.player_balance}", extra_coolfont, LIGHT_RED, 25,600)
    draw_text(f"p2 balance: ${player2.player_balance}", extra_coolfont, LIGHT_RED, 1025,650)

    pygame.display.update()

def main():
    global current_player_turn, round_over
    run = True
    n = Network()
    p1,  current_player_turn = n.getInformation()

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 , current_player_turn = n.send(p1, current_player_turn)

        if round_over:
            round_status = "Not Started"
        else:
            round_status = "Started"

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
                            p1.disc_data, p1.disc_num_values = generate_disc()

                            round_over = False
                        else:

                            if p1.player_confirmed == 0:
                                p1.player_confirmed = 1

                            else:
                                p1.player_confirmed = 0

                        current_player_turn = 1-current_player_turn
                        get_back = n.send(p1, current_player_turn)
                        p2 = get_back[0]



                if betMoney.isOver(mouse_pos):

                    if p1.player_ready == 1 and p2.player_ready == 1:
                        if p1.is_player_turn == 1:

                            if (p1.player_balance - 1) >= 0:
                                p1.overall_bet += 1
                                p1.player_balance -= 1

                if unbetMoney.isOver(mouse_pos):
                    if p1.player_ready == 1 and p2.player_ready == 1:
                        if p1.is_player_turn == 1:

                            if (p1.player_balance - 1) >= 0:
                                p1.overall_bet -= 1
                                p1.player_balance += 1

        # cool stuff
        redrawWindow(win, p1, p2, round_status)

main()