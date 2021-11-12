import pygame

pygame.init()
win = pygame.display.set_mode([500,700])


lines = []


cameraShift = 0
prePoint = None

#colors
class color():

    black = (0,0,0) # normal string
    navy = (20,33,61) # maybe some kind of special string
    orange = (252, 163, 17) # ball
    grey = (229, 229, 229) # background 
    white = (255,255,255)

class Line:
    def __init__(self, pos, prev):
        self.pos = pos
        self.pre =  prev
        self.line_rect = None
    
    def setPre(self, pos):
        self.pre = pos

    def getPos(self):
        return self.pos

    def drawLine(self, cameraShift):
        pygame.draw.line(win, color.black, (self.pre[0], self.pre[1]+cameraShift), (self.pos[0], self.pos[1]+cameraShift), 10)

class Ball:
    def __init__(self):
        self.x = 250
        self.y = 350
        self.dx = 0
        self.dy = 0
        self.gravity = 0.3
        self.ball_rect = pygame.Rect(self.x,self.y,40,40)

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x

    def drawBall(self,cameraShift):
        self.ball_rect = pygame.Rect(self.x-20, self.y+cameraShift-20, 40,40)
        pygame.draw.circle(win, color.orange, (self.x, self.y+cameraShift), 20)

    def getRect(self):
        return self.ball_rect

def reset():
    global prevLine, previous_point
    prevLine.clear()
    prevLine.append([(250,650), (250,650)])
    previous_point = (250,650)
    win.fill((255,255,255))

def main():
    run = True
    ball = Ball()
    clock = pygame.time.Clock()
    cameraShift = 0
    fir = Line((250,700), (250,700))
    lines.append(fir)
    prePoint = (250,700)
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
                lines.append(Line((event.pos[0], event.pos[1]-cameraShift), prePoint))
                prePoint = (event.pos[0], event.pos[1]-cameraShift)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset()
        pygame.display.update()
        win.fill(color.grey)
        for line in lines:
            line.drawLine(cameraShift)
        ball.drawBall(cameraShift)
    pygame.quit()


main()
