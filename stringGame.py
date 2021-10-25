import pygame

pygame.init()
win = pygame.display.set_mode([500,700])

class string:
    def __init__(x,y,preX,preY):
        self.x = x
        self.y = y
        self.preX = preX
        self.preY = preY


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.fill((255,255,255))
        pygame.display.flip()
    pygame.quit()


main()