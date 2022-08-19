# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# attempted genetic mutations in a neural network simulation, displayed with turtle
import math, os, random, turtle

# initialize window
game = turtle.Screen()
game.colormode(255)
game.listen()
game.title("Cat & Mouse")
game.bgcolor("black")
game.setup(width=2000, height=1200)
game.tracer(0)

loop = True  # used to allow player to control the mouse
p2 = True  # used to start a fresh state for the AI


def invertLoop():
    global loop
    loop = not loop


def invertP2():
    global p2
    p2 = not p2


def randX():
    width = game.window_width() / 2  # origin is in the center, half the width is the distance to the screen edges
    return (
                   2 * random.random() - 1) * width  # returns a value between width and -width, which translates to an x coordinate


def randY():
    height = game.window_height() / 2  # origin is in the center, half the height is the distance to the screen ceiling and floor
    return (
                   2 * random.random() - 1) * height  # returns a value between height and -height, which translates to an y coordinate


def retRand(n):  # returns an array of n random numbers (used to generate weights for brain class)
    i = 0
    rands = []
    while n > i:
        rands.append(randSign() * random.random())
        i += 1
    return rands


def randNum():  # a number between -5 and 5
    return 10 * (random.random() * 2 - 1)


def randSign():  # either -1 or 1
    i = random.random()
    if i > .5:
        return 1
    else:
        return -1


def pick(n, m):  # randomly returns either of the inputs
    i = randSign()
    if i > 0:
        return n
    return m


def confine(num, c):
    # number is constrained to values c, 0, and -c
    if num > c:
        num = c
    elif num < -c:
        num = -c
    else:
        num = 0
    return num


def condense(num, c):
    # number is constrained to values between c and -c
    if num > c:
        num = c
    elif num < -c:
        num = -c
    return num


def sigmoid(num):
    e = math.e
    newNum = (pow(e, num) - pow(e, -num)) / (pow(e, num) + pow(e, -num))
    return newNum


def inBorders(coords):
    pair = [coords[0], coords[1]]
    if pair[0] > game.window_width() / 2 - 15:
        pair[0] = game.window_width() / 2 - 15
    if pair[0] < -game.window_width() / 2 + 7:
        pair[0] = -game.window_width() / 2 + 7
    if pair[1] > game.window_height() / 2 - 7:
        pair[1] = game.window_height() / 2 - 7
    if pair[1] < -game.window_height() / 2 + 15:
        pair[1] = -game.window_height() / 2 + 15
    return pair


def respawn(food, mouse, cat, human):  # respawn in space with distance from other objects (inputs are coordinate pairs)
    resDis = 25000  # the squared radius distance for a safe respawn
    while True:  # find an xy that satisfies the respawn distance
        x = randX()
        y = randY()
        if ((food[0] - x) ** 2) + ((food[1] - y) ** 2) >= resDis:
            if ((mouse[0] - x) ** 2) + ((mouse[1] - y) ** 2) >= resDis:
                if ((cat[0] - x) ** 2) + ((cat[1] - y) ** 2) >= resDis:
                    if ((human[0] - x) ** 2) + ((human[1] - y) ** 2) >= resDis:
                        return inBorders([x, y])


class Food:
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]
        self.me = turtle.Turtle()
        self.me.turtlesize(.5, .5, 1)
        self.me.speed(0)
        self.me.shape('square')
        self.me.color("orange", "yellow")
        self.me.penup()
        self.me.goto(self.x, self.y)

    def move(self, xy):
        self.x = xy[0]
        self.y = xy[1]
        self.me.goto(self.x, self.y)

    def consumed(self):
        xy = respawn([self.x, self.y], [self.x, self.y], [self.x, self.y], [self.x, self.y])
        self.x = xy[0]
        self.y = xy[1]
        self.move([self.x, self.y])


