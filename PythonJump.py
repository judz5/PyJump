import pygame, math, random, time, sys, os, pickle
from pygame.locals import *

mainClock = pygame.time.Clock()

pygame.init()
pygame.font.init()
pygame.mixer.init()

win = pygame.display.set_mode([500,700], RESIZABLE | DOUBLEBUF)
win_rect = win.get_rect()
win_rect_center = win_rect.center

fake_win = win.copy()

platforms = []
particles = []
other_particles = []
buttons = []
lasers = []
square_effects = []

score = 0
cameraShift = 0

main_Font = pygame.font.Font('dogicapixel.ttf', 60)
button_Font = pygame.font.Font('dogicapixel.ttf', 30)
score_font = pygame.font.Font('dogicapixel.ttf', 25)
name_font = pygame.font.Font('dogicapixel.ttf', 15)

s = 'sound'

jumpSound = pygame.mixer.Sound(os.path.join(s, 'jump.wav'))
highJumpSound = pygame.mixer.Sound(os.path.join(s, 'highJump2.wav'))
deathSound = pygame.mixer.Sound(os.path.join(s, 'death.wav'))
laserSound = pygame.mixer.Sound(os.path.join(s, "explosion.wav"))
selectSound = pygame.mixer.Sound(os.path.join(s, "blipSelect.wav"))


jumpSound.set_volume(0.5)

musicOn = True
sfxEnabled = True

#colors
class color():

    black = (0,0,0) # normal platform
    white = (255,255,255) # background
    background_color =  (2,1,7) 
    breaking_color = (25,43,57)
    spring_color = (136, 159, 179)
    moving_color = (88,132,132)
    platform_color = (56,85,96)
    player_color = (135,96,144)
    laser_color = (66,44,91)
    polygon_color = (33,21,56)

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
        self.color = color.platform_color
        x = random.randint(0,20)
        if(x <= 1):
            self.type = 1
        elif(x == 10):
            self.type = 2
            self.color = color.breaking_color
        elif(x == 15):
            self.type = 3
            self.dx = 5
            self.color = color.moving_color
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
            pygame.draw.rect(fake_win, color.spring_color, (self.x-18, self.y-15+cameraShift, 37, 10))
        
        self.rect = (self.x - 37, (self.y-5)+cameraShift, 75, 10)
        pygame.draw.rect(fake_win, self.color, self.rect)

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
        pygame.draw.rect(fake_win, color.player_color, self.rect)

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x
 
    def jump(self):
        playSound(jumpSound)
        self.dy = -10

    def highJump(self):
        playSound(highJumpSound)
        self.dy = -20

    def kill(self):
        playSound(deathSound)
        pygame.mixer.music.fadeout(2800)
        for i in range(50):
            other_particles.append(Particle([self.rect.centerx, self.rect.centery], [random.randint(0, 20) / 10 - 1, random.uniform(-2.0,-4.0)], random.randint(2, 8),color.player_color))

class Laser:
    def __init__(self, score):
        self.x = random.randint(50, 450)
        
        self.drawAll = True

        self.x0 = self.x - 100
        self.x1 = self.x + 100

        if score<=50:
            self.speed = 1
        elif score<=150:
            self.speed = 2
        elif score>150:
            self.speed = 1
            
    def shift(self):
        if(self.x0 != self.x and self.x1 != self.x):
            self.x0 += self.speed
            self.x1 -= self.speed
        else:
            self.drawAll = False

    def drawLaser(self, player):
        #pygame.draw.line(win, color.l1, (self.x, 0), (self.x, 700))
        if self.drawAll:
            pygame.draw.line(fake_win, color.laser_color, (self.x0, 0), (self.x0, 700))
            pygame.draw.line(fake_win, color.laser_color, (self.x1, 0), (self.x1, 700))
        else:
            self.checkDeath(player)
            self.effect()
            
    def checkDeath(self, player):
        global player_dead
        if(player.rect.centerx > self.x - 25 and player.rect.centerx < self.x + 25):
            player.kill()
            player_dead = True

    def remove(self):
        lasers.remove(self)

    def effect(self):
        playSound(laserSound)
        for i in range(0, 700, 10):
            other_particles.append(Particle([self.x, i], [random.randint(0, 20) / 10 - 1, random.uniform(-1.0,-2.0)], random.randint(2, 6),color.laser_color))
        self.remove()

