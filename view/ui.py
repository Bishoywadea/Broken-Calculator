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