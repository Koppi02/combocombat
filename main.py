import pygame
from fighter import Fighter
from import_characters import *
from settings import *
from charsel import CharacterSelection
from game import Game

pygame.init()

game = Game()

# Játék Loop
while True:
    if game.start_menu():

        char_selection = CharacterSelection(
            game.screen, game.fighters, pygame.font.Font('./DoubleHomicide.ttf', 48))
        selected_fighter_indices = char_selection.run()

        if selected_fighter_indices is None:
            break

        score = [0, 0]
        intro_count = 4
        say_ready = True
        say_fight = True
        round_over = False
        fighters = game.set_fighters(selected_fighter_indices)

        run = True
        while run:
            game.clock.tick(FPS)
            game.draw_bg(game.bg_image)  # Háttér kirajzolása

            # Fighter frissítés és kirajzolás
            fighters[0].update()
            fighters[1].update()
            fighters[0].draw(game.screen)
            fighters[1].draw(game.screen)
            fighters[0].regen()
            fighters[1].regen()

            # Kamera pivot teszt
            # camera_pivot = ((fighter_1.rect.center[0] + fighter_2.rect.center[0])/2, (fighter_1.rect.center[1] + fighter_2.rect.center[1])/2)
            # pygame.draw.circle(screen, RED, camera_pivot, 30, 10)

            # HP bar, játékosok, stb. kirajzolása
            game.draw_health_and_stamina_bar(game.health_image, fighters[0].health, fighters[0].max_health, game.stamina_image,
                                             fighters[0].stamina, fighters[0].max_stamina, SCREEN_WIDTH / 50, SCREEN_HEIGHT / 30, False)
            game.draw_health_and_stamina_bar(game.health_image, fighters[1].health, fighters[1].max_health, game.stamina_image,
                                             fighters[1].stamina, fighters[1].max_stamina, SCREEN_WIDTH - SCREEN_WIDTH / 50, SCREEN_HEIGHT / 30, True)
            game.draw_text(f"{fighters[0].name}: " +
                           str(score[0]), SCORE_FONT, RED, SCREEN_WIDTH / 50, SCREEN_HEIGHT / 30 + 75)
            game.draw_text(f"{fighters[1].name}: " + str(score[1]), SCORE_FONT, RED, SCREEN_WIDTH - SCREEN_WIDTH / 50 - SCORE_FONT.size(
                f"{fighters[1].name}: " + str(score[1]))[0], SCREEN_HEIGHT / 30 + 75)

            # Visszaszámláló logika
            if intro_count <= 0:
                fighters[0].move(SCREEN_WIDTH, SCREEN_HEIGHT,
                                 game.screen, fighters[1], round_over)
                fighters[1].move(SCREEN_WIDTH, SCREEN_HEIGHT,
                                 game.screen, fighters[0], round_over)
            else:
                if intro_count == 2:
                    game.draw_centered_text("READY", COUNT_FONT,
                                            RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                    if say_ready:
                        pygame.mixer.Sound.play(game.ready_sound)
                        say_ready = False
                if intro_count == 1:
                    game.draw_centered_text("Fight", COUNT_FONT,
                                            RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                    if say_fight:
                        pygame.mixer.Sound.play(game.fight_sound)
                        say_fight = False
                        pygame.mixer.music.set_volume(1)
                if (pygame.time.get_ticks() - game.last_count_update) >= 1000:
                    intro_count -= 1
                    game.last_count_update = pygame.time.get_ticks()
                if intro_count == 0:
                    pygame.mixer.music.play(-1)

            # Eseménykezelés
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Nézze meg ha valaki vesztett
            if not round_over:
                winner = ''
                if fighters[0].alive == False or fighters[1].alive == False:
                    winner = fighters[1].name if fighters[0].alive == False else fighters[0].name
                    score[1 if fighters[0].alive == False else 0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                    pygame.mixer.music.fadeout(1000)

                else:

                    if score[0] >= WINNING_SCORE or score[1] >= WINNING_SCORE:
                        pygame.mixer.music.fadeout(1000)
                        result = game.winner_screen(
                            fighters[0].name if score[0] > score[1] else fighters[1].name)
                        if result == 'restart':
                            score = [0, 0]
                            fighters = game.set_fighters(
                                selected_fighter_indices)
                        elif result == 'menu':
                            score = [0, 0]
                            run = game.start_menu()
                        else:
                            run = False
                        continue
            else:
                game.draw_centered_text(
                    f'{winner} wins!', COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 4
                    say_ready = True
                    say_fight = True
                    fighters = game.set_fighters(selected_fighter_indices)

            # Frissíti a képet
            pygame.display.update()
    pygame.quit()
