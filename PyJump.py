import pygame
import math
import random
import time

pygame.init()
win = pygame.display.set_mode([500,700])

platforms = []
particles = []
other_particles = []

lasers = []

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
    red = (255,0,0)
    green = (0,255,0)

    l1 = (128,0,0)
    l2 = (255,65,65)

class Particle():
    def __init__(self, pos, vel, timer, color):
        self.pos = pos
        self.vel = vel
        self.timer = timer
        self.color = color
        
class Platform:
    def __init__(self, y):
        self.x = random.randint(40,460)
        self.dx = 0
        self.y = y
        self.rect = None
        self.color = color.blue
        x = random.randint(0,20)
        if(x <= 1):
            self.type = 1
        elif(x == 10):
            self.type = 2
            self.color = color.red
        elif(x == 15):
            self.type = 3
            self.dx = 5
            self.color = color.green
        else:
            self.type = 0
        
    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x

    def getPos(self):
        return self.pos

    def drawPlatform(self, cameraShift):
        if(self.type == 1):
            pygame.draw.rect(win, color.orange, (self.x-18, self.y-15+cameraShift, 37, 10))
        
        self.rect = (self.x - 37, (self.y-5)+cameraShift, 75, 10)
        pygame.draw.rect(win, self.color, self.rect)

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

    def kill(self):
        for i in range(50):
            other_particles.append(Particle([self.rect.centerx, self.rect.centery], [random.randint(0, 20) / 10 - 1, random.uniform(-2.0,-4.0)], random.randint(2, 8),color.pink))


class Laser:
    def __init__(self, score):
        self.x = random.randint(50, 450)
        
        self.drawAll = True

        self.x0 = self.x - 100
        self.x1 = self.x + 100

        if score<=35:
            self.speed = 1
        elif score<=100:
            self.speed = 2
        elif score<=150:
            self.speed = 2

    def shift(self):
        if(self.x0 != self.x and self.x1 != self.x):
            self.x0 += self.speed
            self.x1 -= self.speed
        else:
            self.drawAll = False

    def drawLaser(self, player):
        pygame.draw.line(win, color.l1, (self.x, 0), (self.x, 700))
        if self.drawAll:
            pygame.draw.line(win, color.l1, (self.x0, 0), (self.x0, 700))
            pygame.draw.line(win, color.l1, (self.x1, 0), (self.x1, 700))
        else:
            self.checkDeath(player)
            self.effect()
            
    def checkDeath(self, player):
        print("Checking if you died")
        if(player.rect.centerx > self.x - 25 and player.rect.centerx < self.x + 25):
            print("uh you shouldve died")
            player.kill()

    def remove(self):
        lasers.clear()

    def effect(self):
        for i in range(0, 700, 10):
            other_particles.append(Particle([self.x, i], [random.randint(0, 20) / 10 - 1, random.uniform(-1.0,-2.0)], random.randint(2, 6),color.l1))
        self.remove()

def newPlatforms(cameraShift, score):
    # gap between them
    if score <= 25:
        gap_lower, gap_upper= 48, 68
    elif score <= 75:
        gap_lower, gap_upper = 68, 88
    else:
        gap_lower, gap_upper = 88, 108 
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

def newLaser(score, maxLasers):
    if(score >= 25):
        print(maxLasers)
        if(len(lasers)<maxLasers+1):
            for i in range(maxLasers):
                lasers.append(Laser(score))

def main():
    global platforms
    run = True
    player = Player()
    clock = pygame.time.Clock()
    cameraShift = 0
    player.dx = 0
    
    laser_timer = 0
    maxLasers = 1

    platforms.append(Platform(500))
    player.jump()

    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    while run:
        win.fill(color.black)
        score = int(cameraShift/200)
        clock.tick(60)
        
        laser_timer += 1
        if(laser_timer > random.randint(200,500)):
            if score>=100 and score<125:
                maxLasers = 2
            elif score>=125:
                maxLasers = 3
            newLaser(score, maxLasers)
            laser_timer = 0

        # generating new plats
        newPlatforms(cameraShift, score)
        
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
            if plat.type == 3:
                if plat.x+plat.dx >= 465:
                    plat.dx = -5
                elif plat.x+plat.dx <= 35:
                    plat.dx = 5
                plat.setX(plat.x + plat.dx)

        # Check if player hits platform
        for plat in platforms:
            if plat.y+cameraShift > player.y:
                if player.rect.colliderect(plat.rect) and player.dy>=0 and player.rect.bottom <= (plat.y+cameraShift+5): # +5 is the tolerance, kinda room for error
                    if(plat.type == 0 or plat.type == 3):
                        player.jump()
                        for i in range(5):
                            particles.append(Particle([player.rect.centerx, plat.y-5], [random.randint(0, 20) / 10 - 1, -1.5], random.randint(2, 6),color.white))
                    elif(plat.type == 1):
                        player.highJump()
                        for i in range(25):
                            particles.append(Particle([player.rect.centerx, plat.y-5], [random.randint(0, 20) / 10 - 1, -1.5], random.randint(2, 6),color.white))    
                    elif(plat.type == 2):
                        player.jump()
                        for i in range(5):
                            particles.append(Particle([player.rect.centerx, plat.y-5], [random.randint(0, 20) / 10 - 1, -1.5], random.randint(2, 6),color.white))
                        for i in range(50):
                            particles.append(Particle([plat.x, plat.y+20], [random.randint(0, 20) / 10 - 1, random.uniform(-2.0,-4.0)], random.randint(2, 8),color.red))
                        plat.y = 1000

        # score
        output = "Score = %d" % score
        textSurface = myfont.render(output, False, color.white)
        win.blit(textSurface,(0,0))

        for laser in lasers:
            laser.shift()
            laser.drawLaser(player)

        # Drawing Particles 
        for particle in particles:
            particle.pos[0] += particle.vel[0]
            particle.pos[1] += particle.vel[1]
            particle.timer -= 0.05
            particle.vel[1] += 0.1

            pygame.draw.circle(win, particle.color, [int(particle.pos[0]), int(particle.pos[1])+cameraShift], int(particle.timer))
            # Removing old particles 
            if particle.timer <= 0:
                particles.remove(particle)

        # drawing laser particles
        for particle in other_particles:
            particle.pos[0] += particle.vel[0]
            particle.pos[1] += particle.vel[1]
            particle.timer -= 0.05
            particle.vel[1] += 0.1

            pygame.draw.circle(win, particle.color, [int(particle.pos[0]), int(particle.pos[1])], int(particle.timer))
            # Removing old particles 
            if particle.timer <= 0:
                other_particles.remove(particle)

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
        if not player.x+player.dx < 0 and not player.x+player.dx > 450:
            player.setX(player.x + player.dx)

        player.drawPlayer(cameraShift)
        pygame.display.update()

    pygame.quit()


main()
