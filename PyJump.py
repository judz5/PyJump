import pygame
import math
import random

pygame.init()
win = pygame.display.set_mode([500,700])

platforms = []
particles = []

cameraShift = 0
prePoint = None

#colors
class color():

    black = (0,0,0) # normal platform
    navy = (20,33,61) # maybe spring or moving platform
    orange = (252, 163, 17) # ball
    pink = (255, 0, 160) # background 
    white = (255,255,255) # background
    blue = (0,186,255)


class Particle():
    def __init__(self, pos, vel, timer):
        self.pos = pos
        self.vel = vel
        self.timer = timer
        
class Platform:
    def __init__(self, y):
        self.x = random.randint(40,460)
        self.y = y
        self.rect = None
        if(random.randint(0, 10) == 5):
            self.type = 1
        else:
            self.type = 0
        

    def setY(self, y):
        self.y = y

    def getPos(self):
        return self.pos

    def drawPlatform(self, cameraShift):
        if(self.type == 1):
            pygame.draw.rect(win, color.orange, (self.x-18, self.y-15+cameraShift, 37, 10))
        self.rect = (self.x - 37, (self.y-5)+cameraShift, 75, 10)
        pygame.draw.rect(win, color.blue, self.rect)

class Player:
    def __init__(self):
        self.x = 250
        self.y = 350
        self.pos = (self.x, self.y)
        self.dx = 0
        self.dy = 0
        self.gravity = 0.3
        self.score = 0
        self.rect = pygame.Rect(self.x,self.y,40,40)
    
    def drawPlayer(self,cameraShift):
        #self.rect = pygame.Rect(self.x-22, self.y+cameraShift-22, 45,45)
        self.rect = pygame.Rect(self.x, self.y+cameraShift, 45,45)
        pygame.draw.rect(win, color.pink  , self.rect)

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x
 
    def jump(self):
        self.dy = -10

    def highJump(self):
        self.dy = -20

def newPlatforms(cameraShift, score):
    # gap between them
    if score <= 10:
        gap_lower, gap_upper= 48, 68
    elif score <= 25:
        gap_lower, gap_upper = 68, 88
    elif score <= 50:
        gap_lower, gap_upper = 88, 108
    else:
        gap_lower, gap_upper = 108, 125 
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
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    while run:
        win.fill(color.black)
        score = int(cameraShift/200)
        newPlatforms(cameraShift, score)
        clock.tick(60)

        player.dy += player.gravity
        player.setY(player.y + player.dy)
        
        # Check if hits bottom relative to camera shift
        if player.y > 680-cameraShift:
            run = False
        
        # Getting the Camera Shift 
        if player.y < win.get_height() // 2 - 40:
            temp = -player.y + win.get_height()/2 - 20
            if temp>cameraShift:
                cameraShift = temp
            else:
                pass

        # Drawing platforms from list
        for plat in platforms:
            plat.drawPlatform(cameraShift)

        # Check if player hits platform
        for plat in platforms:
            if plat.y+cameraShift > player.y:
                if player.rect.colliderect(plat.rect) and player.dy>=0 and player.rect.bottom <= (plat.y+cameraShift+5): # +5 is the tolerance, kinda room for error
                    if(plat.type == 0):
                        player.jump()
                        for i in range(5):
                            particles.append(Particle([player.rect.centerx, plat.y-5], [random.randint(0, 20) / 10 - 1, -1.5], random.randint(2, 6)))
                    elif(plat.type == 1):
                        player.highJump()
                        for i in range(25):
                            particles.append(Particle([player.rect.centerx, plat.y-5], [random.randint(0, 20) / 10 - 1, -1.5], random.randint(2, 6)))    
                          
        # Possible way of doing the score
        output = "Score = %d" % score
        textSurface = myfont.render(output, False, color.white)
        win.blit(textSurface,(0,0))

        # Drawing Particles 
        for particle in particles:
            particle.pos[0] += particle.vel[0]
            particle.pos[1] += particle.vel[1]
            particle.timer -= 0.05
            particle.vel[1] += 0.1

            pygame.draw.circle(win, color.white, [int(particle.pos[0]), int(particle.pos[1])+cameraShift], int(particle.timer))
            # Removing old particles 
            if particle.timer <= 0:
                particles.remove(particle)

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

        # Stay in bounds  
        if not player.x+player.dx < 0 or player.x+player.dx > 500:
            player.setX(player.x + player.dx)

        player.drawPlayer(cameraShift)
        pygame.display.update()

    pygame.quit()


main()
