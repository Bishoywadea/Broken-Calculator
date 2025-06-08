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
        
    def setup_ui(self):
        """Set up UI elements."""
        # Calculator centered on screen
        calc_width = 380
        calc_height = 500
        calc_x = (Config.SCREEN_WIDTH - calc_width) // 2
        calc_y = (Config.SCREEN_HEIGHT - calc_height) // 2 - 50
        
        # Create menu button for now
        self.menu_button = pygame.Rect(
            calc_x,
            calc_y + calc_height + 20,
            180,
            50
        )
    
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
        # Draw placeholder text for now
        font = pygame.font.Font(None, 72)
        text = font.render(f"Target: {self.game_manager.target_number}", True, (50, 50, 50))
        rect = text.get_rect(center=(Config.SCREEN_WIDTH // 2, 100))
        surface.blit(text, rect)
        
        # Draw menu button
        if self.menu_button:
            pygame.draw.rect(surface, (200, 200, 200), self.menu_button)
            font = pygame.font.Font(None, 36)
            text = font.render("Back to Menu", True, (50, 50, 50))
            text_rect = text.get_rect(center=self.menu_button.center)
            surface.blit(text, text_rect)

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