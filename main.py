import pgzrun
import random
import math
from pygame import Rect

try:
    from pgzero.actor import Actor
    from pgzero.loaders import sounds
    from pgzero.loaders import music
    from pgzero.keyboard import keyboard
    from pgzero.screen import screen 
except ImportError:
    pass
#from pgzero.actor import Actor
#from pgzero.loaders import sounds, music
#from pgzero.keyboard import Keyboard
#from pgzero.screen import Screen

WIDTH = 800
HEIGHT = 600
TITLE = "HERO ZONE: SPACE SURVIVE"

MENU = 0
PLAYING = 1
GAME_OVER = 2
WINS = 3 

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

    def update_movement(self, keyboard):
        if keyboard.left and self.actor.left > 0:
            self.actor.x -= self.speed
        if keyboard.right and self.actor.right < WIDTH:
            self.actor.x += self.speed
        if keyboard.up and self.actor.top > 0:
            self.actor.y -= self.speed
        if keyboard.down and self.actor.bottom < HEIGHT:
            self.actor.y += self.speed
        
        self.update_animation()

class Enemy(AnimatedSprite):
    def __init__(self, pos, patrol_dist=140):
        super().__init__("inimigo", 4, pos)
        self.start_x = pos[0]
        self.patrol_dist = patrol_dist
        self.direction = 1
        self.base_speed = 2 
        
    def patrol(self, extra_speed):
        current_speed = self.base_speed + extra_speed
        self.actor.x += current_speed * self.direction
        if self.actor.right >= WIDTH or self.actor.left <= 0:
            self.direction *= -1
            if self.actor.left <= 0: self.actor.left = 0
            if self.actor.right >= WIDTH: self.actor.right = WIDTH
        self.update_animation()

class EnemyType2(AnimatedSprite):
    def __init__(self, pos, patrol_dist=120):
        super().__init__("monstro", 4, pos)
        self.start_y = pos[1]
        self.patrol_dist = patrol_dist
        self.direction = 1
        self.base_speed = 2
        
    def patrol(self, extra_speed):
        current_speed = self.base_speed + extra_speed
        self.actor.y += current_speed * self.direction
        if self.actor.bottom >= HEIGHT or self.actor.top <= 0:
            self.direction *= -1
            if self.actor.top <= 0: self.actor.top = 0
            if self.actor.bottom >= HEIGHT: self.actor.bottom = HEIGHT
        self.update_animation()
class Game:
    def __init__(self):
        self.state = MENU
        self.audio_enabled = True
        self.hero = Hero((400, 300))
        self.enemies = []
        for c in range(9) : 
            enemy_x = random.randint(100, WIDTH - 100)
            enemy_y = random.randint(100, HEIGHT - 100)
            if c % 2 == 0:
                self.enemies.append(Enemy((enemy_x, enemy_y)))
            else:
                self.enemies.append(EnemyType2((enemy_x, enemy_y)))
        
        self.btn_start = Rect((WIDTH//2 - 100, 220), (200, 50))
        self.btn_audio = Rect((WIDTH//2 - 100, 300), (200, 50))
        self.btn_exit = Rect((WIDTH//2 - 100, 380), (200, 50))

        self.background_tiles = "cenario_certo"

        self.extra_speed = 0 
        self.frame_count = 0 


    def create_map(self):
        self.background_tiles = []
        for y in range(0, HEIGHT, self.tile_size):
            row = []
            for x in range(0, WIDTH, self.tile_size):
                if random.random() < 0.1:
                    title_num = 214
                else : 
                    title_num = random.randint(1, 234)
                row.append(f"cenario ({title_num})")
                #row.append(f"cenario ({random.randint(1, 234)})")
            self.background_tiles.append(row)

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        if self.audio_enabled:
            music.play("puzzle-dance-__fowksprod_.wav")
        else:
            music.stop()

    def update(self, keyboard):
        if self.state == PLAYING:
            self.frame_count += 1
            if self.frame_count % 300 == 0:
                self.extra_speed += 0.5
            if self.frame_count >= 7200 :
                self.state = WINS 
            self.hero.update_movement(keyboard)
            for enemy in self.enemies:
                enemy.patrol(self.extra_speed)
                if self.hero.actor.colliderect(enemy.actor):
                    if self.audio_enabled:
                        sounds.explosion_a.play()
                    self.state = GAME_OVER

    def draw(self, screen):
        screen.clear()
        
        screen.blit (self.background_tiles, (0, 0))

        if self.state == MENU : 
            self.draw_menu(screen)
        elif self.state == PLAYING:
            self.hero.draw()
            screen.draw.text("YOU", center=(self.hero.actor.x, self.hero.actor.y - 40), 
                             fontsize=22, 
                             color="gold",
                             shadow=(1, 1))
            for enemy in self.enemies:
                enemy.draw()
            segundos = max(0, 120 - self.frame_count // 60)
            screen.draw.text(f"TIME LEFT: {segundos}s", topleft=(10, 10), fontsize=30, color="white")
            screen.draw.text(f"SPEED LEVEL: {int(self.extra_speed)}", topright=(WIDTH - 10, 10), fontsize=30, color="white")
        elif self.state == GAME_OVER:
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=100, color="red")
            screen.draw.text("CLICK TO RESTART", center=(WIDTH//2, HEIGHT//2 + 100), fontsize=50, color="white")

        elif self.state == WINS:
            screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2), fontsize=100, color="green")
            screen.draw.text("CLICK TO RESTART", center=(WIDTH//2, HEIGHT//2 + 100), fontsize=50, color="white")
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
    current_game.update(keyboard)

def draw():
    current_game.draw(screen)

def on_mouse_down(pos):
    if current_game.state == MENU:
        if current_game.btn_start.collidepoint(pos):
            current_game.state = PLAYING
            if current_game.audio_enabled:
                music.play("puzzle-dance-__fowksprod_.wav")
        elif current_game.btn_audio.collidepoint(pos):
            current_game.toggle_audio()
        elif current_game.btn_exit.collidepoint(pos):
            exit()
    elif current_game.state == GAME_OVER or current_game.state == WINS:
        current_game.__init__()

pgzrun.go()