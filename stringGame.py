import pygame
import turtle

pygame.init()
win = pygame.display.set_mode([500,700])

prevLine = [[(250,650), (250,650)]]

previous_point = (250,650)

ballPos = None
ballDX = None
ballDY = None
gravity = None

def draw_mousePos(event):
    global previous_point
    click_pos = event.pos
    if previous_point != None:
        prevLine.append([previous_point, click_pos])
        previous_point = None
    previous_point = click_pos
    
def drawAll():
    for i in range(len(prevLine)):
        first = prevLine[i][0]
        last = prevLine[i][1]
        pygame.draw.line(win, (0,0,0), first, last, 10)
        
def reset():
    global prevLine, previous_point
    prevLine.clear()
    prevLine.append([(250,650), (250,650)])
    previous_point = (250,650)
    win.fill((255,255,255))

def makeBall():
    global ballPos, ballDX, ballDY, gravity
    ballPos = (250,100)
    ballDX = 0
    ballDY = 0
    gravity = 0.1

def ballCord(x, y):
    ballPos[0] += x
    ballPos[1] += y

def setY(change):
    ballDY -= change

def drawBall():
    pygame.draw.circle(win, (0,0,255), ballPos, 20)

def main():
    run = True
    makeBall()
    while run:
        ballCord(0, -1*gravity)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                draw_mousePos(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset()
        pygame.display.update()
        win.fill((255,255,255))
        drawAll()
        drawBall()
    pygame.quit()



main()