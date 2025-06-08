import pygame
from view.config import Config
from view.menu import Menu

class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_info = pygame.display.Info()
        Config.SCREEN_WIDTH = screen_info.current_w
        Config.SCREEN_HEIGHT = screen_info.current_h
        
        pygame.display.set_caption("Broken Calculator")
        
        # Game states
        self.STATE_MENU = "menu"
        self.STATE_PLAYING = "playing"
        self.current_state = self.STATE_MENU
        
        # Menu
        self.menu = Menu(self)
        
        # Game components
        self.difficulty = "easy"
        
    def start_level(self, difficulty):
        """Start a new game with selected difficulty."""
        self.difficulty = difficulty
        self.current_state = self.STATE_PLAYING
        print(f"Starting {difficulty} level")
        
    def handle_event(self, event):
        """Handle game events."""
        if self.current_state == self.STATE_MENU:
            self.menu.handle_event(event)
            
    def update(self, dt):
        """Update game state."""
        pass
    
    def render(self):
        """Render the game."""
        if self.current_state == self.STATE_MENU:
            self.menu.draw(self.screen)
        elif self.current_state == self.STATE_PLAYING:
            # For now, just show a placeholder
            self.screen.fill((240, 245, 255))
            font = pygame.font.Font(None, 72)
            text = font.render(f"{self.difficulty.capitalize()} Game", True, (50, 50, 50))
            rect = text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
            self.screen.blit(text, rect)