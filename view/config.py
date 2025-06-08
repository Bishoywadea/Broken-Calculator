import pygame

class Config:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    
    # Theme setting
    DARK_THEME = False
    
    # Light theme colors
    LIGHT_COLORS = {
        'BACKGROUND': (240, 245, 255),
        'BORDER': (100, 100, 100),
        'UI_BACKGROUND': (240, 240, 240),
        'TEXT': (50, 50, 50),
        'TEXT_LIGHT': (100, 100, 100),
        'BUTTON_HOVER': (220, 220, 220),
        'SUCCESS': (50, 200, 50),
        'ERROR': (200, 50, 50),
        'EQUATION_BG': (250, 250, 250),
        'EQUATION_BORDER': (100, 100, 100),
        'TARGET_BG': (255, 230, 150),
        'SCORE_COLOR': (255, 215, 0),
        'CALCULATOR_BG': (255, 255, 255),
        'BUTTON_NORMAL': (250, 250, 250),
        'BUTTON_PRESSED': (200, 200, 200),
        'BUTTON_EQUALS': (255, 230, 230),
        'PANEL_BG': (250, 250, 250),
        'BUTTON_BROKEN': (200, 200, 200),
        'BUTTON_BROKEN_TEXT': (150, 150, 150),
    }
    
    # Dark theme colors
    DARK_COLORS = {
        'BACKGROUND': (35, 35, 40),
        'BORDER': (150, 150, 150),
        'UI_BACKGROUND': (60, 60, 70),
        'TEXT': (200, 200, 200),
        'TEXT_LIGHT': (150, 150, 150),
        'BUTTON_HOVER': (80, 80, 90),
        'SUCCESS': (50, 200, 50),
        'ERROR': (200, 50, 50),
        'EQUATION_BG': (50, 50, 60),
        'EQUATION_BORDER': (100, 100, 100),
        'TARGET_BG': (100, 80, 50),
        'SCORE_COLOR': (255, 215, 0),
        'CALCULATOR_BG': (45, 45, 55),
        'BUTTON_NORMAL': (70, 70, 80),
        'BUTTON_PRESSED': (50, 50, 60),
        'BUTTON_EQUALS': (100, 70, 70),
        'PANEL_BG': (50, 50, 60),
        'BUTTON_BROKEN': (40, 40, 50),
        'BUTTON_BROKEN_TEXT': (80, 80, 80),
    }
    
    @classmethod
    def get_colors(cls):
        """Get current theme colors."""
        return cls.DARK_COLORS if cls.DARK_THEME else cls.LIGHT_COLORS
    
    @classmethod
    def toggle_theme(cls):
        """Toggle between light and dark theme."""
        cls.DARK_THEME = not cls.DARK_THEME
    
    # Keep old COLORS for compatibility, will update in next commit
    COLORS = LIGHT_COLORS
    
    # UI Layout
    EQUATION_HEIGHT = 60
    EQUATION_MARGIN = 10
    BUTTON_SIZE = 80
    BUTTON_MARGIN = 10
    CALC_BUTTON_SIZE = 80
    CALC_BUTTON_SPACING = 10
    
    # Game Settings
    MAX_EQUATIONS = 5
    
    # Scoring
    SCORE_BASE = 10
    SCORE_OPERATOR_BONUS = 5
    SCORE_PARENTHESIS_BONUS = 10
    SCORE_LENGTH_BONUS = 2