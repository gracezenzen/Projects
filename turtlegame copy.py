#Grace Zenzen zenze007

# I understand this is a graded, individual examination that may not be
# discussed with anyone. I also understand that obtaining solutions or
# partial solutions from outside sources, or discussing
# any aspect of the examination with anyone will result in failing the course.
# I further certify that this program represents my own work and that none of
# it was obtained from any source other than material presented as part of the
# course.

#Completed through task 9 (extra credit) and all tasks before (1-8)

from turtle import *
import tkinter.messagebox
import tkinter
import random
import math
import datetime

screenMinX = -500
screenMinY = -500
screenMaxX = 500
screenMaxY = 500

#Task 4 and 9
class LaserBeam(RawTurtle):
    def __init__(self, canvas, x, y, direction, originalDirection, dx, dy):
        super().__init__(canvas)
        self.penup()
        self.goto(x,y)
        self.setheading(direction)
        self.color("Green")
        self.lifespan=200
        if (dx,dy)==(0,0):
            self.__dx=math.cos(math.radians(direction))*2
            self.__dy=math.sin(math.radians(direction))*2
        #Extra credit: Fixes laser path when turtle goes very fast. Treats (dx,dy) of Tiny
        #as a vector, then rotates that vector and multiplies it by 2. Added extra case for when the speed of Tiny==0
        #Rotation is calculated as the diference between the direction the turtle is facing and the direction the turtle is moving
        else:
            rotation=direction-originalDirection
            self.__dx=2*(dx*math.cos(math.radians(rotation)) - dy*math.sin(math.radians(rotation)))
            self.__dy=2*(dx*math.sin(math.radians(rotation))+dy*math.cos(math.radians(rotation)))
        self.shape("laser")

    #Task 4B
    def getLifespan(self):
        return self.lifespan

    def getDX(self):
        return self.__dx

    def getDY(self):
        return self.__dy

    def getRadius(self):
        return 4

    #Task 4C
    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.getDX() + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.getDY() + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.lifespan=self.lifespan-1

        self.goto(x,y)

