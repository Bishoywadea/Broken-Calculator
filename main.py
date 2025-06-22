import pygame
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from sugar3.activity.activity import Activity
from logic.game_manager import GameManager
from view.ui import CalculatorUI
from gettext import gettext as _


class main:
    def __init__(self, journal=True):
        self.journal = journal
        self.running = True
        self.canvas = None
        self.game = None
        self.activity = None
        
    def set_activity(self, activity):
        """Set reference to the activity."""
        self.activity = activity
        if self.game:
            self.game.set_activity(activity)
    
    def set_canvas(self, canvas):
        self.canvas = canvas
        pygame.display.set_caption(_("Broken Calculator"))
    
    def quit(self):
        self.running = False
    
    def run(self):
        # Initialize pygame
        pygame.init()
        
        # Initialize the game manager
        self.game = GameManager()
        
        if self.activity:
            self.game.set_activity(self.activity)
        
        # Main loop for handling GTK events
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle GTK events for Sugar integration
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            clock.tick(30)  
        
        # Clean up
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game_instance = main(journal=False)
    game_instance.run()