import pygame

class CalcButton:
    def __init__(self, x, y, width, height, value, display_value=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.display_value = display_value or value
        self.hovered = False
        self.pressed = False
        self.broken = False
        
    def handle_event(self, event, game_manager):
        if self.broken:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        return False
    
    def draw(self, surface):
        if self.broken:
            # Broken button - gray and disabled
            color = (200, 200, 200)
            text_color = (150, 150, 150)
        else:
            # Working button
            if self.pressed:
                color = (220, 220, 220)
            elif self.hovered:
                color = (240, 240, 240)
            else:
                color = (255, 255, 255)
            text_color = (50, 50, 50)
        
        # Special color for equals button
        if self.value == '=' and not self.broken:
            if self.pressed:
                color = (255, 180, 180)
            elif self.hovered:
                color = (255, 200, 200)
            else:
                color = (255, 220, 220)
        
        # Draw button with rounded corners
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, (180, 180, 180), self.rect, 2, border_radius=12)
        
        # Draw text
        font_size = 36
        font = pygame.font.Font(None, font_size)
        
        text_surface = font.render(str(self.display_value), True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)