class Ghost(RawTurtle):
    def __init__(self,canvasobj,dx,dy,x,y,size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.goto(x,y)
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        if self.__size==3:
            self.shape("blueghost.gif")
        elif self.__size==2:
            self.shape("pinkghost.gif")
    #Task 1
    def getDX(self):
        return self.__dx

    def getDY(self):
        return self.__dy

    def changeDX(self, dx):
        self.__dx=dx

    def changeDY(self, dy):
        self.__dy=dy

    #Moves the ghost from its current position to a new position
    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.getDX() + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.getDY() + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    #returns the approximate "radius" of the Ghost object
    def getRadius(self):
        return self.__size * 10 - 5

class FlyingTurtle(RawTurtle):
    def __init__(self,canvasobj,dx,dy,x,y, size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.color("purple")
        self.goto(x,y)
        self.originalAngle=None
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        self.shape("turtle")

    #Task 2
    def getDX(self):
        return self.__dx

    def getDY(self):
        return self.__dy

    def changeDX(self, dx):
        self.__dx=dx

    def changeDY(self, dy):
        self.__dy=dy

    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.getDX() + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.getDY() + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    #E.C. Introduce variable "originalAngle" which is saved for every new turboBoost.
    #That angle is then used for all future turboBoosts until the turtle stops.
    #This value is also passed into laser beam class as the "direction turtle is moving"
    def turboBoost(self):
        if self.originalAngle==None:
            self.originalAngle=self.heading()
        x = math.cos(math.radians(self.originalAngle))
        y = math.sin(math.radians(self.originalAngle))
        self.changeDX(self.getDX()+x)
        self.changeDY(self.getDY()+y)

    #E.C. Reset originalAngle when turtle stops.
    def stopTurtle(self):
        self.originalAngle=None
        angle = self.heading()
        self.changeDX(0)
        self.changeDY(0)


    def getRadius(self):
        return 2

#Task 5A. Uses distance formula and approximate radius of objects to determine if the objects
#"hit"/intersect. Since radius is approximate this can cause some errors (e.g. ghost and turtle intersect, but no message is triggered)
def intersect(obj1, obj2):
    dis=math.sqrt((obj2.xcor()-obj1.xcor())**2+(obj2.ycor()-obj1.ycor())**2)
    if dis<=(obj1.getRadius()+obj2.getRadius()):
        return True
    return False

def main():

    # Start by creating a RawTurtle object for the window.
    firstwindow = tkinter.Tk()
    firstwindow.title("Turtle Saves the World!")
    canvas = ScrolledCanvas(firstwindow,600,600,600,600)
    canvas.pack(side = tkinter.LEFT)
    t = RawTurtle(canvas)

    screen = t.getscreen()
    screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
    screen.register_shape("blueghost.gif")
    screen.register_shape("pinkghost.gif")
    screen.register_shape("laser",((-2,-4),(-2,4),(2,4),(2,-4)))
    frame = tkinter.Frame(firstwindow)
    frame.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)

    #Task 6
    scoreVal=tkinter.StringVar()
    scoreVal.set("0")
    scoreTitle=tkinter.Label(frame, text='Score')
    scoreTitle.pack()
    score=tkinter.Label(frame, height=2, width=20, textvariable=scoreVal, fg="Yellow", bg='black')
    score.pack()
    livesTitle=tkinter.Label(frame, text="Extra Lives Remaining")
    livesTitle.pack()
    livesFrame=tkinter.Frame(frame, height=30,width=60,relief=tkinter.SUNKEN)
    livesFrame.pack()
    livesCanvas=ScrolledCanvas(livesFrame, 150,40, 150,40)
    livesCanvas.pack()
    livesTurtle=RawTurtle(livesCanvas)
    livesTurtle.ht()
    livesScreen=livesTurtle.getscreen()
    life1=FlyingTurtle(livesCanvas, 0,0,-35,0,0)
    life2=FlyingTurtle(livesCanvas,0,0,0,0,0)
    life3=FlyingTurtle(livesCanvas, 0,0,35,0,0)
    lives=[life1,life2,life3]
    t.ht()

    screen.tracer(10)

    #Tiny Turtle!
    flyingturtle = FlyingTurtle(canvas,0,0,(screenMaxX-screenMinX)/2+screenMinX,(screenMaxY-screenMinY)/2 + screenMinY,3)

    #Laser lists
    liveLasers=[]
    deadLasers=[]

    #A list to keep track of all the ghosts
    ghosts = []
    hiddenGhosts=[]

    #Create some ghosts and randomly place them around the screen. Added code makes sure a ghost isn't instantiated
    #in the starting position of the turtle.
    for numofghosts in range(6):
        dx = random.random()*6  - 4
        dy = random.random()*6  - 4
        x = random.random() * (screenMaxX - screenMinX) + screenMinX
        y = random.random() * (screenMaxY - screenMinY) + screenMinY
        #Added code
        if x==250:
            x=500
        elif y==250:
            y=-500

        ghost = Ghost(canvas,dx,dy,x,y,3)
        ghosts.append(ghost)

    def play():
        #start counting time for the play function
        ##LEAVE THIS AT BEGINNING OF play()
        start = datetime.datetime.now()

        #When Tiny hits ghost (Task 8)
        for each_ghost in ghosts:
            if intersect(each_ghost, flyingturtle):
                tkinter.messagebox.showinfo("Sorry", "You Lost a Life")
                each_ghost.ht()
                if flyingturtle.xcor()==0 and flyingturtle.ycor()==0:
                    each_ghost.goto(250,250)
                else:
                    each_ghost.goto(flyingturtle.xcor()*-1, flyingturtle.ycor()*-1)
                hiddenGhosts.append(each_ghost)
                ghosts.remove(each_ghost)
                lives.pop().ht()

        #Task 5. Calls intersect to determine if laser and ghost touch. Updates lists accordingly.
        for each_laser in liveLasers:
            for each_ghost in ghosts:
                if intersect(each_ghost, each_laser):
                    each_ghost.ht()
                    ghosts.remove(each_ghost)
                    liveLasers.remove(each_laser)
                    hiddenGhosts.append(each_ghost)
                    deadLasers.append(each_laser)

                    #Task 6
                    temp_score=int(scoreVal.get())+20
                    scoreVal.set(str(temp_score))

        #move all dead lasers
        for each_laser in deadLasers:
            if each_laser.xcor()!=-screenMinX*2 and each_laser.ycor()!=-screenMinY*2:
                each_laser.ht()
                each_laser.penup()
                each_laser.goto(-screenMinX*2,-screenMinY*2)


        #Task 7. If all ghosts are dead. Game over.
        if ghosts==[]:
            canvas.delete("all")
            tkinter.messagebox.showinfo("You Win!!","You saved the world!")
            return None

        #Task 8. If all lives are lost. Game over.
        elif lives==[]:
            canvas.delete("all")
            tkinter.messagebox.showinfo("You Lose!", "Haha")
            return None

        # Move the turtle
        flyingturtle.move()

        #move each laser
        for each_laser in liveLasers:
            each_laser.move()
            if each_laser.lifespan==0:
                liveLasers.remove(each_laser)
                deadLasers.append(each_laser)

        #Move the ghosts
        for each_ghost in ghosts:
            each_ghost.move()

        #stop counting time for the play function
        ##LEAVE THIS AT END OF ALL CODE IN play()
        end = datetime.datetime.now()
        duration = end - start

        millis = duration.microseconds / 1000.0

        # Set the timer to go off again
        screen.ontimer(play,int(10-millis))


    # Set the timer to go off the first time in 5 milliseconds
    screen.ontimer(play, 5)

    #Turn turtle 7 degrees to the left
    def turnLeft():
        flyingturtle.setheading(flyingturtle.heading()+7)

    #Task 3: Turn turtle 7 degrees to the right
    def turnRight():
        flyingturtle.setheading(flyingturtle.heading()-7)

    #turboBoost turtle
    def forward():
        flyingturtle.turboBoost()

    #stop Turtle
    def stop():
        flyingturtle.stopTurtle()

    #Task 4: Creates laser and adds it to liveLasers
    def fireLaser():
        laser=LaserBeam(canvas, flyingturtle.xcor(), flyingturtle.ycor(), flyingturtle.heading(), flyingturtle.originalAngle,  flyingturtle.getDX(), flyingturtle.getDY())
        liveLasers.append(laser)

    #Call functions above when pressing relevant keys
    screen.onkeypress(turnLeft,"Left")
    screen.onkeypress(turnRight, "Right")
    screen.onkeypress(forward,"Up")
    screen.onkeypress(stop, "Down")
    #Task 4
    screen.onkeypress(fireLaser, "")

    screen.listen()
    tkinter.mainloop()

if __name__ == "__main__":
    main()
