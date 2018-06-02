from bisect import insort
from pygame import Surface, image, transform
class KeyFrameList:
    '''
Used for creating continous linear piecewise functions that go through given points (keyframes)
    '''
    def __init__(self):
        self.keyframes = []
    def add_keyframe(self, newKeyframe):
        insort(self.keyframes, newKeyframe)
    def load_from_file(self, file):
        time, rot, x, y = None, None, 0, 0
        for i in file:
            data =[float(j) for j in i.split()]
            if len(data) == 4:
                time, rot, x, y = data
            else:
                time, rot = data
            self.add_keyframe(KeyFrame(time, rot, x, y))
        return self
    def switch_between_frames(self, k1, k2, time):
        '''
            [KeyFrame], [KeyFrame], int -> int, int ,int
        '''
        timeRange = k2.time-k1.time
        upperProportion = (time-k1.time)/timeRange
        lowerProportion = 1-upperProportion
        angOut = k1.rotation*lowerProportion+k2.rotation*upperProportion
        xOut = k1.x*lowerProportion+k2.x*upperProportion
        yOut = k1.y*lowerProportion+k2.y*upperProportion
        return angOut, xOut, yOut
    def current_position(self, time):
        time = time%self.keyframes[-1].time
        if len(self.keyframes)>1:
            for i in range(0,len(self.keyframes)-1):
                if self.keyframes[i].time<=time<=self.keyframes[i+1].time:
                    k1, k2 = self.keyframes[i], self.keyframes[i+1]
                    return self.switch_between_frames(k1,k2,time)
                
    def transition(self, nextAnimation, lastTime, time, duration):
        '''
lastTime is the last time value that was given to the current_position of the current animation
time is the current value to be used for transitioning between the two animations
duration is the amount of time it should take to transfer to the next animation
'''
        lastAnimationPosition = self.current_position(lastTime)
        nextAnimationPosition = nextAnimation.keyframes[0].get_clone()
        nextAnimationPosition.time = duration
        #print(time-lastTime)
        return self.switch_between_frames(KeyFrame(0, lastAnimationPosition[0], lastAnimationPosition[1], lastAnimationPosition[2]), nextAnimationPosition, time-lastTime), time-lastTime>duration
        
    def visualize(self,resolution = 1):
        rotations = [i.rotation for i in self.keyframes]
        xPositions = [i.x for i in self.keyframes]
        yPositions = [i.y for i in self.keyframes]
        maxRotation = max(rotations)
        minRotation = min(rotations)
        maxX = max(xPositions)
        minX = min(xPositions)
        maxY = max(yPositions)
        minY = min(yPositions)
        lowestPoint = min([minX,minY,minRotation])
        highestPoint = max([maxX,maxY,maxRotation])
        timeEnd = self.keyframes[-1].time
        sOut = Surface((timeEnd+20, highestPoint-lowestPoint+20))
        sOut.fill((255,255,255))
        point = 0
        while point< timeEnd:
            #print(self.current_position(point))
            rot,x,y = self.current_position(point)
            sOut.set_at((int(point+10),sOut.get_height()-int(rot-lowestPoint+10)),(255,0,0))
            sOut.set_at((int(point+10),sOut.get_height()-int(x-lowestPoint+10)),(0,255,0))
            sOut.set_at((int(point+10),sOut.get_height()-int(y-lowestPoint+10)),(0,0,255))
            point+=resolution
        sOut = transform.smoothscale(sOut,(sOut.get_width()*4,sOut.get_height()*4))
        image.save(sOut,'rotationVisual.png')
class KeyFrame:
    def __init__(self, time, rotation, x=0, y=0, has_parent = True):
        self.time = time
        self.rotation = rotation
        self.x = x
        self.y = y
        self.has_parent = has_parent
    def get_clone(self):
        return KeyFrame(self.time, self.rotation, self.x, self.y, self.has_parent)
    def __lt__(self, other):
        return self.time<other.time
    def __str__(self):
        return 'time: %d angle: %.3f position: (%d, %d)'%(self.time, self.rotation, self.x, self.y)
