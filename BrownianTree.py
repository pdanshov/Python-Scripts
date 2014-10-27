import sys                        
import pygame                    
from pygame.locals import * #constants from pygame.locals - like OPENGL, K_1, etc...
import pygame.font as font
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randint
import random
import numpy as np
import math
import objloader
import geometry
from progressbar import ProgressBar

sqr = lambda x: x*x

if False: #fullscreen
        fs = FULLSCREEN
        RESOLUTION = (1280,800)
else:
        RESOLUTION = (800,600)
        fs = 0



#### LOADING  ###############################

cow = objloader.OBJ("models/cow2.obj")

def readtetrahedronlist(fn):
        counter = 0
        res = []
        with open(fn,"r") as f:
                for line in f:
                        if counter%4 == 0:
                                a = eval(line)
                        elif counter%4 == 1:
                                b = eval(line)
                        elif counter%4 == 2:
                                c = eval(line)
                        elif counter%4 == 3:
                                d = eval(line)
                                res.append(geometry.Tetrahedron(a,b,c,d))
                        counter+=1
        return res


def evalfile(fn):
        return eval(open(fn,"r").read())


points = evalfile("models/cow2.int")[:5]
print "We have %d points inside mesh." % len(points)
print "And %d points on mesh." % len(cow.vertices)
points = points + cow.vertices
random.shuffle(points)

bar = ProgressBar()
l = len(points)
i = 0
tetr = geometry.Tetrahedron()
for p in points:
        i+=1
        bar.render(i*100/l)
        tetr.split(p)

#print "and now cut cow"
#tetr.mesh_cut(cow)
#tetr.save_to_file("tetrahedrons.txt",True)

#### INIT #####################################
pygame.init()  
pygame.display.set_caption("Hello 3D!")
screen= pygame.display.set_mode(RESOLUTION,OPENGL|DOUBLEBUF|fs)

def reSetProjection():
        glMatrixMode(GL_PROJECTION)            
        glLoadIdentity()                      
        ysc = 5.0* RESOLUTION[1]/RESOLUTION[0]
        glOrtho(-5,5,-ysc,ysc,-5,5)
        glMatrixMode(GL_MODELVIEW)

reSetProjection()
glClearColor(0.0,0.0,0.0,0.0)
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
glEnable(GL_COLOR_MATERIAL)

glPointSize(3)
glEnable(GL_LIGHTING)
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_DEPTH_TEST)

cow.genlist()
tetr.genlist()

tetrascow = readtetrahedronlist("tetrahedrons.txt")

loaded_list = glGenLists(1)
glNewList(loaded_list,GL_COMPILE)
glBegin(GL_TRIANGLES)
for t in tetrascow:
        t.draw()
glEnd()
glEndList()

class palette:
        colors = [(0,1,1),(1,0,1),(1,1,0)]


polygonmode = 2
def changemode():
        global polygonmode
        polygonmode = (polygonmode + 1) % 3
        if polygonmode ==0:
                glPolygonMode(GL_FRONT,GL_LINE)
                glPolygonMode(GL_BACK,GL_LINE)
        elif polygonmode == 1:
                glPolygonMode(GL_FRONT,GL_FILL)
                glPolygonMode(GL_BACK,GL_FILL)
        elif polygonmode == 2:
                glPolygonMode(GL_FRONT,GL_POINT)
                glPolygonMode(GL_BACK,GL_POINT)

changemode()
class SceneRotator:
        def __init__(self):
                self.x = 0.0
                self.y = 0.0
                self.z = 0.0
                self.d = 1.0
        def _normangle(self,x):
                if x<0:
                        return 360+x
                elif x>360:
                        return x-360
                else:
                        return x
        def do(self):
                self.x,self.y,self.z = map(self._normangle,(self.x,self.y,self.z))
                glLoadIdentity()
                glRotate(self.y,0,1,0)
                glRotate(self.x,1,0,0)
                glRotate(self.z,0,0,1)

                glScale(self.d,self.d,self.d)

scenerot = SceneRotator()

DRAW_GRID = False
DRAW_COW = False
DRAW_TETR = False
DRAW_POINTS = False
DRAW_LOADED = True

def draw ():
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        scenerot.do()
        if DRAW_GRID:
                glDisable(GL_LIGHTING)
                glBegin(GL_LINES)
                for i in xrange(-10,11):
                        if i % 10 == 0:
                                glColor(0.0,1.0,0.0)
                        else:
                                glColor(0.0,0.3,0.0)
                        glVertex(i,0,-10)
                        glVertex(i,0,10)

                        glVertex(-10,0,i)
                        glVertex(10,0,i)
                glEnd()
                glEnable(GL_LIGHTING)
        if DRAW_COW:
                glColor(1,1,1)
                glCallList(cow.gl_list)
        if DRAW_TETR:
                glColor(0,0,1)
                glCallList(tetr.gl_list)

        if DRAW_LOADED:
                glColor(0,0,1)
                glCallList(loaded_list)
        if DRAW_POINTS:
                glColor(1,0,0)
                glBegin(GL_POINTS)
                for i in points:
                        glVertex(i[0],i[1],i[2])
                glEnd()

        glFlush()                                # Flush everything to screen ASAP
        pygame.display.flip()


pygame.mouse.set_visible(False)
pygame.event.set_allowed(None)
pygame.event.set_allowed([QUIT,MOUSEMOTION,MOUSEBUTTONDOWN])

mouselock = False
def processinput():
        global DRAW_LOADED, DRAW_GRID, DRAW_COW, DRAW_POINTS, DRAW_TETR
        global mouselock
        event=pygame.event.poll()

        if event.type is QUIT:
                sys.exit(0)
        key = pygame.key.get_pressed()
        if key[K_ESCAPE] or key[K_q]: sys.exit(0)
        if key[K_m]: changemode()
        if key[K_w]: scenerot.d /=1.1
        if key[K_s]: scenerot.d *=1.1
        if key[K_l]: mouselock = not mouselock
        if key[K_a]: scenerot.y+=5.0
        if key[K_d]: scenerot.y-=5.0
        if key[K_r]: scenerot.x+=5.0
        if key[K_f]: scenerot.x-=5.0
        '''
        if key[K_l]:
                DRAW_LOADED = not DRAW_LOADED
                key[K_l] = False
        if key[K_g]: DRAW_GRID = not DRAW_GRID
        if key[K_t]:
                DRAW_TETR = not DRAW_TETR
                key[K_t] = False
        if key[K_p]: DRAW_POINTS = not DRAW_POINTS
        if key[K_c]: DRAW_COW = not DRAW_COW
        '''
       
        if fs==FULLSCREEN:
                if event.type is MOUSEMOTION:
                        if mouselock:
                                return
                        x,y = pygame.mouse.get_rel()
                        scenerot.y+=x/10.0
                        scenerot.x+=y/10.0
while 1:
        processinput()
        draw()