def newPlatforms(cameraShift, score):
    # gap between them
    if score <= 150:
        gap_lower, gap_upper= 48, 68
    else:
        gap_lower, gap_upper = 68, 88
    # deleting platforms outside of screen 
    i = 0
    while(i < len(platforms)):
        if platforms[i].y+cameraShift > fake_win.get_height():
            del platforms[i]
        i+=1
    i = 0        

    # Gen only the platforms we can see [-1] returns the last in a list
    while platforms[-1].y+cameraShift >= 0:
        gap = random.randint(gap_lower, gap_upper)
        plat = Platform(platforms[-1].y - gap)
        platforms.append(plat)

def newLaser(score, maxLasers):
    if(score >= 25):
        if(len(lasers)<maxLasers):
            for i in range(maxLasers):
                lasers.append(Laser(score))

class Button():
    def __init__(self, height, width, y, text):
        self.height = height
        self.width = width
        self.y = y
        self.rect = pygame.Rect(250-(self.width/2), self.y, self.width, self.height)
        self.text = text
        self.color = (255,255,255)

    def draw_button(self):
        pygame.draw.rect(fake_win, self.color, self.rect)

    def add_text(self):
        draw_text(self.text, button_Font, (0,0,0), fake_win, self.rect.centery)

def draw_text(text, font, color, surface, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(fake_win.get_width()/2, y))
    #textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def check_hover(sel):
    # for button in buttons:
    #     if(button.rect.collidepoint(pos)):
    #         button.color = color.breaking_color
    #     else:
    #         button.color = color.platform_color
    buttons[sel].color = color.breaking_color
    

def check_pos(pos):
    for button in buttons:
        if(button.rect.collidepoint(pos)):
            return button.text
    return ''

def advance(loc, angle, amt):
    new_loc = loc.copy()
    new_loc[0] += math.cos(math.radians(angle)) * amt
    new_loc[1] += math.sin(math.radians(angle)) * amt
    return new_loc

def playSound(sfx):
    global sfxEnabled
    if(sfxEnabled):
        pygame.mixer.Sound.play(sfx)

