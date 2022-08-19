import os, random, turtle

# neural network attempts to chose 1/9 responses which best matches the input clicks position relative to the center of the screen, displayed with turtle

# initialize window
game = turtle.Screen()
game.listen()
game.title("Making AI")
game.bgcolor("black")
game.setup(width=2000, height=1200)
game.tracer(0)

loop = True


def invertLoop():
    global loop
    loop = not loop


def randlist(n):
    li = []
    i = 0
    while i < n:
        li.append(random.random())
        i += 1
    return li


def constrain(num, c):
    if num > c:
        num = c
    elif num < -c:
        num = -c
    else:
        num = 0
    return num


class Brain:
    def __init__(self):
        self.nodes = randlist(4)
        self.me = turtle.Turtle()
        self.me.speed(0)
        self.me.shape('square')
        self.me.color("white")
        self.me.penup()
        self.me.goto(0, 0)

        # brief training
        i = 0
        lr = .015
        while i < 10000:
            i += 1
            test = self.activate(50, 0)
            if test[0] != 100:
                self.nodes[0] += lr
            if test[1] != 0:
                if test[1] > 0:
                    self.nodes[2] -= lr
                else:
                    self.nodes[2] += lr

            test = self.activate(-50, 0)
            if test[0] != -100:
                self.nodes[0] += lr
            if test[1] != 0:
                if test[1] > 0:
                    self.nodes[2] -= lr
                else:
                    self.nodes[2] += lr

            test = self.activate(0, 50)
            if test[1] != 100:
                self.nodes[3] += lr
            if test[0] != 0:
                if test[0] > 0:
                    self.nodes[1] -= lr
                else:
                    self.nodes[1] += lr

            test = self.activate(0, -50)
            if test[1] != -100:
                self.nodes[3] += lr
            if test[0] != 0:
                if test[0] > 0:
                    self.nodes[1] -= lr
                else:
                    self.nodes[1] += lr

        print(self.nodes)

    def move(self, xy):
        self.me.goto(xy[0], xy[1])

    def activate(self, x, y):
        movX = x * self.nodes[0] + y * self.nodes[1]
        movY = x * self.nodes[2] + y * self.nodes[3]
        movX = constrain(movX, 100)
        movY = constrain(movY, 100)
        xy = [movX, movY]
        self.move(xy)
        return xy


class Grid:
    def __init__(self, color):
        self.n1 = turtle.Turtle()
        self.n1.speed(0)
        self.n1.shape('square')
        self.n1.color(color)
        self.n1.penup()
        self.n1.goto(0, 0)

        self.n2 = turtle.Turtle()
        self.n2.speed(0)
        self.n2.shape('square')
        self.n2.color(color)
        self.n2.penup()
        self.n2.goto(100, 0)

        self.n3 = turtle.Turtle()
        self.n3.speed(0)
        self.n3.shape('square')
        self.n3.color(color)
        self.n3.penup()
        self.n3.goto(-100, 0)

        self.n4 = turtle.Turtle()
        self.n4.speed(0)
        self.n4.shape('square')
        self.n4.color(color)
        self.n4.penup()
        self.n4.goto(0, 100)

        self.n5 = turtle.Turtle()
        self.n5.speed(0)
        self.n5.shape('square')
        self.n5.color(color)
        self.n5.penup()
        self.n5.goto(0, -100)

        self.n6 = turtle.Turtle()
        self.n6.speed(0)
        self.n6.shape('square')
        self.n6.color(color)
        self.n6.penup()
        self.n6.goto(100, 100)

        self.n7 = turtle.Turtle()
        self.n7.speed(0)
        self.n7.shape('square')
        self.n7.color(color)
        self.n7.penup()
        self.n7.goto(100, -100)

        self.n8 = turtle.Turtle()
        self.n8.speed(0)
        self.n8.shape('square')
        self.n8.color(color)
        self.n8.penup()
        self.n8.goto(-100, 100)

        self.n9 = turtle.Turtle()
        self.n9.speed(0)
        self.n9.shape('square')
        self.n9.color(color)
        self.n9.penup()
        self.n9.goto(-100, -100)


gru = Grid("red")
ego = Brain()

while loop:
    game.update()
    game.onclick(ego.activate)
    game.onkeypress(invertLoop, "p")
