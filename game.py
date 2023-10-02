import pygame
import math
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QLineEdit, QLabel
from random import randint

pygame.init()

pygame.font.SysFont('arial', 36)
sc = pygame.display.set_mode((1000, 600))
running = False
menu = True

import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Wall():
    def __init__(self, x, y, len1, len2, sdvig):
        self.x = x
        self.y = y
        self.len1 = len1
        self.len2 = len2
        self.sdvig = sdvig
        self.color = (0, 125, 255)

    def move(self):
        self.y += self.sdvig

    def draw1(self, sc):
        pygame.draw.rect(sc, (128, 0, 128), (0, 0, 12, 600))
        pygame.draw.rect(sc, (128, 0, 128), (988, 0, 12, 600))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.len1, self.len2))


class Ball():
    def __init__(self, x, y, rad, sdvigx, sdvigy, image):

        self.ball = pygame.sprite.Sprite()
        self.ball.image = image
        self.ball.rect = self.ball.image.get_rect()

        self.x = x
        self.y = y
        self.rad = rad
        self.sdvigx = sdvigx
        self.sdvigy = sdvigy
        self.x1 = 0
        self.x2 = 0
        self.color = (255, 0, 0)

    def move(self, pl1, pl2):
        self.x = self.x + self.sdvigx
        self.ball.rect.x = self.x
        self.ball.rect.y = self.y

        self.y = self.y + self.sdvigy
        if (self.x + self.rad >= 1000) or (self.x + self.rad <= 0):
            self.sdvigx *= -1
        if (self.y + self.rad >= 600) or (self.y + self.rad <= 0):
            self.sdvigy *= -1
        if (self.x - 5 <= pl1.x + 25 and self.y >= pl1.y and self.y < pl1.y + 200):
            self.sdvigx *= -1
        if (self.x + 5 >= pl2.x and self.y >= pl2.y and self.y <= pl2.y + 200):
            self.sdvigx *= -1
        if self.x <= 10:
            self.x2 += 1
            self.x = 500
            self.y = 300
        if self.x >= 990:
            self.x1 += 1
            self.x = 500
            self.y = 30

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)


sprites1 = pygame.sprite.Group()

field = pygame.sprite.Sprite()
field.image = pygame.transform.scale(load_image("fon.png"), (1000, 600))
field.rect = field.image.get_rect()
field.rect.x = 0
field.rect.y = 0
sprites1.add(field)

pygame.mouse.set_visible(0)

cursor1 = load_image("c.png", -1)
cursor1 = pygame.transform.scale(cursor1, (22, 22))
cursor = pygame.sprite.Sprite()
cursor.image = cursor1
cursor.rect = cursor.image.get_rect()
sprites1.add(cursor)
font1 = pygame.font.Font(None, 40)
sc.fill((0, 0, 0))

theme = 0

while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (pygame.mouse.get_pos()[0] > 100 and pygame.mouse.get_pos()[0] < 300):
                    if (pygame.mouse.get_pos()[1] > 350 and pygame.mouse.get_pos()[1] < 400):
                        theme += 1
                        menu = False
                        running = True
                if (pygame.mouse.get_pos()[0] > 700 and pygame.mouse.get_pos()[0] < 900):
                    if (pygame.mouse.get_pos()[1] > 350 and pygame.mouse.get_pos()[1] < 400):
                        theme += 2
                        menu = False
                        running = True
    sc.fill((0, 0, 0))

    if pygame.mouse.get_focused() == True:
        cursor.rect.x = pygame.mouse.get_pos()[0]
        cursor.rect.y = pygame.mouse.get_pos()[1]
    sprites1.draw(sc)

    pygame.draw.rect(sc, (0, 255, 0), (700, 900, 200, 50))
    pygame.draw.rect(sc, (0, 255, 0), (100, 350, 200, 50))
    text = font1.render("Футбол", 1, (255, 255, 255))
    place = text.get_rect(center=(200, 375))
    sc.blit(text, place)
    pygame.display.flip()
    pygame.time.delay(40)

clock = pygame.time.Clock()

sprites = pygame.sprite.Group()

b = []
player1 = Wall(0, 80, 25, 200, 0)
player2 = Wall(975, 80, 25, 200, 0)