def game():
    global platforms, musicOn, score, win, fake_win
    
    run = True
    
    player = Player()
    clock = pygame.time.Clock()
    
    cameraShift = 0
    player.dx = 0
    
    laser_timer = 0
    maxLasers = 1

    global player_dead
    player_dead = False

    platforms.clear()
    particles.clear()
    other_particles.clear()
    lasers.clear()
    score = 0

    platforms.append(Platform(500))
    player.dy = -10

    pygame.mixer.music.load(os.path.join(s, "music.mp3"))
    pygame.mixer.music.set_volume(0.25)
    
    if musicOn:
        pygame.mixer.music.play(-1)

    while run:
        fake_win.fill(color.background_color)
        score = int(cameraShift/200)
        clock.tick(60)

        laser_timer += 1
        if(laser_timer > random.randint(500,1000)):
            if score>=100 and score<125:
                maxLasers = 2
            elif score>125:
                maxLasers = 2
            newLaser(score, maxLasers)
            laser_timer = 0

        # generating new plats
        newPlatforms(cameraShift, score)
        
        player.dy += player.gravity
        player.setY(player.y + player.dy)
        
        # Check if hits bottom relative to camera shift
        if player.y > 680-cameraShift and not player_dead:
           player.kill()
           player_dead = True
        
        # Getting the Camera Shift 
        if player.y < fake_win.get_height() // 2 - 40:
            temp = -player.y + fake_win.get_height()/2 - 20
            if temp>cameraShift:
                cameraShift = temp
            else:
                pass

        if random.randint(1, 60) == 1:
            square_effects.append([[random.randint(0, fake_win.get_width()), -80], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 40), random.randint(10, 30) / 500])
        # this is stolen from dafluffypotato sorry ¯\_(ツ)_/¯
        for i, effect in sorted(enumerate(square_effects), reverse=True): # loc, rot, speed, size, decay
            effect[0][1] += effect[2]
            effect[1] += effect[2] * effect[4]
            effect[3] -= effect[4]
            points = [
                advance(effect[0], math.degrees(effect[1]), effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 90, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 180, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 270, effect[3]),
            ]
            points = [[v[0], v[1]] for v in points]
            if effect[3] < 1:
                square_effects.pop(i)
            else:
                pygame.draw.polygon(fake_win, color.polygon_color, points, 2)

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
                if player.rect.colliderect(plat.rect) and player.dy>=0 and player.rect.bottom <= (plat.y+cameraShift+8): # +5 is the tolerance, kinda room for error
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
                            particles.append(Particle([plat.x, plat.y+20], [random.randint(0, 20) / 10 - 1, random.uniform(-2.0,-4.0)], random.randint(2, 8),color.breaking_color))
                        plat.y = 1000

        # score
        output = "Score = %d" % score
        #textSurface = score_font.render(output, False, color.white)
        #win.blit(textSurface,(0,0))
        draw_text(output, button_Font, color.white, fake_win, 20)

        if(score>=100):
            maxLasers = 2
        else:
            maxLasers = 1

        for laser in lasers:
            laser.shift()
            laser.drawLaser(player)

        # Drawing Particles 
        for particle in particles:
            particle.pos[0] += particle.vel[0]
            particle.pos[1] += particle.vel[1]
            particle.timer -= 0.05
            particle.vel[1] += 0.1

            pygame.draw.circle(fake_win, particle.color, [int(particle.pos[0]), int(particle.pos[1])+cameraShift], int(particle.timer))
            # Removing old particles 
            if particle.timer <= 0:
                particles.remove(particle)

        # drawing laser particles
        for particle in other_particles:
            particle.pos[0] += particle.vel[0]
            particle.pos[1] += particle.vel[1]
            particle.timer -= 0.05
            particle.vel[1] += 0.1

            pygame.draw.circle(fake_win, particle.color, [int(particle.pos[0]), int(particle.pos[1])], int(particle.timer))
            # Removing old particles 
            if particle.timer <= 0:
                other_particles.remove(particle)

        if(player_dead):
            if(len(other_particles)==0):
                deathScreen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == VIDEORESIZE:
                win = pygame.display.set_mode(event.size, RESIZABLE | DOUBLEBUF)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.dx = -10 
                if event.key == pygame.K_d:
                    player.dx = 10
                if event.key == pygame.K_LEFT:
                    player.dx = -10
                if event.key == pygame.K_RIGHT:
                    player.dx = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.dx = 0 
                if event.key == pygame.K_d:
                    player.dx = 0
                if event.key == pygame.K_LEFT:
                    player.dx = 0
                if event.key == pygame.K_RIGHT:
                    player.dx = 0

        # Stay in bounds  
        if not player.x+player.dx < 0 and not player.x+player.dx > 450:
            player.setX(player.x + player.dx)

        if not player_dead:
            player.drawPlayer(cameraShift)
        
        win.blit(pygame.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pygame.display.update()

    pygame.quit()

checkMusic = True

def menu():
    global musicOn, checkMusic, win, fake_win
    check = ''
    buttons.clear()

    play = Button(75, 225, 225, 'Play')
    shop = Button(75, 225, 325, 'Shop')
    option = Button(75, 225, 425, 'Options')
    stop = Button(75, 225, 525, 'Quit')

    buttons.append(play)
    buttons.append(shop)
    buttons.append(option)
    buttons.append(stop)

    if musicOn and checkMusic:
        pygame.mixer.music.load(os.path.join(s, "menuMusic.mp3"))
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
    selected = 0
    while True:
        fake_win.fill(color.background_color)
        
        if random.randint(1, 60) == 1:
            square_effects.append([[random.randint(0, fake_win.get_width()), -80], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 40), random.randint(10, 30) / 500])
        for i, effect in sorted(enumerate(square_effects), reverse=True): # loc, rot, speed, size, decay
            effect[0][1] += effect[2]
            effect[1] += effect[2] * effect[4]
            effect[3] -= effect[4]
            points = [
                advance(effect[0], math.degrees(effect[1]), effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 90, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 180, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 270, effect[3]),
            ]
            points = [[v[0], v[1]] for v in points]
            if effect[3] < 1:
                square_effects.pop(i)
            else:
                pygame.draw.polygon(fake_win, color.polygon_color, points, 2)
        
        draw_text('Py-Jump', main_Font, color.moving_color, fake_win, 125)
        draw_text('Beta 1.2', score_font, color.moving_color, fake_win, 175)
        draw_text('By : Judson Salinas', name_font, color.platform_color, fake_win, 680)
        
        #mouse = pygame.mouse.get_pos()
        for button in buttons:
            button.color = color.platform_color
        check_hover(selected)
        
        if(check == 'Play'):
            playSound(selectSound)
            pygame.mixer.music.fadeout(1000)
            game()
        elif(check == 'Shop'):
            playSound(selectSound)
            store()
        elif(check == 'Options'):
            playSound(selectSound)
            options()
        elif(check == 'Quit'):
            playSound(selectSound)
            time.sleep(0.25)
            pygame.quit()
            sys.exit()

        for button in buttons:
            button.draw_button()
            button.add_text()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                win = pygame.display.set_mode(event.size, RESIZABLE | DOUBLEBUF)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_w:
                    if(selected>0):
                        selected -= 1
                    else:
                        selected = 3
                if event.key == K_s:
                    if(selected<3):
                        selected += 1
                    else:
                        selected = 0
                if event.key == K_DOWN:
                    if(selected<3):
                        selected += 1
                    else:
                        selected = 0
                if event.key == K_UP:
                    if(selected>0):
                        selected -= 1
                    else:
                        selected = 3
                if event.key == K_RETURN:
                    check = buttons[selected].text

        win.blit(pygame.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

def options():
    global musicOn, checkMusic, sfxEnabled, win, fake_win
    buttons.clear()
    check = ''
    #pygame.mixer.music.load(os.path.join(s, "menuMusic.mp3"))
    #pygame.mixer.music.set_volume(0.25)

    #pygame.mixer.music.play(-1)

    mus = Button(75, 225, 225, 'Music')
    sfx = Button(75, 225, 325, 'SFX')
    res = Button(75, 225, 425, 'Reset')
    back = Button(75, 225, 525, "Back")

    buttons.append(mus)
    buttons.append(sfx)
    buttons.append(res)
    buttons.append(back)

    selected = 0
    while True:
        fake_win.fill(color.background_color)
        
        if random.randint(1, 60) == 1:
            square_effects.append([[random.randint(0, fake_win.get_width()), -80], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 40), random.randint(10, 30) / 500])
        for i, effect in sorted(enumerate(square_effects), reverse=True): # loc, rot, speed, size, decay
            effect[0][1] += effect[2]
            effect[1] += effect[2] * effect[4]
            effect[3] -= effect[4]
            points = [
                advance(effect[0], math.degrees(effect[1]), effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 90, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 180, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 270, effect[3]),
            ]
            points = [[v[0], v[1]] for v in points]
            if effect[3] < 1:
                square_effects.pop(i)
            else:
                pygame.draw.polygon(fake_win, color.polygon_color, points, 2)
        
        draw_text('Options', main_Font, color.moving_color, fake_win, 125)

        for button in buttons:
            button.color = color.platform_color
        check_hover(selected)

        if(check == 'Music'):
            playSound(selectSound)
            pygame.mixer.music.stop()
            if musicOn:
                musicOn = False
            else:
                pygame.mixer.music.play(-1)
                musicOn = True
            check = ''
        elif(check == 'SFX'):
            playSound(selectSound)
            if sfxEnabled:
                sfxEnabled = False
            else:
                sfxEnabled = True
            check = ''
        elif(check == 'Back'):
            playSound(selectSound)
            checkMusic = False
            menu()
        elif(check == 'Reset'):
            playSound(selectSound)
            areYouSure()

        for button in buttons:
            button.draw_button()
            button.add_text()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                win = pygame.display.set_mode(event.size, RESIZABLE | DOUBLEBUF)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_w:
                    if(selected>0):
                        selected -= 1
                    else:
                        selected = 3
                if event.key == K_s:
                    if(selected<3):
                        selected += 1
                    else:
                        selected = 0
                if event.key == K_DOWN:
                    if(selected<3):
                        selected += 1
                    else:
                        selected = 0
                if event.key == K_UP:
                    if(selected>0):
                        selected -= 1
                    else:
                        selected = 3
                if event.key == K_RETURN:
                    check = buttons[selected].text
        
        win.blit(pygame.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

def store():
    global checkMusic, win, fake_win
    buttons.clear()
    back = Button(75, 225, 225, "Back")
        
    buttons.append(back)

    check = ''
    selected = 0
    while True:
        fake_win.fill(color.background_color)
        
        if random.randint(1, 60) == 1:
            square_effects.append([[random.randint(0, fake_win.get_width()), -80], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 40), random.randint(10, 30) / 500])
        for i, effect in sorted(enumerate(square_effects), reverse=True): # loc, rot, speed, size, decay
            effect[0][1] += effect[2]
            effect[1] += effect[2] * effect[4]
            effect[3] -= effect[4]
            points = [
                advance(effect[0], math.degrees(effect[1]), effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 90, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 180, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 270, effect[3]),
            ]
            points = [[v[0], v[1]] for v in points]
            if effect[3] < 1:
                square_effects.pop(i)
            else:
                pygame.draw.polygon(fake_win, color.polygon_color, points, 2)
        
        draw_text('Under', button_Font, color.moving_color, fake_win, 125)
        draw_text('Construction', button_Font, color.moving_color, fake_win, 160)

        for button in buttons:
            button.color = color.platform_color
        check_hover(selected)

        if(check == 'Back'):
            playSound(selectSound)
            checkMusic = False
            menu()
        
        for button in buttons:
            button.draw_button()
            button.add_text()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                win = pygame.display.set_mode(event.size, RESIZABLE | DOUBLEBUF)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RETURN:
                    check = buttons[selected].text
        
        win.blit(pygame.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

def deathScreen():
    global score, win, fake_win

    scoreNotChecked = True

    while True:
        fake_win.fill(color.background_color)

        if random.randint(1, 60) == 1:
            square_effects.append([[random.randint(0, fake_win.get_width()), -80], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 40), random.randint(10, 30) / 500])
        for i, effect in sorted(enumerate(square_effects), reverse=True): # loc, rot, speed, size, decay
            effect[0][1] += effect[2]
            effect[1] += effect[2] * effect[4]
            effect[3] -= effect[4]
            points = [
                advance(effect[0], math.degrees(effect[1]), effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 90, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 180, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 270, effect[3]),
            ]
            points = [[v[0], v[1]] for v in points]
            if effect[3] < 1:
                square_effects.pop(i)
            else:
                pygame.draw.polygon(fake_win, color.polygon_color, points, 2)

        if(scoreNotChecked):
            try:
                with open('score.dat', 'rb') as file:
                    score_data = pickle.load(file)
            except:
                score_data = 0

            if(score>score_data):
                isHighScore = True
                with open('score.dat', 'wb') as file:
                    pickle.dump(score, file)
                    file.close()
                with open('score.dat', 'rb') as file:
                    score_data = pickle.load(file)
                    file.close()
            else:
                isHighScore = False
            
            scoreNotChecked = False

        if(isHighScore):
            draw_text('New High Score!', button_Font, color.platform_color, fake_win, 250)
              
        draw_text('Score = %d' % score, main_Font, color.moving_color, fake_win, 300)
        draw_text('Current High Score = %d' % score_data, score_font, color.platform_color, fake_win, 355)
        draw_text('ESC to Continue', score_font, color.platform_color, fake_win, 390)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                win = pygame.display.set_mode(event.size, RESIZABLE | DOUBLEBUF)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playSound(selectSound)
                    checkMusic = True
                    menu()

        win.blit(pygame.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

def areYouSure():
    global checkMusic, win, fake_win
    buttons.clear()

    yes = Button(75, 225, 225, 'Yes')
    no = Button(75,225, 325, 'No')

    buttons.append(yes)
    buttons.append(no)

    selected = 0
    check = ''
    while True:
        fake_win.fill(color.background_color)

        if random.randint(1, 60) == 1:
            square_effects.append([[random.randint(0, fake_win.get_width()), -80], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 40), random.randint(10, 30) / 500])
        for i, effect in sorted(enumerate(square_effects), reverse=True): # loc, rot, speed, size, decay
            effect[0][1] += effect[2]
            effect[1] += effect[2] * effect[4]
            effect[3] -= effect[4]
            points = [
                advance(effect[0], math.degrees(effect[1]), effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 90, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 180, effect[3]),
                advance(effect[0], math.degrees(effect[1]) + 270, effect[3]),
                ]
            points = [[v[0], v[1]] for v in points]
            if effect[3] < 1:
                square_effects.pop(i)
            else:
                pygame.draw.polygon(fake_win, color.polygon_color, points, 2)

        draw_text('Are you Sure?', button_Font, color.moving_color, fake_win, 115)
        draw_text('(This Will Reset', score_font, color.platform_color, fake_win, 155)
        draw_text('All High Scores)', score_font, color.platform_color, fake_win, 190)
        
        for button in buttons:
            button.color = color.platform_color
        check_hover(selected)

        if(check == 'Yes'):
            checkMusic = False
            with open('score.dat', 'wb') as file:
                    pickle.dump(0, file) 
            options()
        elif(check == 'No'):
            checkMusic = False
            options()

        for button in buttons:
            button.draw_button()
            button.add_text()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                win = pygame.display.set_mode(event.size, RESIZABLE | DOUBLEBUF)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_w:
                    if(selected>0):
                        selected -= 1
                    else:
                        selected = 1
                if event.key == K_s:
                    if(selected<1):
                        selected += 1
                    else:
                        selected = 0
                if event.key == K_DOWN:
                    if(selected<1):
                        selected += 1
                    else:
                        selected = 0
                if event.key == K_UP:
                    if(selected>0):
                        selected -= 1
                    else:
                        selected = 1
                if event.key == K_RETURN:
                    check = buttons[selected].text

        win.blit(pygame.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

menu()
