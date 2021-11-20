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

    black = (0,0,0) # normal platform
    navy = (20,33,61) # maybe spring or moving platform
    orange = (252, 163, 17) # ball
    grey = (229, 229, 229) # background 
    white = (255,255,255) # background

class Platform:
    def __init__(self, y):
        self.x = random.randint(40,460)
        self.y = y
        self.rect = None

    def setY(self, y):
        self.y = y

    def getPos(self):
        return self.pos

    def drawPlatform(self, cameraShift):
        self.rect = (self.x - 37, (self.y-5)+cameraShift, 75, 10)
        pygame.draw.rect(win, color.black, self.rect)

class Player:
    def __init__(self):
        self.x = 250
        self.y = 350
        self.pos = (self.x, self.y)
        self.dx = 0
        self.dy = 0
        self.gravity = 0.3
        self.rect = pygame.Rect(self.x,self.y,40,40)

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x

    def moveX(self, x):
        self.x += x

    def get_pos(self):
        return self.pos

    def drawPlayer(self,cameraShift):
        #self.rect = pygame.Rect(self.x-22, self.y+cameraShift-22, 45,45)
        self.rect = pygame.Rect(self.x, self.y+cameraShift, 45,45)
        pygame.draw.rect(win, color.navy, self.rect)

    def getRect(self):
        return self.rect

    def jump(self):
        self.dy = -10

def newPlatforms(cameraShift):
    # gap between them
    gap_lower, gap_upper= 48, 68

    # deleting platforms outside of screen 
    i = 0
    while(i < len(platforms)):
        if platforms[i].y+cameraShift > win.get_height():
            del platforms[i]
        i+=1
    i = 0        

    # Gen only the platforms we can see [-1] returns the last in a list
    while platforms[-1].y+cameraShift >= 0:
        gap = random.randint(gap_lower, gap_upper)
        plat = Platform(platforms[-1].y - gap)
        platforms.append(plat)

def reset():
    global platforms
    platforms.clear()
    win.fill((255,255,255))

def main():
    global platforms
    run = True
    player = Player()
    clock = pygame.time.Clock()
    cameraShift = 0
    player.dx = 0
    platforms.append(Platform(500))
    player.jump()
    while run:
        win.fill(color.grey)
        newPlatforms(cameraShift)
        clock.tick(60)

        player.dy += player.gravity
        player.setY(player.y + player.dy)
        
        if player.y > 680-cameraShift:
            run = False
        
        # Getting the Camera Shift 
        if player.y < win.get_height() // 2 - 40:
            temp = -player.y + win.get_height()/2 - 20
            if temp>cameraShift:
                cameraShift = temp
            else:
                pass

        for plat in platforms:
            plat.drawPlatform(cameraShift)

        # Check if player hits platform
        for plat in platforms:
            if plat.y+cameraShift > player.y:
                if player.rect.colliderect(plat.rect) and player.dy>=0 and player.rect.bottom <= (plat.y+cameraShift+5): # +5 is the tolerance, kinda room for error
                    print("PLAYER Y : %d" % player.rect.bottom)
                    print("PLAT Y : %d" % (plat.y+cameraShift))
                    player.jump()    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.dx = -10 
                if event.key == pygame.K_d:
                    player.dx = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.dx = 0 
                if event.key == pygame.K_d:
                    player.dx = 0
        
        if not player.x+player.dx < 0 or player.x+player.dx > 500:
            player.setX(player.x + player.dx)

        player.drawPlayer(cameraShift)
        pygame.display.update()

    pygame.quit()


main()
