# Coding a game using the turtle module.
import sys

import pygame
import turtle
import random
import _tkinter
import os
from playsound import playsound

# screen generation
wn = turtle.Screen()
wn.setup(1000, 800)
wn.title("Space Star Galactica")
wn.bgcolor("black")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.penup()
pen.color("white")
pen.hideturtle()
turtle1 = turtle.Turtle()
turtle1.color('deep pink')
style = ('Courier', 15, 'italic')
turtle1.penup()
turtle1.hideturtle()
turtle1.goto(100, -350)
turtle1.write('W (UP) A (LEFT) S (DOWN) D (RIGHT) Q (Stop)', False, font=style, align='center')

pygame.init()
shot_sound = pygame.mixer.Sound("blaster.mp3")
explosion_sound = pygame.mixer.Sound("explosion.wav")


# player generation
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.life = 3
        self.color("white")
        self.penup()
        self.goto(-400, 0)
        self.shape("triangle")
        self.speed(0)
        self.dy = 0
        self.dx = 0

    def up(self):
        self.dy = 1

    def down(self):
        self.dy = -1

    def left(self):
        self.dx = -1

    def right(self):
        self.dx = 1

    def stop(self):
        self.dy = 0
        self.dx = 0

    def died(self):
        self.life -= 1
        print("died")

    def move(self):
        self.sety(self.ycor() + self.dy)
        self.setx(self.xcor() + self.dx)

        if self.ycor() > 390:
            self.sety(390)
            self.dy = 0
        elif self.ycor() < -380:
            self.sety(-380)
            self.dy = 0

        if self.xcor() < -390:
            self.setx(-390)
            self.dx = 0

        elif self.xcor() > -290:
            self.setx(-290)
            self.dx = 0


class Bullet(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("lightblue")
        self.penup()
        self.shape("circle")
        self.shapesize(0.3, 0.3, 0)
        self.speed(0)
        self.goto(2000, 0)
        self.dx = 0

    def fire(self):
        self.goto(player.xcor(), player.ycor())
        self.dx = 3
        pygame.mixer.Sound.play(shot_sound)
        pygame.mixer.music.stop()

    def move(self):
        self.setx(self.xcor() + self.dx)


class Enemy(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        colors = ["yellow", "blue", "white", "gray", "pink"]
        self.color(random.choice(colors))
        self.penup()
        self.goto(random.randint(400, wn.window_width() / 2), random.randint(-370, 370))
        self.shape("square")
        self.speed(0)
        self.dx = -0.5

    def move(self):
        if self.dx > 3:
            self.dx = 3
        self.setx(self.xcor() + self.dx)

        if self.xcor() < -500:
            self.goto(wn.window_width() / 2, random.randint(-380, 380))
            if self.dx <= 3:
                self.dx *= 1.1


# create game Objects as turtles
player = Player()
bullet = Bullet()

# Enemy list
enemies = []

for _ in range(3):
    enemies.append(Enemy())


def start_game():
    global game_state
    game_state = 2


def restart():
    enemy.setx(random.randint(400, wn.window_width() / 2))
    enemy.sety(random.randint(-370, 370))
    print("tried")


def quit():
    sys.exit()
    print("tried")


wn.listen()
wn.onkey(quit, "k")
wn.onkey(restart, "l")
wn.onkey(player.up, "w")
wn.onkey(player.down, "s")
wn.onkey(player.stop, "q")
wn.onkey(player.left, "a")
wn.onkey(player.right, "d")
wn.onkey(bullet.fire, "space")

# game loop
while True:
    wn.update()
    player.move()
    bullet.move()

    for enemy in enemies:
        enemy.move()

        if enemy.distance(bullet) < 13:
            enemy.goto(wn.window_width() / 2, random.randint(-400, 400))
            bullet.dx = 0
            bullet.goto(0, wn.window_height())
            pygame.mixer.Sound.play(explosion_sound)
            pygame.mixer.music.stop()

        if enemy.distance(player) < 20:
            player.died()
            print("You died!")
            exit()