class Mouse:
    speed = 10

    def __init__(self, xy, color):
        self.score = 0
        self.gen = 0
        self.x = xy[0]
        self.y = xy[1]
        self.color = color
        self.me = turtle.Turtle()
        self.me.turtlesize(.75, .75, 1)
        self.me.speed(0)
        self.me.tilt(-90)
        self.me.shape('triangle')
        self.me.color("grey", color)
        self.me.penup()
        self.me.goto(self.x, self.y)  # always use self x and y to move
        self.brain = Brain()

        self.scoreTurtle = turtle.Turtle()
        self.scoreTurtle.speed(0)
        self.scoreTurtle.goto(self.x, self.y)
        self.scoreTurtle.color("White", "black")
        self.scoreTurtle.penup()
        self.scoreTurtle.hideturtle()
        self.scoreTurtle.clear()
        self.scoreTurtle.write(self.gen.__str__())

    def move(self, xy):  # xy should be [x,y] 1,0, or -1
        self.x = self.x + self.speed * xy[0]
        self.y = self.y + self.speed * xy[1]
        check = inBorders([self.x, self.y])
        self.x = check[0]
        self.y = check[1]
        self.me.goto(self.x, self.y)

        self.scoreTurtle.goto(self.x, self.y)
        self.scoreTurtle.clear()
        self.scoreTurtle.write(self.gen.__str__())

    def moveUp(self):
        self.move([0, 1])

    def moveDown(self):
        self.move([0, -1])

    def moveLeft(self):
        self.move([-1, 0])

    def moveRight(self):
        self.move([1, 0])

    def moveRUp(self):
        self.move([1, 1])

    def moveLUp(self):
        self.move([-1, 1])

    def moveRDown(self):
        self.move([1, -1])

    def moveLDown(self):
        self.move([-1, -1])

    def eat(self, food):
        if food.x + 15 > self.x > food.x - 15:
            if food.y + 15 > self.y > food.y - 15:
                self.score += 1
                food.consumed()

    def consumed(self, food, human):
        xy = respawn([food.x, food.y], [self.x, self.y], [self.x, self.y], [human.x, human.y])
        self.x = xy[0]
        self.y = xy[1]
        self.gen += 1
        self.me.goto(self.x, self.y)


class Cat:
    speed = 1

    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]
        self.knows = [self.x + randNum(), self.y + randNum()]
        self.sees = False

        self.sight = turtle.Turtle()
        self.sight.speed(0)
        self.sight.color("red")
        self.sight.shape('circle')
        self.sight.turtlesize(10, 10, 1)
        self.sight.penup()
        self.sight.goto(self.x, self.y)

        self.me = turtle.Turtle()
        self.me.speed(0)
        self.me.shape('circle')
        self.me.penup()
        self.me.goto(self.x, self.y)
        self.me.color("white", "orange")

    def Sight(self, mice):
        self.sight.color("grey")
        self.sees = False
        for mouse in mice:
            if ((mouse.x - self.x) ** 2) + ((mouse.y - self.y) ** 2) <= 10000:
                self.sight.color("red")
                self.knows = [mouse.x, mouse.y]
                self.sees = True

    def direct(self):
        pair = [0, 0]
        if self.x > self.knows[0] - 5:
            pair[0] = -1
        if self.x < self.knows[0] + 5:
            pair[0] = 1
        if self.knows[0] + 5 > self.x > self.knows[0] - 5:
            pair[0] = 0
        if self.y > self.knows[1] - 5:
            pair[1] = -1
        if self.y < self.knows[1] + 5:
            pair[1] = 1
        if self.knows[1] + 5 > self.y > self.knows[1] - 5:
            pair[1] = 0
        if pair == [0, 0] and not self.sees:
            self.knows = [randX(), randY()]
        return pair

    def move(self, numXY):
        self.x = self.x + self.speed * numXY[0]
        self.y = self.y + self.speed * numXY[1]
        check = inBorders([self.x, self.y])
        self.x = check[0]
        self.y = check[1]
        self.me.goto(self.x, self.y)
        self.sight.goto(self.x, self.y)

    def eat(self, mouse, food, human):
        if mouse.x + 7 > self.x > mouse.x - 7:
            if mouse.y + 7 > self.y > mouse.y - 7:
                mouse.consumed(food, human)
                return True
        return False


