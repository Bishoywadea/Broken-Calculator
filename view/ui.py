import pygame
from view.config import Config

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