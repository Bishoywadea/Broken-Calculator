import pygame
import random
import math
from view.config import Config
from view.menu import Menu
from view.ui import UI
from logic.equation_validator import EquationValidator
from logic.score_calculator import ScoreCalculator
from logic.broken_button_validator import BrokenButtonValidator

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
        self.ui = None
        self.target_number = 0
        self.difficulty = "easy"
        self.equations = []
        self.current_equation = ""
        self.equation_validator = EquationValidator()
        self.score_calculator = ScoreCalculator()
        self.broken_validator = BrokenButtonValidator()
        self.total_score = 0
        self.game_completed = False
        self.animation_time = 0
        self.stars = []
        self.broken_buttons = []
        
    def start_level(self, difficulty):
        """Start a new game with selected difficulty."""
        self.difficulty = difficulty
        self.current_state = self.STATE_PLAYING
        
        # Generate target number based on difficulty
        if difficulty == "easy":
            self.target_number = random.randint(10, 50)
            broken_count = 3
        elif difficulty == "medium":
            self.target_number = random.randint(50, 100)
            broken_count = 5
        else:  # hard
            self.target_number = random.randint(100, 200)
            broken_count = 7
        
        # Generate broken buttons ensuring puzzle is solvable
        self.broken_buttons = self.broken_validator.generate_broken_buttons(
            self.target_number, broken_count
        )
        
        # Reset game state
        self.equations = []
        self.current_equation = ""
        self.total_score = 0
        self.game_completed = False
        self.stars = []
        
        # Initialize UI
        self.ui = UI(self)
        
    def is_button_broken(self, value):
        """Check if a button is broken."""
        return value in self.broken_buttons
        
    def handle_event(self, event):
        """Handle game events."""
        if self.current_state == self.STATE_MENU:
            self.menu.handle_event(event)
        elif self.current_state == self.STATE_PLAYING:
            if self.ui:
                self.ui.handle_event(event)
                
    def return_to_menu(self):
        """Return to main menu."""
        self.current_state = self.STATE_MENU
            
    def update(self, dt):
        """Update game state."""
        self.animation_time += dt / 1000.0
        
        if self.current_state == self.STATE_PLAYING and self.ui:
            self.ui.update(dt)
        
    def render(self):
        """Render the game."""
        if self.current_state == self.STATE_MENU:
            self.menu.draw(self.screen)
        elif self.current_state == self.STATE_PLAYING:
            # Draw light gradient background
            self.draw_gradient_background(self.screen)
            
            # Draw UI
            if self.ui:
                self.ui.draw(self.screen)
    
    def draw_gradient_background(self, screen):
        """Draw light gradient background."""
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            # Light gradient
            r = int(240 + (250 - 240) * ratio)
            g = int(245 + (255 - 245) * ratio)
            b = 255
            pygame.draw.line(screen, (r, g, b), (0, y), (Config.SCREEN_WIDTH, y))