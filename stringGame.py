import pygame

pygame.init()
win = pygame.display.set_mode([500,700])

previous_point = (250,650)
win.fill((255,255,255))

def draw_mousePos(event):
    global previous_point
    click_pos = event.pos
    if previous_point != None:
        pygame.draw.line(win, (0,0,0), previous_point, click_pos, 5)
        previous_point = None
    previous_point = click_pos
    

def main():
    run = True
    previous_point = None
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                draw_mousePos(event)
        pygame.display.update()
    pygame.quit()


main()