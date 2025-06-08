import pygame
import math
import random
from view.config import Config

class Menu:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font_title = pygame.font.Font(None, 84)
        self.font_button = pygame.font.Font(None, 56)
        self.font_desc = pygame.font.Font(None, 42)
        
        # Animation
        self.animation_time = 0
        self.stars = []
        self.generate_stars()
        
        # Buttons
        self.difficulty_buttons = []
        self.setup_buttons()
        
    def generate_stars(self):
        """Generate background stars."""
        for _ in range(30):
            self.stars.append({
                'x': random.randint(0, Config.SCREEN_WIDTH),
                'y': random.randint(0, Config.SCREEN_HEIGHT),
                'size': random.randint(2, 6),
                'speed': random.uniform(0.5, 2)
            })
    
    def setup_buttons(self):
        """Set up difficulty buttons."""
        button_width = 300
        button_height = 80
        button_spacing = 30
        
        difficulties = [
            {'name': 'Easy', 'color': (100, 255, 100), 'desc': 'Target: 10-50'},
            {'name': 'Medium', 'color': (255, 255, 100), 'desc': 'Target: 50-100'},
            {'name': 'Hard', 'color': (255, 100, 100), 'desc': 'Target: 100-200'}
        ]
        
        start_y = Config.SCREEN_HEIGHT // 2 - (len(difficulties) * (button_height + button_spacing)) // 2
        
        for i, diff in enumerate(difficulties):
            y_pos = start_y + i * (button_height + button_spacing)
            self.difficulty_buttons.append({
                'rect': pygame.Rect(
                    (Config.SCREEN_WIDTH - button_width) // 2,
                    y_pos,
                    button_width,
                    button_height
                ),
                'difficulty': diff['name'].lower(),
                'color': diff['color'],
                'desc': diff['desc'],
                'hovered': False
            })
    
    def handle_event(self, event):
        """Handle menu events."""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            for button in self.difficulty_buttons:
                button['hovered'] = button['rect'].collidepoint(mouse_pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for button in self.difficulty_buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        self.game_manager.start_level(button['difficulty'])
                        return True
        return False
    
    def update(self):
        """Update menu animations."""
        self.animation_time += 0.02
        
        # Update stars
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > Config.SCREEN_HEIGHT:
                star['y'] = -10
                star['x'] = random.randint(0, Config.SCREEN_WIDTH)
    
    def draw(self, screen):
        """Draw the menu."""
        self.update()
        
        # Draw gradient background
        self.draw_gradient_background(screen)
        
        # Draw stars
        self.draw_stars(screen)
        
        # Draw title
        self.draw_title(screen)
        
        # Draw subtitle
        self.draw_subtitle(screen)
        
        # Draw difficulty buttons
        for button in self.difficulty_buttons:
            self.draw_button(screen, button)
    
    def draw_gradient_background(self, screen):
        """Draw gradient background."""
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            r = int(50 + (100 - 50) * ratio)
            g = int(100 + (150 - 100) * ratio)
            b = int(200 + (255 - 200) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (Config.SCREEN_WIDTH, y))
    
    def draw_stars(self, screen):
        """Draw animated stars."""
        for star in self.stars:
            brightness = int(128 + 127 * math.sin(self.animation_time * 2 + star['x']))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])
    
    def draw_title(self, screen):
        """Draw the game title."""
        title_text = "Broken Calculator"
        title_surface = self.font_title.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(Config.SCREEN_WIDTH // 2, 100))
        
        # Shadow
        shadow_surface = self.font_title.render(title_text, True, (30, 30, 30))
        shadow_rect = shadow_surface.get_rect(center=(title_rect.centerx + 4, title_rect.centery + 4))
        screen.blit(shadow_surface, shadow_rect)
        
        # Main title
        screen.blit(title_surface, title_rect)
    
    def draw_subtitle(self, screen):
        """Draw the subtitle."""
        subtitle_text = "Create 5 equations that equal the target!"
        subtitle_surface = self.font_desc.render(subtitle_text, True, (255, 255, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(Config.SCREEN_WIDTH // 2, 180))
        screen.blit(subtitle_surface, subtitle_rect)
    
    def draw_button(self, screen, button):
        """Draw a difficulty button."""
        rect = button['rect']
        color = button['color']
        
        # Hover effect
        if button['hovered']:
            rect = rect.inflate(10, 10)
            color = tuple(min(255, c + 30) for c in color)
        
        # Shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=15)
        
        # Button
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=15)
        
        # Text
        text_surface = self.font_button.render(button['difficulty'].capitalize(), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery - 10))
        screen.blit(text_surface, text_rect)
        
        # Description
        desc_surface = pygame.font.Font(None, 28).render(button['desc'], True, (50, 50, 50))
        desc_rect = desc_surface.get_rect(center=(rect.centerx, rect.centery + 20))
        screen.blit(desc_surface, desc_rect)