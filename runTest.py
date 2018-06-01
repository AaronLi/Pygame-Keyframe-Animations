from pygame import *
from rotateMain import rotateBlit, _sind, _cosd
from Limb import Limb
from keyframelist import KeyFrame, KeyFrameList
screen = display.set_mode((800,600))
running = True
legSprite = Surface((32,8),SRCALPHA)
legSprite.fill((255,255,255))
font.init()
aFont = font.SysFont('Consolas',30)

upperLegL = Limb(400,300,0,28,legSprite, (2,4))
lowerLegL = Limb(0,0,0,28,legSprite, (2,4))
lowerLegL.parent_limb = upperLegL

upperLegR = Limb(400,300,0,28,legSprite, (2,4))
lowerLegR = Limb(0,0,0,28,legSprite, (2,4))
lowerLegR.parent_limb = upperLegR

upperLegKeyframesWalkingR = KeyFrameList()
upperLegKeyframesWalkingR.add_keyframe(KeyFrame(0,290))
upperLegKeyframesWalkingR.add_keyframe(KeyFrame(125,250))
upperLegKeyframesWalkingR.add_keyframe(KeyFrame(250,290))

upperLegKeyframesWalkingL = KeyFrameList()
upperLegKeyframesWalkingL.add_keyframe(KeyFrame(0,250))
upperLegKeyframesWalkingL.add_keyframe(KeyFrame(125,290))
upperLegKeyframesWalkingL.add_keyframe(KeyFrame(250,250))

lowerLegKeyframesWalkingR = KeyFrameList()
lowerLegKeyframesWalkingR.add_keyframe(KeyFrame(0,0))
lowerLegKeyframesWalkingR.add_keyframe(KeyFrame(30,0))
lowerLegKeyframesWalkingR.add_keyframe(KeyFrame(125,-20))
lowerLegKeyframesWalkingR.add_keyframe(KeyFrame(220,-10))
lowerLegKeyframesWalkingR.add_keyframe(KeyFrame(250,0))

lowerLegKeyframesWalkingL = KeyFrameList()
lowerLegKeyframesWalkingL.add_keyframe(KeyFrame(0,-20))
lowerLegKeyframesWalkingL.add_keyframe(KeyFrame(95,-10))
lowerLegKeyframesWalkingL.add_keyframe(KeyFrame(125,0))
lowerLegKeyframesWalkingL.add_keyframe(KeyFrame(220,-10))
lowerLegKeyframesWalkingL.add_keyframe(KeyFrame(250,-20))

upperLegKeyframesCrouchingL = KeyFrameList()
upperLegKeyframesCrouchingL.add_keyframe(KeyFrame(0,0))
upperLegKeyframesCrouchingL.add_keyframe(KeyFrame(1,0))
upperLegKeyframesCrouchingR = KeyFrameList()
upperLegKeyframesCrouchingR.add_keyframe(KeyFrame(0,-90))
upperLegKeyframesCrouchingR.add_keyframe(KeyFrame(1,-90))
lowerLegKeyframesCrouchingL = KeyFrameList()
lowerLegKeyframesCrouchingL.add_keyframe(KeyFrame(0,-90))
lowerLegKeyframesCrouchingL.add_keyframe(KeyFrame(1,-90))
lowerLegKeyframesCrouchingR = KeyFrameList()
lowerLegKeyframesCrouchingR.add_keyframe(KeyFrame(0,-90))
lowerLegKeyframesCrouchingR.add_keyframe(KeyFrame(1,-90))

animations = [(upperLegKeyframesWalkingR,lowerLegKeyframesWalkingR, upperLegKeyframesWalkingL,lowerLegKeyframesWalkingL), (upperLegKeyframesCrouchingR,lowerLegKeyframesCrouchingR,upperLegKeyframesCrouchingL,lowerLegKeyframesCrouchingL)]
currentAnimation = animations[0]
limbs = [upperLegR, lowerLegR, upperLegL, lowerLegL]
oldAnimation = currentAnimation
timer = 0
changeTimer = 0
clockity = time.Clock()
while running:
    for e in event.get():
        if e.type==QUIT:
            running = False
        elif e.type==KEYDOWN:
            if e.key == K_w:
                changeTimer = timer
                oldAnimation = currentAnimation
                currentAnimation = animations[0]
            elif e.key == K_c:
                changeTimer = timer
                oldAnimation = currentAnimation
                currentAnimation = animations[1]
    
    for a,l in zip(currentAnimation, limbs):
        l.rotation = a.current_position(timer)[0]
    screen.fill((0,0,0))
    screen.blit(aFont.render('%3d'%(timer%250),True,(255,255,255)),(10,10))
    for i in limbs:
        i.draw(screen)
    display.flip()
    timer+=1
    clockity.tick(60)
quit()
