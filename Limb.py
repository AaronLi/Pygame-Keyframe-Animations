from pygame import *
from rotateMain import rotateBlit, _sind, _cosd
class Limb:
    def __init__(self, x, y, rotation, length, sprite, rotatePoint):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.length = length
        self.sprite = sprite
        self.parent_limb = None
        self.rotatePoint = rotatePoint
        self.reflect = False
    def get_tip_pos(self, integer = False):
        tipX, tipY = self.get_pos()
        if self.reflect:
            tipX+=self.length*_cosd(180+self.get_rotation())
            tipY+=self.length*_sind(180+self.get_rotation())
        else:
            tipX+=self.length*_cosd(-self.get_rotation())
            tipY+=self.length*_sind(-self.get_rotation())
        if integer:
            return int(tipX), int(tipY)
        else:
            return tipX, tipY
    def draw(self, surface):
        if self.parent_limb == None:
            if self.reflect:
                rotateBlit(surface, self.sprite, self.get_pos(), self.rotatePoint, 180-self.get_rotation())
            else:
                rotateBlit(surface, self.sprite, self.get_pos(), self.rotatePoint, self.get_rotation())
            surface.set_at(self.get_pos(True), (255,0,0))
            surface.set_at(self.get_tip_pos(True), (0,0,255))
        else:
            if self.reflect:
                rotateBlit(surface, self.sprite, self.get_pos(), self.rotatePoint, 180-self.get_rotation())
            else:
                rotateBlit(surface, self.sprite, self.get_pos(), self.rotatePoint, self.get_rotation())
            surface.set_at(self.get_pos(True), (255,0,0))
            surface.set_at(self.get_tip_pos(True), (0,0,255))
    def get_rotation(self):
        rotOut = self.rotation
        limb = self.parent_limb
        while limb != None:
            rotOut+=limb.get_rotation()
            limb = limb.parent_limb
        return rotOut
    def get_pos(self, integer=False):
        if self.parent_limb == None:
            x, y = self.x, self.y
            if integer:
                return int(x), int(y)
            else:
                return x, y
        else:
            x, y = self.parent_limb.get_tip_pos()
            if integer:
                return int(x), int(y)
            else:
                return x, y
