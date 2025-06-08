import pygame
from view.config import Config
from view.calc_button import CalcButton

class UI:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.calc_buttons = []
        self.new_game_button = None
        self.message = ""
        self.message_type = ""
        self.message_timer = 0
        self.character_animation = 0
        self.menu_button = None
        self.character_image = pygame.image.load("assets/images/teacher.png").convert_alpha()
        self.character_image = pygame.transform.scale(self.character_image, (100, 150))

        self.setup_ui()
    
    def show_message(self, message, message_type="info"):  
        """Show a temporary message."""
        self.message = message
        self.message_type = message_type
        self.message_timer = 2000
    
    def update(self, dt):  
        """Update UI state."""
        if self.message_timer > 0:
            self.message_timer -= dt
        
        # Update character animation
        self.character_animation += dt / 1000.0
    
    def draw(self, surface):  
        """Draw the UI."""

        self.draw_background_sections(surface)

        # Draw calculator
        self.draw_calculator(surface)
        
        # Draw menu button
        self.menu_button.draw(surface)
        
        # Draw message
        if self.message_timer > 0:
            self.draw_message(surface)

        # Draw target with character
        self.draw_target_section(surface)

        # Draw equations panel
        self.draw_equations_panel(surface)

        # Draw score
        self.draw_score(surface)

        # Draw Completion screen
        if self.game_manager.game_completed:
            self.draw_completion_screen(surface)

    def draw_background_sections(self, surface):  
        """Draw subtle background sections for better visual organization."""
        # Left section background (target area)
        left_bg = pygame.Rect(0, 0, 250, Config.SCREEN_HEIGHT)
        pygame.draw.rect(surface, (245, 245, 250), left_bg)
        
        # Right section background (equations panel area)
        right_bg = pygame.Rect(Config.SCREEN_WIDTH - 350, 0, 350, Config.SCREEN_HEIGHT)
        pygame.draw.rect(surface, (248, 248, 252), right_bg)

    def setup_ui(self):  
        """Set up UI elements."""
        # Calculator centered on screen
        calc_width = 320
        calc_height = 460
        calc_x = Config.SCREEN_WIDTH // 2 - calc_width - 50
        calc_y = (Config.SCREEN_HEIGHT - calc_height) // 2
        
        # Create calculator buttons
        button_size = 65
        button_spacing = 8
        
        # Define button layout
        button_layout = [
            [('C', 'C'), ('(', '('), (')', ')'), ('÷', '/')],
            [('7', '7'), ('8', '8'), ('9', '9'), ('×', '*')],
            [('4', '4'), ('5', '5'), ('6', '6'), ('-', '-')],
            [('1', '1'), ('2', '2'), ('3', '3'), ('+', '+')],
            [('0', '0'), ('.', '.'), ('⌫', 'backspace'), ('=', '=')]
        ]
        
        # Calculate starting position for button grid
        grid_start_x = calc_x + 20
        grid_start_y = calc_y + 100
        
        for row_idx, row in enumerate(button_layout):
            for col_idx, button_data in enumerate(row):
                display, value = button_data
                x = grid_start_x + col_idx * (button_size + button_spacing)
                y = grid_start_y + row_idx * (button_size + button_spacing)
                
                button = CalcButton(x, y, button_size, button_size, value, display)
                
                if value in self.game_manager.broken_buttons:
                    button.broken = True
                
                self.calc_buttons.append(button)
        
        self.menu_button = CalcButton(
            calc_x,
            calc_y + calc_height + 15,
            calc_width,
            45,
            'menu',
            'New Game'
        )

    def handle_event(self, event):   
        """Handle UI events."""
        for button in self.calc_buttons:
            if button.handle_event(event, self.game_manager): 
                self.handle_calc_button(button.value)
                return True
        
        # Handle menu button
        if self.menu_button.handle_event(event, self.game_manager):
            self.game_manager.return_to_menu()
            return True
            
        return False

    def handle_calc_button(self, value):   
        """Handle calculator button press."""
        if self.game_manager.game_completed:
            return
        
        if self.game_manager.is_button_broken(value):
            self.show_message("That button is broken!", "error")
            return
            
        if value == 'C':
            self.game_manager.current_equation = ""
        elif value == 'backspace':
            self.game_manager.current_equation = self.game_manager.current_equation[:-1]
        elif value == '=':
            self.game_manager.submit_equation()
        else:
            # Add to equation
            if value == '/':
                self.game_manager.current_equation += '÷'
            elif value == '*':
                self.game_manager.current_equation += '×'
            else:
                self.game_manager.current_equation += value

    def draw_calculator(self, surface):   
        """Draw the calculator with proper spacing."""
        # Calculator positioned slightly to the left
        calc_width = 320
        calc_height = 460
        calc_x = Config.SCREEN_WIDTH // 2 - calc_width - 50
        calc_y = (Config.SCREEN_HEIGHT - calc_height) // 2
        
        # Calculator background with shadow
        shadow_rect = pygame.Rect(calc_x + 5, calc_y + 5, calc_width, calc_height)
        pygame.draw.rect(surface, (200, 200, 200), shadow_rect, border_radius=20)
        
        calc_rect = pygame.Rect(calc_x, calc_y, calc_width, calc_height)
        pygame.draw.rect(surface, (255, 255, 255), calc_rect, border_radius=20)
        pygame.draw.rect(surface, (180, 180, 180), calc_rect, 3, border_radius=20)
        
        # Draw display
        display_rect = pygame.Rect(
            calc_x + 15,
            calc_y + 15,
            calc_width - 30,
            60
        )
        pygame.draw.rect(surface, (240, 240, 240), display_rect, border_radius=10)
        pygame.draw.rect(surface, (200, 200, 200), display_rect, 2, border_radius=10)
        
        # Display text
        font = pygame.font.Font(None, 42)
        text = self.game_manager.current_equation if self.game_manager.current_equation else "0"
        
        # Truncate if too long
        if len(text) > 15:
            text = "..." + text[-12:]
        
        text_surface = font.render(text, True, (50, 50, 50))
        text_rect = text_surface.get_rect(midright=(display_rect.right - 10, display_rect.centery))
        surface.blit(text_surface, text_rect)
        
        # Draw calculator buttons
        for button in self.calc_buttons:
            button.draw(surface)

    def draw_message(self, surface):  
        """Draw temporary message at the bottom."""
        font = pygame.font.Font(None, 36)
        
        color = (200, 50, 50) if self.message_type == "error" else (50, 200, 50)
        message_surface = font.render(self.message, True, color)
        message_rect = message_surface.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 80))
        
        # Background with semi-transparency
        bg_rect = message_rect.inflate(40, 20)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(240)
        bg_surface.fill((255, 255, 255))
        surface.blit(bg_surface, bg_rect)
        
        # Border
        pygame.draw.rect(surface, color, bg_rect, 2, border_radius=10)
        
        # Message text
        surface.blit(message_surface, message_rect)

    def draw_target_section(self, surface):  
        """Draw target section with better layout."""
        section_x = 125
        section_y = 150
        
        # Target label
        font_label = pygame.font.Font(None, 32)
        label_surface = font_label.render("Target:", True, (80, 80, 80))
        label_rect = label_surface.get_rect(center=(section_x, section_y))
        surface.blit(label_surface, label_rect)
        
        # Target number in larger circle
        circle_y = section_y + 70
        pygame.draw.circle(surface, (255, 235, 170), (section_x, circle_y), 55)
        pygame.draw.circle(surface, (220, 180, 100), (section_x, circle_y), 55, 3)
        
        font_number = pygame.font.Font(None, 72)
        number_surface = font_number.render(str(self.game_manager.target_number), True, (50, 50, 50))
        number_rect = number_surface.get_rect(center=(section_x, circle_y))
        surface.blit(number_surface, number_rect)
        
        # Draw character below target with better positioning
        self.draw_character(surface, section_x, circle_y + 140)


    def draw_character(self, surface, x, y):   
        """Draw the mascot character with animation."""
        y_offset = int(5 * pygame.math.Vector2(0, 1).rotate(self.character_animation * 100).y)
        
        rect = self.character_image.get_rect(center=(x, y + y_offset))
        surface.blit(self.character_image, rect)

    def draw_score(self, surface):  
        """Draw the total score in the top-right corner."""
        # Score background
        score_bg_rect = pygame.Rect(Config.SCREEN_WIDTH - 200, 30, 170, 50)
        pygame.draw.rect(surface, (255, 255, 255), score_bg_rect, border_radius=25)
        pygame.draw.rect(surface, (255, 215, 0), score_bg_rect, 3, border_radius=25)
        
        # Score text
        font = pygame.font.Font(None, 42)
        score_text = f"Score: {self.game_manager.total_score}"
        score_surface = font.render(score_text, True, (255, 180, 0))
        score_rect = score_surface.get_rect(center=score_bg_rect.center)
        surface.blit(score_surface, score_rect)

    def draw_equations_panel(self, surface):  
        """Draw equations panel with better positioning."""
        panel_width = 300
        panel_height = 420
        panel_x = Config.SCREEN_WIDTH - panel_width - 25
        panel_y = (Config.SCREEN_HEIGHT - panel_height) // 2
        
        # Panel shadow
        shadow_rect = pygame.Rect(panel_x + 3, panel_y + 3, panel_width, panel_height)
        pygame.draw.rect(surface, (210, 210, 210), shadow_rect, border_radius=20)
        
        # Panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, border_radius=20)
        pygame.draw.rect(surface, (180, 180, 180), panel_rect, 3, border_radius=20)
        
        # Title
        font_title = pygame.font.Font(None, 32)
        title_surface = font_title.render("Your Equations", True, (50, 50, 50))
        title_rect = title_surface.get_rect(center=(panel_rect.centerx, panel_rect.top + 25))
        surface.blit(title_surface, title_rect)
        
        # Draw equation slots
        slot_height = 65
        slot_margin = 8
        start_y = panel_rect.top + 60
        
        font_eq = pygame.font.Font(None, 26)
        font_score = pygame.font.Font(None, 22)
        
        for i in range(5):
            slot_y = start_y + i * (slot_height + slot_margin)
            slot_rect = pygame.Rect(
                panel_rect.left + 15,
                slot_y,
                panel_rect.width - 30,
                slot_height
            )
            
            if i < len(self.game_manager.equations):
                # Filled slot
                eq_data = self.game_manager.equations[i]
                pygame.draw.rect(surface, (240, 255, 240), slot_rect, border_radius=10)
                pygame.draw.rect(surface, (150, 220, 150), slot_rect, 2, border_radius=10)
                
                # Equation
                eq_text = f"{eq_data['equation']} = {self.game_manager.target_number}"
                eq_surface = font_eq.render(eq_text, True, (50, 50, 50))
                eq_rect = eq_surface.get_rect(midleft=(slot_rect.left + 10, slot_rect.centery - 10))
                surface.blit(eq_surface, eq_rect)
                
                # Score
                score_text = f"+{eq_data['score']} pts"
                score_surface = font_score.render(score_text, True, (255, 180, 0))
                score_rect = score_surface.get_rect(midleft=(slot_rect.left + 10, slot_rect.centery + 15))
                surface.blit(score_surface, score_rect)
            else:
                # Empty slot
                pygame.draw.rect(surface, (250, 250, 250), slot_rect, border_radius=10)
                pygame.draw.rect(surface, (220, 220, 220), slot_rect, 2, border_radius=10)
                
                # Placeholder
                placeholder = f"Equation {i + 1}"
                placeholder_surface = font_eq.render(placeholder, True, (200, 200, 200))
                placeholder_rect = placeholder_surface.get_rect(center=slot_rect.center)
                surface.blit(placeholder_surface, placeholder_rect)

    def draw_completion_screen(self, surface):  
        """Draw game completion overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Completion panel
        panel_width = 600
        panel_height = 400
        panel_rect = pygame.Rect(
            (Config.SCREEN_WIDTH - panel_width) // 2,
            (Config.SCREEN_HEIGHT - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        # Panel shadow
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 8
        shadow_rect.y += 8
        pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=30)
        
        # Panel background
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, border_radius=30)
        pygame.draw.rect(surface, (255, 215, 0), panel_rect, 4, border_radius=30)
        
        # Stars decoration
        star_y = panel_rect.top + 50
        for i in range(3):
            star_x = panel_rect.centerx + (i - 1) * 80
            self.draw_star(surface, star_x, star_y, 25, (255, 215, 0))
        
        # Title
        font_title = pygame.font.Font(None, 72)
        title_surface = font_title.render("Excellent!", True, (50, 200, 50))
        title_rect = title_surface.get_rect(center=(panel_rect.centerx, panel_rect.top + 120))
        surface.blit(title_surface, title_rect)
        
        # Score display
        font_large = pygame.font.Font(None, 56)
        font_medium = pygame.font.Font(None, 42)
        
        score_surface = font_large.render(f"Final Score: {self.game_manager.total_score}", 
                                        True, (255, 180, 0))
        score_rect = score_surface.get_rect(center=(panel_rect.centerx, panel_rect.centery))
        surface.blit(score_surface, score_rect)
        
        # Difficulty
        difficulty_text = f"Difficulty: {self.game_manager.difficulty.capitalize()}"
        diff_surface = font_medium.render(difficulty_text, True, (100, 100, 100))
        diff_rect = diff_surface.get_rect(center=(panel_rect.centerx, panel_rect.centery + 60))
        surface.blit(diff_surface, diff_rect)
        
        # Broken buttons count
        broken_count = len(self.game_manager.broken_buttons)
        broken_text = f"With {broken_count} broken buttons!"
        broken_surface = font_medium.render(broken_text, True, (200, 100, 100))
        broken_rect = broken_surface.get_rect(center=(panel_rect.centerx, panel_rect.centery + 110))
        surface.blit(broken_surface, broken_rect)
        
        # New Game prompt
        prompt_font = pygame.font.Font(None, 32)
        prompt_text = "Click 'New Game' to play again!"
        prompt_surface = prompt_font.render(prompt_text, True, (100, 100, 100))
        prompt_rect = prompt_surface.get_rect(center=(panel_rect.centerx, panel_rect.bottom - 40))
        surface.blit(prompt_surface, prompt_rect)

    def draw_star(self, surface, x, y, size, color):  
        """Draw a star shape."""
        import math
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.5
            px = x + radius * math.cos(angle - math.pi / 2)
            py = y + radius * math.sin(angle - math.pi / 2)
            points.append((px, py))
        pygame.draw.polygon(surface, color, points)