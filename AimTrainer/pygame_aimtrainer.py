"""
Desktop version of the aim trainer. Some enhanced features.

~MELBO
"""

import pygame
import pygame.gfxdraw
import random
import time
from math import sqrt

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Classes and functions
class Game:
    def __init__(self, circle_count: int):
        self.round_time = 20
        self.hit_counter = 0
        self.start_time = time.time()
        self.wavetimes = []
        self.circle_count = circle_count
        self.wave = Wave(circle_count)

    def shoot(self):
        # Handles shooting
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for circle in self.wave.circles:
            if sqrt((circle.x - mouse_x)**2 + (circle.y - mouse_y)**2) < circle.r:
                self.wave.circles.remove(circle)
                shot_sound.stop() # Stop previously playing sound
                shot_sound.play() # Play sound
                self.hit_counter += 1
                break
    
    def draw(self):
        # Draws wave circles
        for circle in self.wave.circles:
            circle.draw()

        # Draw timer
        timer_text = font.render(str(round(self.round_time - (time.time() - self.start_time))), True, text_color)
        timer_rect = timer_text.get_rect(center = (screen.get_width()/2, 0))
        screen.blit(timer_text, (timer_rect[0], timer_rect[1] + timer_rect.height/2))

        # Reset tooltip
        reset_text = font.render("Press r to reset", True, text_color)
        reset_text_rect = reset_text.get_rect(center=(screen.get_width()/2, screen.get_height()))
        screen.blit(reset_text, (reset_text_rect[0], reset_text_rect[1] - reset_text_rect.height/2))

    def update(self):
        # Reinitializes wave if wave is empty
        if len(self.wave.circles) == 0:
            wavetime = time.time() - self.wave.start_time
            self.wavetimes.append(wavetime)
            self.wave.__init__(self.circle_count)

class Wave:
    def __init__(self, circle_count):
        self.start_time = time.time()
        self.circle_count = circle_count
        self.circles = [Circle() for x in range(circle_count)]

class Circle:
    def __init__(self):
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(round(screen.get_height()*(1/3)), round(screen.get_height()*(2/3)))
        self.r = screen.get_height()/20
    
    def draw(self):
        # Circle
        pygame.gfxdraw.aacircle(screen, self.x, self.y, round(self.r), text_color)
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, round(self.r), text_color)

        # Small ellipse (very messy)
        ellipse_surface = pygame.Surface((round(10*self.r), round(10*self.r)), pygame.SRCALPHA)
        pygame.gfxdraw.filled_ellipse(ellipse_surface, round(5*self.r), round(2*self.r), round(3*self.r), round(1.8*self.r), text_color_lighter)
        pygame.gfxdraw.aaellipse(ellipse_surface, round(5*self.r), round(2*self.r), round(3*self.r), round(1.8*self.r), text_color_lighter)
        ellipse_surface = pygame.transform.rotate(ellipse_surface, 30)
        ellipse_surface = pygame.transform.scale_by(ellipse_surface, 0.13)
        screen.blit(ellipse_surface, (round(self.x - self.r), round(self.y - self.r)))
    
# Variables
pygame.display.set_caption("Aim Trainer")
screen = pygame.display.set_mode((1000,500), pygame.RESIZABLE)
clock = pygame.time.Clock()
base_font_name = "Arial"
title_font = pygame.font.Font("Fredoka-Bold.ttf", size=round(screen.get_height()/10))
font = pygame.font.Font("Fredoka-Bold.ttf", size=round(screen.get_height()/20))
shot_sound = pygame.mixer.Sound("shot.wav")
bg_color = pygame.Color(170, 238, 187)
text_color = pygame.Color(85, 130, 139)
text_color_lighter = pygame.Color(159, 200, 208)
pygame.mouse.set_cursor(pygame.cursors.broken_x)

# Main game loop
running = True
initialized = False
while running:
    # Initializing
    if not initialized:
        # Gets mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Fills screen
        screen.fill(bg_color)

        # Title text
        title_text = title_font.render("Aim Trainer", True, text_color)
        title_text_rect = title_text.get_rect(center = (screen.get_width()/2, screen.get_height()/4))
        screen.blit(title_text, title_text_rect)

        # Left initializer text
        start_text_left = font.render("Click this side for one bubble", True, text_color)
        start_text_left_rect = start_text_left.get_rect(center = (screen.get_width()/4, screen.get_height()/2))
        screen.blit(start_text_left, start_text_left_rect)

        # Right initializer text
        start_text_right = font.render("Click this side for five bubbles", True, text_color)
        start_text_right_rect = start_text_right.get_rect(center = (screen.get_width()*(3/4), screen.get_height()/2))
        screen.blit(start_text_right, start_text_right_rect)

        # Manually underlines left and right text depending on mouse position
        if mouse_x <= screen.get_width()/2:
            pygame.draw.line(screen, text_color, (start_text_left_rect.left, start_text_left_rect.top + start_text_left_rect.height), (start_text_left_rect.left + start_text_left_rect.width, start_text_left_rect.top + start_text_left_rect.height))
        elif mouse_x > screen.get_width()/2:
            pygame.draw.line(screen, text_color, (start_text_right_rect.left, start_text_right_rect.top + start_text_right_rect.height), (start_text_right_rect.left + start_text_right_rect.width, start_text_right_rect.top + start_text_right_rect.height))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_x <= screen.get_width()/2:
                    # Clicking left on startup gives waves with 1 circle
                    game = Game(1)
                    initialized = True
                elif mouse_x > screen.get_width()/2:
                    # Clicking right on startup gives waves with 5 circles
                    game = Game(5)
                    initialized = True
        pygame.display.flip()
        clock.tick(60)
    
    # Main game loop
    if running and initialized:
        # Event checking
        for event in pygame.event.get():
            # Exits the loop when window is closed
            if event.type == pygame.QUIT:
                running = False

            # Shoots
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.shoot()

            # Reset button
            if pygame.key.get_pressed()[pygame.K_r]:
                initialized = False
                break
        
        # Fills screen with background color
        screen.fill(bg_color)

        # Updates the game
        game.draw()
        game.update()

        # Reinitializes game if time is up
        if (time.time() - game.start_time) > game.round_time:
            end_game_string = f"Circles: {game.hit_counter}"
            end_game_text = font.render(end_game_string, True, text_color)
            end_game_rect = end_game_text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
            pygame.draw.rect(screen, bg_color, end_game_rect)
            screen.blit(end_game_text, (end_game_rect))
            pygame.display.update(end_game_rect) 
            time.sleep(1)
            pygame.event.clear()
            initialized = False

        # Renders whole screen
        pygame.display.flip()

        # Lock fps
        clock.tick(60)

# Quits game
pygame.quit()