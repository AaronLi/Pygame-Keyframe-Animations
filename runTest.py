from pygame import *
from rotateMain import rotateBlit, _sind, _cosd, _atand
from Limb import Limb
from keyframelist import KeyFrame, KeyFrameList
import glob
from Body import Body
screen = display.set_mode((800,600))
running = True
legSpriteR = Surface((32,8),SRCALPHA)
legSpriteL = Surface((32,8),SRCALPHA)
legSpriteR.fill((200,200,200))
legSpriteL.fill((255,255,255))
bodySprite = Surface((36,8), SRCALPHA)
bodySprite.fill((255,255,255))
font.init()
aFont = font.SysFont('Consolas',30)

upperLegL = Limb(400,300,0,28,legSpriteL, (2,4))
lowerLegL = Limb(0,0,0,28,legSpriteL, (2,4))
lowerLegL.parent_limb = upperLegL

upperLegR = Limb(400,300,0,28,legSpriteR, (2,4))
lowerLegR = Limb(0,0,0,28,legSpriteR, (2,4))
lowerLegR.parent_limb = upperLegR


body = Body(bodySprite, 400,300)
body.add_limb(upperLegR, (18,0), 'upperLegR')
body.add_limb(upperLegL, (18,0), 'upperLegL')
body.add_draw_limb(lowerLegR, 'lowerLegR')
body.add_draw_limb(lowerLegL, 'lowerLegL')
body.rotation = 270
body.set_animation('standing')
body.current_animation = 'standing'
clockity = time.Clock()
body.load_from_file('./keyframes/body')
keysDown = [False for i in range(5)]
timer = 0
while running:
    for e in event.get():
        if e.type==QUIT:
            running = False
        elif e.type==KEYDOWN or e.type == KEYUP:
            if e.key == K_a:
                keysDown[0] = e.type==KEYDOWN
            elif e.key == K_d:
                keysDown[1] = e.type==KEYDOWN
            elif e.key == K_s:
                keysDown[2] = e.type==KEYDOWN
            elif e.key == K_w:
                keysDown[3] = e.type==KEYDOWN
            elif e.key == K_LSHIFT:
                keysDown[4] = e.type==KEYDOWN
    if keysDown[0]:
            body.set_facing(left = True)
            body.set_animation('running' if keysDown[4] else 'walking')
            #set_animation(RUNNING if keysDown[4] else WALKING)
    elif keysDown[1]:
            body.set_facing(left = False)
            body.set_animation('running' if keysDown[4] else 'walking')
    if keysDown[2]:
            body.set_animation('crouching')
    if not any(keysDown):
        body.set_animation('standing')
    #body.rotation+=1
    screen.fill((0,0,0))
    #screen.blit(aFont.render('%3d'%(timer%200),True,(255,255,255)),(10,10))
    body.update(timer)
    body.draw(screen)
    lowerLimb = lowerLegL if lowerLegL.get_tip_pos()[1]>lowerLegR.get_tip_pos()[1] else lowerLegR
    draw.line(screen,(0,255,0), (0,lowerLimb.get_tip_pos()[1]),(800,lowerLimb.get_tip_pos()[1]),3)
    #draw.line(screen,(0,0,255), (lowerLimb.get_tip_pos()[0], 0),(lowerLimb.get_tip_pos()[0], 600),3)
    display.flip()
    timer+=1
    clockity.tick(60)
quit()
