import pgzrun
import random
import math 
from pygame import Rect 

WIDTH = 800 
HEIGHT = 600
TITLE = " HERO ZONE "

MENU = 0 
JOGANDO = 1 
PAUSE = 2 
# Criação de classes dos bonecos

class AnimatedSprite:
    # Base ´para criação de Sprites
    def __init__(self, prefix, frame_count, pos ,animetion_speed = 0.1) : 
        self.prefix = prefix
        self.frame_count = frame_count
        self.animetion_speed = animetion_speed
        self.current_frame = 0 
        self.state = 'idle'
        self.actor= Actor(self.image, pos)
        self.flip_h = False

    def update(self) :
        self.current_frame += self.animetion_speed
        frame_index = int(self.current_frame) % self.frame_count
        self.actor.image = f"{self.prefix}_{self.state}_{frame_index}"

    def draw(self) : 
        self.draw()