class Human:
    speed = 1

    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]
        self.knows = [self.x + randNum(), self.y + randNum()]
        self.sees = False

        self.sight = turtle.Turtle()
        self.sight.speed(0)
        self.sight.color("red")
        self.sight.shape('circle')
        self.sight.turtlesize(40, 40, 1)
        self.sight.penup()
        self.sight.goto(self.x, self.y)

        self.me = turtle.Turtle()
        self.me.speed(0)
        self.me.shape('circle')
        self.me.color("white", "black")
        self.sight.turtlesize(15, 15, 1)
        self.me.penup()
        self.me.goto(self.x, self.y)

    def Sight(self, mice, cat):
        self.sight.color("grey")
        self.sees = False
        for mouse in mice:
            if ((mouse.x - self.x) ** 2) + ((mouse.y - self.y) ** 2) <= 23000:
                self.sight.color("red")
                self.knows = [mouse.x, mouse.y]
                self.sees = True
                cat.knows = [mouse.x, mouse.y]  # alert the cat of mouse position

    def seek(self):
        width = game.window_width() / 2 - 100
        height = game.window_height() / 2 - 100
        return [randSign() * width, randSign() * height]

    def direct(self):
        pair = [0, 0]
        if self.x > self.knows[0] - 5:
            pair[0] = -1
        if self.x < self.knows[0] + 5:
            pair[0] = 1
        if self.knows[0] + 5 > self.x > self.knows[0] - 5:
            pair[0] = 0
        if self.y > self.knows[1] - 5:
            pair[1] = -1
        if self.y < self.knows[1] + 5:
            pair[1] = 1
        if self.knows[1] + 5 > self.y > self.knows[1] - 5:
            pair[1] = 0
        if self.sees:
            pair = [0, 0]
        if pair == [0, 0]:
            self.knows = self.seek()
        return pair

    def move(self, xy):
        if not self.sees:
            self.x = self.x + self.speed * xy[0]
            self.y = self.y + self.speed * xy[1]
            check = inBorders([self.x, self.y])
            self.x = check[0]
            self.y = check[1]
            self.me.goto(self.x, self.y)
            self.sight.goto(self.x, self.y)


class Brain:  # intelligence designed for the mouse
    def __init__(self):
        self.layer1 = retRand(6)
        self.layer2 = retRand(4)
        self.bias = 1
        self.score = 0

    def activate(self, x1, y1, x2, y2, x3,
                 y3):  # xy1 should be mouse xy, xy2 should be food, xy3 should be cat, and xy4 should be person
        foodX = (condense((x2 - x1), 5))  # x distance from mouse and food
        foodY = (condense((y2 - y1), 5))  # y distance from mouse and food
        catX = (condense((x3 - x1), 5))  # x distance from mouse and cat
        catY = (condense((y3 - y1), 5))  # y distance from mouse and cat
        xz = foodX * self.layer1[0] + catX * self.layer1[1] + self.bias * self.layer1[2]
        yz = foodY * self.layer1[3] + catY * self.layer1[4] + self.bias * self.layer1[5]
        x = xz * self.layer2[0] + self.bias * self.layer2[1]
        y = yz * self.layer2[2] + self.bias * self.layer2[3]
        x = sigmoid(x)
        y = sigmoid(y)
        xy = [x, y]
        return xy

    def setLayer1(self, weights):  # floating point numbers in array
        self.layer1 = weights

    def setLayer2(self, weights):  # floating point numbers in array
        self.layer2 = weights

    def setScore(self, num):  # set score, integer value
        self.score = num

    def merge(self, b1, b2):  # brain becomes a child of the two input brains (its weights are randomly merged)
        i = 0
        while i < self.layer1.__len__():
            self.layer1[i] = pick(b1.layer1[i], b2.layer1[i])
            i += 1
        i = 0
        while i < self.layer2.__len__():
            self.layer2[i] = pick(b1.layer2[i], b2.layer2[i])
            i += 1


