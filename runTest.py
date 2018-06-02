from pygame import *
from rotateMain import rotateBlit, _sind, _cosd
from Limb import Limb
from keyframelist import KeyFrame, KeyFrameList
screen = display.set_mode((800,600))
running = True
legSpriteR = Surface((32,8),SRCALPHA)
legSpriteL = Surface((32,8),SRCALPHA)
legSpriteR.fill((200,200,200))
legSpriteL.fill((255,255,255))
font.init()
aFont = font.SysFont('Consolas',30)

upperLegL = Limb(400,300,0,28,legSpriteL, (2,4))
lowerLegL = Limb(0,0,0,28,legSpriteL, (2,4))
lowerLegL.parent_limb = upperLegL

upperLegR = Limb(400,300,0,28,legSpriteR, (2,4))
lowerLegR = Limb(0,0,0,28,legSpriteR, (2,4))
lowerLegR.parent_limb = upperLegR

upperLegKeyframesWalkingR = KeyFrameList().load_from_file(open('keyframes/walking/upperLegWalkingR.txt'))
upperLegKeyframesWalkingL = KeyFrameList().load_from_file(open('keyframes/walking/upperLegWalkingL.txt'))
lowerLegKeyframesWalkingR = KeyFrameList().load_from_file(open('keyframes/walking/lowerLegWalkingR.txt'))
lowerLegKeyframesWalkingL = KeyFrameList().load_from_file(open('keyframes/walking/lowerLegWalkingL.txt'))

upperLegKeyframesCrouchingL = KeyFrameList().load_from_file(open('keyframes/crouching/upperLegCrouchingL.txt'))
upperLegKeyframesCrouchingR = KeyFrameList().load_from_file(open('keyframes/crouching/upperLegCrouchingR.txt'))
lowerLegKeyframesCrouchingL = KeyFrameList().load_from_file(open('keyframes/crouching/lowerLegCrouchingL.txt'))
lowerLegKeyframesCrouchingR = KeyFrameList().load_from_file(open('keyframes/crouching/lowerLegCrouchingR.txt'))

upperLegStandingL = KeyFrameList()
upperLegStandingL.add_keyframe(KeyFrame(0,275))
upperLegStandingL.add_keyframe(KeyFrame(100,285))
upperLegStandingL.add_keyframe(KeyFrame(200,275))

upperLegStandingR = KeyFrameList()
upperLegStandingR.add_keyframe(KeyFrame(0,265))
upperLegStandingR.add_keyframe(KeyFrame(100,260))
upperLegStandingR.add_keyframe(KeyFrame(200,265))

lowerLegStandingL = KeyFrameList()
lowerLegStandingL.add_keyframe(KeyFrame(0,-5))
lowerLegStandingL.add_keyframe(KeyFrame(100,-15))
lowerLegStandingL.add_keyframe(KeyFrame(200,-5))

lowerLegStandingR = KeyFrameList()
lowerLegStandingR.add_keyframe(KeyFrame(0,-5))
lowerLegStandingR.add_keyframe(KeyFrame(100,-15))
lowerLegStandingR.add_keyframe(KeyFrame(200,-5))

animations = [(upperLegKeyframesWalkingR,lowerLegKeyframesWalkingR, upperLegKeyframesWalkingL,lowerLegKeyframesWalkingL), (upperLegKeyframesCrouchingR,lowerLegKeyframesCrouchingR,upperLegKeyframesCrouchingL,lowerLegKeyframesCrouchingL), (upperLegStandingR, lowerLegStandingR, upperLegStandingL, lowerLegStandingL)]
currentAnimation = animations[2]
limbs = [upperLegR, lowerLegR, upperLegL, lowerLegL]
oldAnimation = currentAnimation
nextAnimation = currentAnimation
timer = 0
wasTransitioning = False
changeTimer = -60
animationOffset = 0
clockity = time.Clock()
WALKING = 0
CROUCHING = 1
STANDING = 2
def set_animation(animationNumber):
    global changeTimer, oldAnimation, nextAnimation, wasTransitioning
    if currentAnimation != animations[animationNumber] and nextAnimation != animations[animationNumber]\
     and not wasTransitioning:
        changeTimer = timer
        oldAnimation = currentAnimation
        nextAnimation = animations[animationNumber]
        wasTransitioning = True
        print('switch', timer-changeTimer, animationNumber)
def set_facing(left=False):
    global wasTransitioning
    if not wasTransitioning:
        for i in limbs:
            i.reflect = left
keysDown = [False for i in range(4)]
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
    if keysDown[0]:
        #if currentAnimation != animations[WALKING] and nextAnimation != animations[WALKING]:
            set_facing(left = True)
            set_animation(WALKING)
    elif keysDown[1]:
        #if currentAnimation != animations[WALKING] and nextAnimation != animations[WALKING]:
            set_facing(left = False)
            set_animation(WALKING)
    if keysDown[2]:
        #if currentAnimation != animations[CROUCHING] and nextAnimation != animations[CROUCHING]:
            set_animation(CROUCHING)
    if not any(keysDown):
        set_animation(STANDING)
    #print(changeTimer, currentAnimation == animations[0])
    for a,l, n in zip(currentAnimation, limbs, nextAnimation):
        posData, doneSwitch = a.transition(n, changeTimer-animationOffset, timer-animationOffset, 30)
        if doneSwitch:
            if doneSwitch and wasTransitioning:
                #print('switch done', timer-changeTimer)
                currentAnimation = nextAnimation
                wasTransitioning = False
                animationOffset = timer
                break
            l.rotation = a.current_position(timer-animationOffset)[0]
        else:
            l.rotation = posData[0]
    screen.fill((0,0,0))
    screen.blit(aFont.render('%3d'%(timer%200),True,(255,255,255)),(10,10))
    for i in limbs:
        i.draw(screen)
    lowerLimb = max(lowerLegL.get_tip_pos()[1],lowerLegR.get_tip_pos()[1])
    draw.line(screen,(0,255,0), (0,lowerLimb),(800,lowerLimb),3)
    display.flip()
    timer+=1
    clockity.tick(60)
quit()
