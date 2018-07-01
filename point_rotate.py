from pygame import *
import math
def _sind(degrees):
    return math.sin(math.radians(degrees))
def _cosd(degrees):
    return math.cos(math.radians(degrees))
def _atand(y, x):
    return math.degrees(math.atan2(y, x))
def rotateBlit(surface: Surface, sprite: Surface, position: tuple, rotationPoint: tuple, rotation: float):
    rotatedSurface = transform.rotate(sprite, rotation)
    posRelToCenter = (rotationPoint[0]-sprite.get_width()/2, rotationPoint[1]-sprite.get_height()/2)
    distFromCenter = math.hypot(posRelToCenter[0], posRelToCenter[1])
    offsetAngle = _atand(posRelToCenter[1], posRelToCenter[0])
    rotateCenter = (rotatedSurface.get_width()/2, rotatedSurface.get_height()/2)
    offsetPoint = (int(rotateCenter[0]+_cosd(-rotation+offsetAngle)*distFromCenter), int(rotateCenter[1]+_sind(-rotation+offsetAngle)*distFromCenter))
    return surface.blit(rotatedSurface, (position[0]-offsetPoint[0], position[1]-offsetPoint[1]))

if __name__ == '__main__':
    screen = display.set_mode((300, 300))
    fancyStick = image.load("handLong.png").convert_alpha()
    fancyStickVertical = image.load("handShort.png").convert_alpha()
    running = True
    clockity = time.Clock()
    angle = 0
    angle2 = 0
    while running:
        for e in event.get():
            if e.type==QUIT:
                running = False
        screen.fill((0, 0, 0))
        draw.circle(screen,(255,255,255), (150, 150), 150)
        for i in range(0,360,30):
            draw.circle(screen, (0,0,0), (150+int(_cosd(i)*130), 150+int(_sind(i)*130)), int(abs(_cosd(4*i)*4)))
        #draw.line(screen,(0,255,255),(0,150),(300,150))
        #draw.line(screen,(0,255,255),(150,0),(150,300))
        draw.rect(screen,(255,0,0), rotateBlit(screen, fancyStick, (150,150), (6,107), angle),3)
        rotateBlit(screen, fancyStickVertical, (150, 150), (64,99), angle2)
        angle -=1.66666667
        angle2-=0.30277777778
        display.flip()
        clockity.tick(60)
    quit()