# player loop
joe = Human([200, 200])
gato = Cat([-500, 0])
brie = Mouse([0, 0], "pink")
cheese = Food([100, 0])
mice = [brie]
pride = [gato]

scoreTurtle = turtle.Turtle()
scoreTurtle.speed(0)
scoreTurtle.goto(0, 550)
scoreTurtle.color("White", "black")
scoreTurtle.penup()
scoreTurtle.hideturtle()

framer = 0

while loop:
    game.update()
    scoreTurtle.clear()
    scoreTurtle.write("Score: " + brie.score.__str__())
    game.onkeypress(brie.moveLeft, "a")
    game.onkeypress(brie.moveRight, "d")
    game.onkeypress(brie.moveUp, "w")
    game.onkeypress(brie.moveDown, "x")
    game.onkeypress(brie.moveLUp, "q")
    game.onkeypress(brie.moveRUp, "e")
    game.onkeypress(brie.moveLDown, "z")
    game.onkeypress(brie.moveRDown, "c")

    framer = framer % 2

    brie.eat(cheese)

    joe.Sight(mice, gato)
    gato.Sight(mice)
    gato.eat(brie, cheese, joe)
    if framer == 0:
        joe.move(joe.direct())
        gato.move(gato.direct())

    framer += 1

    game.onkeypress(invertLoop, "p")

#  AI loop
joe.move([200, 200])
gato.move([-1000, 0])
brie.move([0, 0])
brie.score = 0

# pride.append(Cat([-500, 0]))  # divide mice to cat?

# mice of many designer colors
mice.append(Mouse([0, 0], "light blue"))
mice.append(Mouse([0, 0], "red"))
mice.append(Mouse([0, 0], "blue"))
mice.append(Mouse([0, 0], "white"))
mice.append(Mouse([0, 0], "green"))
mice.append(Mouse([0, 0], "purple"))
mice.append(Mouse([0, 0], "magenta"))
mice.append(Mouse([0, 0], "light green"))
mice.append(Mouse([0, 0], "orange"))

# r = 0  # generate 255/z greyscale mice
# z = 16
# while r < 256:
#    mice.append(Mouse([0, 0], (r, r, r)))
#    r += z


cheese.move([100, 0])
scoreTurtle.clear()


def bScore(brain):
    return brain.score


framer = 0

pool = [Brain()]

while p2:
    game.update()
    framer = framer % 2

    joe.Sight(mice, gato)
    for cat in pride:  # In case of more cats
        cat.Sight(mice)
        for mouse in mice:  # each cat handles each mouse.
            mouse.eat(cheese)  # assume one food
            if cat.eat(mouse, cheese, joe):  # if the cat eats the mouse
                if mouse.score > mouse.brain.score:
                    mouse.brain.setScore(mouse.score)
                    pool.append(mouse.brain)
                    pool.sort(key=bScore, reverse=True)  # sort highest scores to slots 0 and 1
                    scoreTurtle.clear()
                    scoreTurtle.write("Highest Scores: " + pool[0].score.__str__())
                mouse.score = 0
                if pool[0].score > 2:
                    if randSign() > 0:
                        rand = randSign() + randSign() + randSign()
                        if rand > 2:
                            mouse.brain.merge(pool[0], pool[1])
                        elif rand > 1:
                            mouse.brain.merge(mouse.brain, pool[0])
                        elif rand > 0:
                            mouse.brain.merge(mouse.brain, pool[1])
                        elif rand > -1:
                            mouse.brain.merge(mouse.brain, Brain())
                        elif rand > -2:
                            mouse.brain = Brain()
                        else:
                            mouse.brain.merge(pool[0], pool[0])
                else:
                    mouse.brain.merge(mouse.brain, Brain())  # random modification of current brain
            if framer == 0:
                xy = mouse.brain.activate(mouse.x, mouse.y, cheese.x, cheese.y, cat.x, cat.y)
                mouse.move(xy)
                joe.move(joe.direct())
                cat.move(cat.direct())

    framer += 1

    game.onkeypress(invertP2, "o")