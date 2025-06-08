import pygame
from view.config import Config

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
    
    def handle_event(self, event):
        """Handle UI events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button and self.menu_button.collidepoint(event.pos):
                self.game_manager.return_to_menu()
                return True
        return False
    
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

    def setup_ui(self):
        """Set up UI elements."""
        # Calculator centered on screen
        calc_width = 380
        calc_height = 500
        calc_x = (Config.SCREEN_WIDTH - calc_width) // 2
        calc_y = (Config.SCREEN_HEIGHT - calc_height) // 2 - 50
        
        # Create calculator buttons
        button_size = 80
        button_spacing = 10
        
        # Define button layout - each tuple is (display_text, actual_value)
        button_layout = [
            [('C', 'C'), ('(', '('), (')', ')'), ('÷', '/')],
            [('7', '7'), ('8', '8'), ('9', '9'), ('×', '*')],
            [('4', '4'), ('5', '5'), ('6', '6'), ('-', '-')],
            [('1', '1'), ('2', '2'), ('3', '3'), ('+', '+')],
            [('0', '0'), ('.', '.'), ('⌫', 'backspace'), ('=', '=')]
        ]
        
        # Calculate starting position for button grid
        grid_start_x = calc_x + (calc_width - (4 * button_size + 3 * button_spacing)) // 2
        grid_start_y = calc_y + 110
        
        for row_idx, row in enumerate(button_layout):
            for col_idx, button_data in enumerate(row):
                display, value = button_data  # Unpack the tuple
                x = grid_start_x + col_idx * (button_size + button_spacing)
                y = grid_start_y + row_idx * (button_size + button_spacing)
                
                # Create button with correct parameters
                button = CalcButton(x, y, button_size, button_size, value, display)
                
                # Check if this button should be broken
                if value in self.game_manager.broken_buttons:
                    button.broken = True
                
                self.calc_buttons.append(button)
        
        self.menu_button = CalcButton(
            calc_x,
            calc_y + 100 + 5 * (button_size + button_spacing) + 20,
            4 * button_size + 3 * button_spacing,
            50,
            'menu',
            'New Game'
        )

    def handle_event(self, event):
        """Handle UI events."""
        # Handle calculator button clicks
        for button in self.calc_buttons:
            if button.handle_event(event, self.game_manager):  # Pass game_manager
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
        """Draw the calculator."""
        # Calculator background
        calc_width = 380
        calc_height = 500
        calc_x = (Config.SCREEN_WIDTH - calc_width) // 2
        calc_y = (Config.SCREEN_HEIGHT - calc_height) // 2 - 50
        
        calc_rect = pygame.Rect(calc_x, calc_y, calc_width, calc_height)
        pygame.draw.rect(surface, (255, 255, 255), calc_rect, border_radius=20)
        pygame.draw.rect(surface, (200, 200, 200), calc_rect, 3, border_radius=20)
        
        # Draw display
        display_rect = pygame.Rect(
            calc_x + 20,
            calc_y + 20,
            calc_width - 40,
            70
        )
        pygame.draw.rect(surface, (250, 250, 250), display_rect, border_radius=10)
        pygame.draw.rect(surface, (200, 200, 200), display_rect, 2, border_radius=10)
        
        # Display text
        font = pygame.font.Font(None, 48)
        if self.game_manager.current_equation:
            text = self.game_manager.current_equation
        else:
            text = "0"
        
        # Truncate if too long
        if len(text) > 15:
            text = "..." + text[-12:]
        
        text_surface = font.render(text, True, (50, 50, 50))
        text_rect = text_surface.get_rect(midright=(display_rect.right - 15, display_rect.centery))
        surface.blit(text_surface, text_rect)
        
        # Draw calculator buttons
        for button in self.calc_buttons:
            button.draw(surface)

    def draw_message(self, surface):
        """Draw temporary message."""
        font = pygame.font.Font(None, 36)
        
        color = (200, 50, 50) if self.message_type == "error" else (50, 200, 50)
        message_surface = font.render(self.message, True, color)
        message_rect = message_surface.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 100))
        
        # Background
        bg_rect = message_rect.inflate(40, 20)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, border_radius=10)
        pygame.draw.rect(surface, color, bg_rect, 2, border_radius=10)
        
        surface.blit(message_surface, message_rect)

    def draw_target_section(self, surface):
        """Draw target number with character."""
        # Position
        section_x = 200
        section_y = Config.SCREEN_HEIGHT // 2 - 150
        
        # Target label
        font_label = pygame.font.Font(None, 36)
        label_surface = font_label.render("Target:", True, (100, 100, 100))
        label_rect = label_surface.get_rect(center=(section_x, section_y))
        surface.blit(label_surface, label_rect)
        
        # Target number in circle
        circle_y = section_y + 60
        pygame.draw.circle(surface, (255, 230, 150), (section_x, circle_y), 50)
        pygame.draw.circle(surface, (220, 180, 100), (section_x, circle_y), 50, 3)
        
        font_number = pygame.font.Font(None, 64)
        number_surface = font_number.render(str(self.game_manager.target_number), True, (50, 50, 50))
        number_rect = number_surface.get_rect(center=(section_x, circle_y))
        surface.blit(number_surface, number_rect)

        # Draw character
        self.draw_character(surface, section_x, circle_y + 100)


    def draw_character(self, surface, x, y):
        """Draw the mascot character from image."""
        # Center the image at the given position
        rect = self.character_image.get_rect(center=(x, y))
        surface.blit(self.character_image, rect)

    def draw_score(self, surface):
        """Draw the total score."""
        font = pygame.font.Font(None, 48)
        score_text = f"Score: {self.game_manager.total_score}"
        score_surface = font.render(score_text, True, (255, 215, 0))
        score_rect = score_surface.get_rect(topright=(Config.SCREEN_WIDTH - 50, 50))
        surface.blit(score_surface, score_rect)

    def draw_equations_panel(self, surface):
        """Draw the equations panel."""
        panel_width = 300
        panel_height = 400
        panel_x = Config.SCREEN_WIDTH - panel_width - 100
        panel_y = (Config.SCREEN_HEIGHT - panel_height) // 2 - 50
        
        # Panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, border_radius=20)
        pygame.draw.rect(surface, (200, 200, 200), panel_rect, 3, border_radius=20)
        
        # Title
        font_title = pygame.font.Font(None, 36)
        title_surface = font_title.render("Your Equations", True, (50, 50, 50))
        title_rect = title_surface.get_rect(center=(panel_rect.centerx, panel_rect.top + 30))
        surface.blit(title_surface, title_rect)
        
        # Draw equation slots
        slot_height = 60
        slot_margin = 10
        start_y = panel_rect.top + 70
        
        font_eq = pygame.font.Font(None, 28)
        font_score = pygame.font.Font(None, 24)
        
        for i in range(5):
            slot_y = start_y + i * (slot_height + slot_margin)
            slot_rect = pygame.Rect(
                panel_rect.left + 20,
                slot_y,
                panel_rect.width - 40,
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
        
        # Panel background
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, border_radius=30)
        pygame.draw.rect(surface, (255, 215, 0), panel_rect, 4, border_radius=30)
        
        # Title
        font_title = pygame.font.Font(None, 72)
        title_surface = font_title.render("Excellent!", True, (50, 200, 50))
        title_rect = title_surface.get_rect(center=(panel_rect.centerx, panel_rect.top + 80))
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