# This file is part of the Broken Calculator game.
# Copyright (C) 2025 Bishoy Wadea
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import pygame
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gettext import gettext as _


class main:
    def __init__(self, journal=True):
        self.journal = journal
        self.running = True
        self.canvas = None
        self.show_help = False
        self.activity = None
        self.game = None
        self.ui = None

    def set_activity(self, activity):
        """Set reference to the Sugar activity."""
        self.activity = activity
        if self.game:
            self.game.set_activity(activity)

    def set_canvas(self, canvas):
        """Set the Pygame canvas."""
        self.canvas = canvas
        pygame.display.set_caption(_("Broken Calculator"))

    def get_save_data(self):
        """Get the current game state for saving."""
        pass

    def load_from_journal(self, save_data):
        """Load game state from journal data."""
        pass

    def toggle_help(self):
        """Toggle help display."""
        self.show_help = not self.show_help

    def quit(self):
        """Quit the game."""
        self.running = False

    def check_events(self):
        """Handle Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.show_help:
                    self.show_help = False

    def draw_help(self, screen):
        """Draw the help panel."""
        if self.show_help:
            # Create help text
            font = pygame.font.Font(None, 36)
            help_text = [
                _("Broken Calculator Rules:"),
                _("1. Create equations that equal the target number"),
                _("2. Some buttons are broken and can't be used"),
                _("3. Each correct equation earns points"),
                _("4. More complex equations earn more points"),
                _("5. Try to get the highest score possible!")
            ]
            
            # Render text surfaces
            text_surfaces = [font.render(line, True, (255, 255, 255)) 
                            for line in help_text]
            
            # Calculate panel size
            padding = 20
            spacing = 10
            total_height = sum(t.get_height() + spacing for t in text_surfaces) + padding * 2
            max_width = max(t.get_width() for t in text_surfaces) + padding * 2
            
            # Draw panel
            panel = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
            panel.fill((80, 80, 120, 230))
            pygame.draw.rect(panel, (200, 200, 200), (0, 0, max_width, total_height), 3)
            
            # Position and draw
            panel_x = (screen.get_width() - max_width) // 2
            panel_y = (screen.get_height() - total_height) // 2
            screen.blit(panel, (panel_x, panel_y))
            
            # Draw text
            y_offset = panel_y + padding
            for text in text_surfaces:
                text_x = panel_x + (max_width - text.get_width()) // 2
                screen.blit(text, (text_x, y_offset))
                y_offset += text.get_height() + spacing

    def run(self):
        """Main game loop."""
        pygame.init()
        
        # Initialize fonts and help system
        self.help_font = pygame.font.Font(None, 36)
        
        # Main game loop
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle GTK events for Sugar integration
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            dt = clock.tick(60)  # 60 FPS
            
            # Handle events
            self.check_events()
            
            # Draw everything
            if hasattr(self, 'game') and self.game:
                self.game.update(dt)
                
            # Draw help if shown
            if hasattr(self, 'show_help') and self.show_help:
                self.draw_help(pygame.display.get_surface())
            
            pygame.display.flip()

        # Clean up
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    game_instance = main(journal=False)
    game_instance.run()