import sys
import logging
from os import path, chdir, getcwd
from Settings import *


def resource_path(relative_path):
    # This is used for Freezing the code into a .exe file
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    return path.join(path.abspath("."), relative_path)


def text_objects(text, font):
    # print Font to an object
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def button(game, msg, x, y, w, h, ic, ac, action=None):
    # Create a button that accepts font and has a function that it calls
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(game.screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "Knight":
                logging.info("Knight button pressed")
                game.player_class = "Knight"
                game.intro = False
            if action == "Ranger":
                logging.info("Ranger button pressed")
                game.player_class = "Ranger"
                game.intro = False
            elif action == "quit":
                logging.info("Quit Button Pressed")
                pg.quit()
                quit()
    else:
        pg.draw.rect(game.screen, ic, (x, y, w, h))

    smallText = pg.font.Font(resource_path(getcwd() + "/img/coolvetica rg.ttf"), 30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    game.screen.blit(textSurf, textRect)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(game.screen, ac, (x, y, w, h))
    else:
        pg.draw.rect(game.screen, ic, (x, y, w, h))

    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    game.screen.blit(textSurf, textRect)


# HUD functions
def draw_player_health(surf, x, y, pct):
    # Draw the player's health to the screen
    if pct < 0:
        pct = 0
    BAR_LENGTH = 500
    BAR_HEIGHT = 60
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_player_mana(surf, x, y, pct):
    # Draw the player's mana to the screen
    if pct < 0:
        pct = 0
    BAR_LENGTH = 500
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLUE, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_player_equip1(surf, x, y, pct):
    # Show ability 1
    # TODO implement graphical abilities
    BAR_LENGTH = 100
    BAR_HEIGHT = 100
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLACK, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_player_equip2(surf, x, y, pct):
    # Show ability 2
    # TODO implement graphical abilities
    BAR_LENGTH = 100
    BAR_HEIGHT = 100
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLACK, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
