import pgzrun
import random
import math
from pygame import Rect

try:
    from pgzero.actor import Actor
    from pgzero.loaders import sounds
    from pgzero.loaders import music
    from pgzero.keyboard import Keyboard
    from pgzero.screen import Screen
except ImportError:
    pass
#from pgzero.actor import Actor
#from pgzero.loaders import sounds, music
#from pgzero.keyboard import Keyboard
#from pgzero.screen import Screen

WIDTH = 800
HEIGHT = 600
TITLE = "HERO ZONE: DESERT ADVENTURE"

MENU = 0
PLAYING = 1
GAME_OVER = 2

class AnimatedSprite:
    def __init__(self, prefix, frame_count, pos, animation_speed=0.1):
        self.prefix = prefix
        self.frame_count = frame_count
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.actor = Actor(f"{self.prefix}1", pos)

    def update_animation(self):
        self.current_frame += self.animation_speed
        frame_index = (int(self.current_frame) % self.frame_count) + 1
        self.actor.image = f"{self.prefix}{frame_index}"

    def draw(self):
        self.actor.draw()

class Hero(AnimatedSprite):
    def __init__(self, pos):
        super().__init__("herromoviment", 4, pos)
        self.speed = 4

    def update_movement(self, Keyboard):
        if Keyboard.left and self.actor.left > 0:
            self.actor.x -= self.speed
        if Keyboard.right and self.actor.right < WIDTH:
            self.actor.x += self.speed
        if Keyboard.up and self.actor.top > 0:
            self.actor.y -= self.speed
        if Keyboard.down and self.actor.bottom < HEIGHT:
            self.actor.y += self.speed
        
        self.update_animation()

class Enemy(AnimatedSprite):
    def __init__(self, pos, patrol_dist=140):
        super().__init__("inimigo", 4, pos)
        self.start_x = pos[0]
        self.patrol_dist = patrol_dist
        self.direction = 1
        self.speed = 2

    def patrol(self):
        self.actor.x += self.speed * self.direction
        if abs(self.actor.x - self.start_x) >= self.patrol_dist:
            self.direction *= -1
        self.update_animation()

class Game:
    def __init__(self):
        self.state = MENU
        self.audio_enabled = True
        self.hero = Hero((400, 300))
        self.enemies = [Enemy((200, 150)), Enemy((600, 450))]
        
        self.btn_start = Rect((WIDTH//2 - 100, 220), (200, 50))
        self.btn_audio = Rect((WIDTH//2 - 100, 300), (200, 50))
        self.btn_exit = Rect((WIDTH//2 - 100, 380), (200, 50))

        self.tile_size = 64
        self.background_tiles = []
        self.create_map()

    def create_map(self):
        self.background_tiles = []
        for y in range(0, HEIGHT, self.tile_size):
            row = []
            for x in range(0, WIDTH, self.tile_size):
                row.append(f"cenario ({random.randint(214, 225)})")
            self.background_tiles.append(row)

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        if self.audio_enabled:
            music.play("puzzle-dance_-_fowksprod_wav")
        else:
            music.stop()

    def update(self, Keyboard):
        if self.state == PLAYING:
            self.hero.update_movement(Keyboard)
            for enemy in self.enemies:
                enemy.patrol()
                if self.hero.actor.colliderect(enemy.actor):
                    if self.audio_enabled:
                        sounds.explosion_a.play()
                    self.state = GAME_OVER

    def draw(self, screen):
        screen.clear()
        
        for r_idx, row in enumerate(self.background_tiles):
            for c_idx, tile in enumerate(row):
                screen.blit(tile, (c_idx * self.tile_size, r_idx * self.tile_size))

        if self.state == MENU:
            self.draw_menu(screen)
        elif self.state == PLAYING:
            self.hero.draw()
            for enemy in self.enemies:
                enemy.draw()
        elif self.state == GAME_OVER:
            screen.draw.text("GAME OVER", center=(WIDTH//2, 250), fontsize=80, color='red')
            screen.draw.text("Click to Return Menu", center=(WIDTH//2, 350), fontsize=40, color='white')

    def draw_menu(self, screen):
        screen.draw.text("HERO ZONE", center=(WIDTH//2, 120), fontsize=100, color="gold")
        
        screen.draw.filled_rect(self.btn_start, "darkgreen")
        screen.draw.text("START GAME", center=self.btn_start.center, fontsize=30, color="white")
        
        screen.draw.filled_rect(self.btn_audio, "navy")
        audio_label = "AUDIO: ON" if self.audio_enabled else "AUDIO: OFF"
        screen.draw.text(audio_label, center=self.btn_audio.center, fontsize=30, color="white")
        
        screen.draw.filled_rect(self.btn_exit, "darkred")
        screen.draw.text("EXIT", center=self.btn_exit.center, fontsize=30, color="white")

current_game = Game()

def update():
    current_game.update(Keyboard)

def draw():
    current_game.draw(Screen)

def on_mouse_down(pos):
    if current_game.state == MENU:
        if current_game.btn_start.collidepoint(pos):
            current_game.state = PLAYING
            if current_game.audio_enabled:
                music.play("puzzle-dance_-_fowksprod_wav")
        elif current_game.btn_audio.collidepoint(pos):
            current_game.toggle_audio()
        elif current_game.btn_exit.collidepoint(pos):
            exit()
    elif current_game.state == GAME_OVER:
        current_game.__init__()

pgzrun.go()