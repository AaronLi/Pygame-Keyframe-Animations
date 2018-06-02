from rotateMain import rotateBlit, _sind, _cosd, _atand
from math import hypot
class Body:
    def __init__(self, sprite, x, y):
        self.limbs = {}
        self.rotation = 0
        self.sprite = sprite
        self.x = x
        self.y = y
        self.parent_limb = None
        self.drawing_limbs = []
        self.animation_limbs = {}
        self.animations = {}
        self.current_animation = ''
        self.changeTimer= -60
        self.oldAnimation = None
        self.nextAnimation = None
        self.wasTransitioning = False
        self.animationOffset = 0
        self.timer = 0
    def add_limb(self, limb, position, alias):
        '''
position is relative to center of body
'''
        limb.parent_limb = self
        self.limbs[limb] = position
        self.animation_limbs[alias] = limb
    def draw(self, surface):
        rotateBlit(surface,self.sprite, (self.x, self.y), (self.sprite.get_width()/2, self.sprite.get_height()/2), self.rotation)
        for i in self.drawing_limbs:
            i.draw(surface)
        for i in self.limbs:
            i.draw(surface)
    def update(self, timer):
        self.timer = timer
        animationSet = self.animations[self.current_animation]
        for l in self.animation_limbs:
            posData, doneSwitch = self.animations[self.current_animation][l].transition(self.animations[self.nextAnimation][l], self.changeTimer-self.animationOffset, self.timer-self.animationOffset, 30)
            if doneSwitch:
                if doneSwitch and self.wasTransitioning:
                    self.current_animation = self.nextAnimation
                    self.wasTransitioning = False
                    self.animationOffset = self.timer
                    break
                self.animation_limbs[l].rotation = self.animations[self.current_animation][l].current_position(self.timer-self.animationOffset)[0]
            else:
                self.animation_limbs[l].rotation = posData[0]
    def set_animation(self, nextAnimationName):
        if self.current_animation != nextAnimationName and nextAnimationName != self.nextAnimation\
     and not self.wasTransitioning:
            self.changeTimer = self.timer
            self.oldAnimation = self.current_animation
            self.nextAnimation = nextAnimationName
            self.wasTransitioning = True
    def add_draw_limb(self, limb, alias):
        self.drawing_limbs.append(limb)
        self.animation_limbs[alias] = limb
    def get_tip_pos(self, calling_limb, integer = False):
        limbPos = self.limbs[calling_limb]
        pointDist = hypot(limbPos[0], limbPos[1])
        angleRel = _atand(limbPos[1], limbPos[0])
        xOut, yOut = self.x, self.y
        xOut+=pointDist*_cosd(-(self.rotation+angleRel))
        yOut+=pointDist*_sind(-(self.rotation+angleRel))
        return xOut, yOut
    def get_rotation(self):
        return self.rotation-270
    def add_animation_set(self, animationName, animationSet):
        '''
animationSet should be in the style animationSet[limbAlias:animation]
'''
        self.animations[animationName] = animationSet
    def set_facing(self, left = False):
        if not self.wasTransitioning:
            for i in self.animation_limbs.values():
                i.reflect= left
