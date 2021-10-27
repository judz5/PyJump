import pygame
import turtle

pygame.init()
win = pygame.display.set_mode([500,700])

prevLine = [[(250,650), (250,650)]]

previous_point = (250,650)
cameraShift = 0

def draw_mousePos(event):
    global previous_point
    click_pos = event.pos
    if previous_point != None:
        prevLine.append([previous_point, click_pos])
        previous_point = None
    previous_point = click_pos
    
def drawAll(cameraShift):
    for i in range(len(prevLine)):
        first = prevLine[i][0]
        last = prevLine[i][1]
        pygame.draw.line(win, (0,0,0), (first[0], first[1]+cameraShift), (last[0], last[1]+cameraShift), 10)
        
def reset():
    global prevLine, previous_point
    prevLine.clear()
    prevLine.append([(250,650), (250,650)])
    previous_point = (250,650)
    win.fill((255,255,255))

class Ball:
    def __init__(self):
        self.x = 250
        self.y = 350
        self.dx = 0
        self.dy = 0
        self.gravity = 0.3

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x

    def drawBall(self,cameraShift):
        pygame.draw.circle(win, (0,0,255), (self.x, self.y+cameraShift), 20)

def main():
    run = True
    ball = Ball()
    clock = pygame.time.Clock()
    cameraShift = 0
    while run:
        clock.tick(60)

        ball.dy += ball.gravity
        ball.setY(ball.y + ball.dy)

        if ball.y > 680:
            ball.dy *= -1.1

        if ball.y < 350:
            cameraShift = -ball.y + win.get_height()/2 - 20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                draw_mousePos(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset()
        pygame.display.update()
        win.fill((255,255,255))
        drawAll(cameraShift)
        ball.drawBall(cameraShift)
    pygame.quit()



main()