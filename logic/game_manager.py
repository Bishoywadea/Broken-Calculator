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
            if self.ui.handle_event(event):
                return
            
    def return_to_menu(self):
        """Return to main menu."""
        self.current_state = self.STATE_MENU
            
    def update(self, dt):
        """Update game state."""
        self.animation_time += dt / 1000.0

        for star in self.stars[:]:
            star['x'] += star['vx']
            star['y'] += star['vy']
            star['life'] -= 0.01
            star['vy'] += 0.1
        
            if star['life'] <= 0:
                self.stars.remove(star)
        
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
            if self.game_completed:
                self.draw_stars(self.screen)
    
    def draw_gradient_background(self, screen):
        """Draw light gradient background."""
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            # Light gradient
            r = int(240 + (250 - 240) * ratio)
            g = int(245 + (255 - 245) * ratio)
            b = 255
            pygame.draw.line(screen, (r, g, b), (0, y), (Config.SCREEN_WIDTH, y))

    def submit_equation(self):
        """Submit the current equation for validation."""
        if not self.current_equation.strip():
            return
        
        # Convert display symbols back to Python operators
        equation_for_eval = self.current_equation.replace("×", "*").replace("÷", "/")
        
        # Validate equation
        result = self.equation_validator.validate(equation_for_eval, self.target_number)
        
        if result['valid']:
            # Check if equation is unique
            if not self.is_equation_unique(equation_for_eval):
                self.ui.show_message("Equation already used!", "error")
                return
            
            # Calculate score
            score = self.score_calculator.calculate_score(equation_for_eval)
            
            # Add equation to list
            self.equations.append({
                'equation': self.current_equation,
                'score': score
            })
            
            self.total_score += score
            self.current_equation = ""
            
            # Check if game is complete
            if len(self.equations) >= 5:
                self.complete_game()
        else:
            self.ui.show_message(result['error'], "error")

    def is_equation_unique(self, equation):
        """Check if equation is unique (not just reordered)."""
        equation_normalized = equation.replace(" ", "")
        for eq in self.equations:
            if self.equation_validator.are_equations_equivalent(
                equation_normalized, 
                eq['equation'].replace("×", "*").replace("÷", "/").replace(" ", "")
            ):
                return False
        return True

    def complete_game(self):
        """Handle game completion."""
        self.game_completed = True
        self.generate_celebration_stars()


    def generate_celebration_stars(self):
        """Generate stars for celebration animation."""
        for _ in range(30):
            self.stars.append({
                'x': random.randint(100, Config.SCREEN_WIDTH - 100),
                'y': random.randint(100, Config.SCREEN_HEIGHT - 100),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.randint(5, 15),
                'color': random.choice([(255, 255, 100), (255, 200, 100), (255, 150, 150)]),
                'life': 1.0
            })

    def draw_stars(self, screen):
        """Draw celebration stars."""
        for star in self.stars:
            alpha = star['life']
            size = int(star['size'] * alpha)
            if size > 0:
                color = tuple(int(c * alpha) for c in star['color'])
                self.draw_star(screen, star['x'], star['y'], size, color)

    def draw_star(self, screen, x, y, size, color):
        """Draw a star shape."""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                px = x + size * math.cos(angle)
                py = y + size * math.sin(angle)
            else:
                px = x + (size * 0.4) * math.cos(angle)
                py = y + (size * 0.4) * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)