if (theme == 1):
    field = pygame.sprite.Sprite()
    field.image = pygame.transform.scale(load_image("f1.png"), (1000, 600))
    field.rect = field.image.get_rect()
    field.rect.x = 0
    field.rect.y = 0
    sprites.add(field)
    pygame.mixer.music.load('m1.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)
else:
    field = pygame.sprite.Sprite()
    field.image = pygame.transform.scale(load_image("f2.png"), (1000, 600))
    field.rect = field.image.get_rect()
    field.rect.x = 0
    field.rect.y = 0
    sprites.add(field)
    pygame.mixer.music.load('m2.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)

cursor1 = load_image("c.png", -1)
cursor1 = pygame.transform.scale(cursor1, (22, 22))
cursor = pygame.sprite.Sprite()
cursor.image = cursor1
cursor.rect = cursor.image.get_rect()
sprites.add(cursor)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (theme == 1):
                    ball1 = load_image("b1.png", -1)
                else:
                    ball1 = load_image("b2.png", -1)
                ball1 = pygame.transform.scale(ball1, (30, 30))
                b.append(Ball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, -30, -30, ball1))
                sprites.add(b[-1].ball)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if player2.y > 10:
                    player2.sdvig = -30
                    player2.move()
            if event.key == pygame.K_DOWN:
                if player2.y < 390:
                    player2.sdvig = 30
                    player2.move()
            if event.key == pygame.K_w:
                if player1.y > 10:
                    player1.sdvig = -30
                    player1.move()
            if event.key == pygame.K_s:
                if player1.y < 390:
                    player1.sdvig = 30
                    player1.move()
    sc.fill((0, 0, 0))

    if pygame.key.get_pressed()[pygame.K_UP]:
        if player2.y > 10:
            player2.sdvig = -30
            player2.move()
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if player2.y < 390:
            player2.sdvig = 30
            player2.move()
    if pygame.key.get_pressed()[pygame.K_w]:
        if player1.y > 10:
            player1.sdvig = -30
            player1.move()
    if pygame.key.get_pressed()[pygame.K_s]:
        if player1.y < 390:
            player1.sdvig = 30
            player1.move()

    if pygame.mouse.get_focused() == True:
        cursor.rect.x = pygame.mouse.get_pos()[0]
        cursor.rect.y = pygame.mouse.get_pos()[1]

    sprites.draw(sc)

    player1.draw1(sc)
    for i in b:
        # i.draw(sc)
        i.move(player1, player2)
        player1.draw(sc)
        player2.draw(sc)
        font = pygame.font.Font(None, 40)
        text = font.render(str(b[0].x1) + " : " + str(b[0].x2), 1, (255, 0, 0))
        place = text.get_rect(center=(500, 30))
        sc.blit(text, place)
    if len(b) != 0 and (b[0].x1 > 7 or b[0].x2 > 7):
        if b[0].x1 > b[0].x2:
            text = font.render("Игрок слева победил", 1, (255, 0, 0))
            place = text.get_rect(center=(500, 300))
            sc.blit(text, place)
        else:
            text = font.render("Игрок справа победил", 1, (255, 0, 0))
            place = text.get_rect(center=(500, 300))
            sc.blit(text, place)
        f = open('lastgames.txt', 'r')
        lines = []
        for line in f:
            lines.append(line)
        print(lines)
        f.close()
        f = open('lastgames.txt', 'w')
        f.close()
        text1 = font.render(lines[0], 1, (255, 0, 0))
        place = text.get_rect(center=(630, 400))
        sc.blit(text1, place)
        text1 = font.render(lines[1], 1, (255, 0, 0))
        place = text.get_rect(center=(630, 440))
        sc.blit(text1, place)
        text1 = font.render(lines[2], 1, (255, 0, 0))
        place = text.get_rect(center=(630, 480))
        sc.blit(text1, place)
        text1 = font.render(lines[3], 1, (255, 0, 0))
        place = text.get_rect(center=(630, 520))
        sc.blit(text1, place)
        text1 = font.render(lines[4], 1, (255, 0, 0))
        place = text.get_rect(center=(630, 560))
        sc.blit(text1, place)
        lines[4] = lines[3]
        lines[3] = lines[2]
        lines[2] = lines[1]
        lines[1] = lines[0]
        lines[0] = ""
        lines[0] = str(b[0].x1) + " : " + str(b[0].x2)
        f = open('lastgames.txt', 'w')
        f.write(lines[0] + "\n")
        f.write(lines[1])
        f.write(lines[2])
        f.write(lines[3])
        f.write(lines[4])
        f.close()
        pygame.display.flip()
        pygame.time.delay(5000)
        b = []

    pygame.display.flip()
    pygame.time.delay(40)
