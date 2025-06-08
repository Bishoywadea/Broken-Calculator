import pygame

class Config:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    
    COLORS = {
        'BACKGROUND': (35, 35, 40),  # Dark background
        'BORDER': (100, 100, 100),
        'UI_BACKGROUND': (240, 240, 240),
        'TEXT': (50, 50, 50),
        'TEXT_LIGHT': (200, 200, 200),
        'BUTTON_HOVER': (220, 220, 220),
        'SUCCESS': (50, 200, 50),
        'ERROR': (200, 50, 50),
        'EQUATION_BG': (250, 250, 250),
        'EQUATION_BORDER': (100, 100, 100),
        'TARGET_BG': (255, 230, 150),
        'SCORE_COLOR': (255, 215, 0),
        'CALCULATOR_BG': (240, 240, 240),
        'BUTTON_NORMAL': (250, 250, 250),
        'BUTTON_PRESSED': (200, 200, 200),
        'BUTTON_EQUALS': (255, 230, 230),
        'PANEL_BG': (250, 250, 250),
    }
    
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