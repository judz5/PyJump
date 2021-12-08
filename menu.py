import pygame, sys
from pygame.locals import *

mainClock = pygame.time.Clock()
pygame.init()
win = pygame.display.set_mode([500,700])
win_rect = win.get_rect()
win_rect_center = win_rect.center

buttons = []

main_Font = pygame.font.Font('dogicapixel.ttf', 60)
button_Font = pygame.font.Font('dogicapixel.ttf', 30)

class Button():
    def __init__(self, height, width, y, text):
        self.height = height
        self.width = width
        self.y = y
        self.rect = pygame.Rect(250-(self.width/2), self.y, self.width, self.height)
        self.text = text
        self.color = (255,255,255)

    def draw_button(self):
        pygame.draw.rect(win, self.color, self.rect)

    def add_text(self):
        draw_text(self.text, button_Font, (0,0,0), win, self.rect.centery)

def draw_text(text, font, color, surface, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(win.get_width()/2, y))
    #textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def check_hover(pos):
    for button in buttons:
        if(button.rect.collidepoint(pos)):
            button.color = (150,150,150)
        else:
            button.color = (255,255,255)

def main_menu():
    play = Button(75, 225, 250, 'Play')
    shop = Button(75, 225, 375, 'Shop')
    stop = Button(75, 225, 500, 'Quit')

    buttons.append(play)
    buttons.append(shop)
    buttons.append(stop)
    while True:
        win.fill((0,0,0))
        draw_text('Py-Jump', main_Font, (255,255,255), win, 150)

        mouse = pygame.mouse.get_pos()

        check_hover(mouse)

        for button in buttons:
            button.draw_button()
            button.add_text()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        mainClock.tick(60)


main_menu()
