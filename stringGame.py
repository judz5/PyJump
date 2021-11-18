import pygame
import math
import random

pygame.init()
win = pygame.display.set_mode([500,700])

platforms = []

cameraShift = 0
prePoint = None

#colors
class color():

    black = (0,0,0) # normal string
    navy = (20,33,61) # maybe some kind of special string
    orange = (252, 163, 17) # ball
    grey = (229, 229, 229) # background 
    white = (255,255,255)

class Platform:
    def __init__(self, y):
        self.x = random.randint(0,500)
        self.y = y

    def setY(self, y):
        self.y = y

    def getPos(self):
        return self.pos

    def drawPlatform(self, cameraShift):
        pygame.draw.rect(win, color.black, (self.x - 37, (self.y-5)+cameraShift, 75, 10))

class Ball:
    def __init__(self):
        self.x = 250
        self.y = 350
        self.pos = (self.x, self.y)
        self.dx = 0
        self.dy = 0
        self.gravity = 0.3
        self.ball_rect = pygame.Rect(self.x,self.y,40,40)

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x

    def moveX(self, x):
        self.x += x

    def get_pos(self):
        return self.pos

    def drawBall(self,cameraShift):
        self.ball_rect = pygame.Rect(self.x-20, self.y+cameraShift-20, 40,40)
        pygame.draw.circle(win, color.orange, (self.x, self.y+cameraShift), 20)

    def getRect(self):
        return self.ball_rect

def newPlatforms():
    # gap between them
    gap_lower, gap_upper= 24, 48
    
    # Deletin platforms outside screen
    for p in platforms:
        if p.y > win.get_height():
            del p

    while platforms[-1].y >= 0:
        gap = random.randint(gap_lower, gap_upper)
        plat = Platform(platforms[-1].y - gap)


def reset():
    global platforms
    platforms.clear()
    win.fill((255,255,255))

def main():
    global platforms
    run = True
    ball = Ball()
    clock = pygame.time.Clock()
    cameraShift = 0
    ball.dx = 0
    platforms.append(Platform(500))
    while run:
        win.fill(color.grey)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    ball.dx = -10
                if event.key == pygame.K_d:
                    ball.dx = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    ball.dx = 0
                if event.key == pygame.K_d:
                    ball.dx = 0
   
        if ball.x < 0:
            ball.setX(500)
        if ball.x > 500:
            ball.setX(0)    

        ball.setX(ball.x + ball.dx)

        for plat in platforms:
            plat.drawPlatform(cameraShift)

        ball.drawBall(cameraShift)
        pygame.display.update()
        newPlatforms()
 
    pygame.quit()


main()
