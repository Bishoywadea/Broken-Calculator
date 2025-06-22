
import random
from logic.equation_validator import EquationValidator
from logic.score_calculator import ScoreCalculator
from logic.broken_button_validator import BrokenButtonValidator

class GameManager:
    def __init__(self):
        # Game logic components
        self.equation_validator = EquationValidator()
        self.score_calculator = ScoreCalculator()
        self.broken_validator = BrokenButtonValidator()
        
        # Game state variables
        self.target_number = 0
        self.difficulty = "none"
        self.equations = []
        self.current_equation = ""
        self.total_score = 0
        self.game_completed = False
        self.broken_buttons = []
        
    def start_level(self, difficulty):
        """Start a new game with selected difficulty. This now only sets up data."""
        self.difficulty = difficulty
        
        # Generate target number based on difficulty
        if difficulty == "easy":
            self.target_number = random.randint(10, 50)
            broken_count = 3
        elif difficulty == "medium":
            self.target_number = random.randint(50, 100)
            broken_count = 5
        else:  # hard
            self.target_number = random.randint(100, 200)
            broken_count = 7
        
        # Generate broken buttons
        # Assuming generate_broken_buttons does not use Pygame
        self.broken_buttons = self.broken_validator.generate_broken_buttons(
            self.target_number, broken_count
        )
        
        # Reset game state data
        self.equations = []
        self.current_equation = ""
        self.total_score = 0
        self.game_completed = False

    def is_button_broken(self, value):
        """Check if a button is broken. This is pure logic, so it stays."""
        return value in self.broken_buttons
            
    def submit_equation(self):
        """
        Submit the current equation for validation.
        Returns None on success, or an error message string on failure.
        """
        if not self.current_equation.strip():
            return "Equation is empty." # Return error message
        
        # Convert display symbols back to Python operators for evaluation
        equation_for_eval = self.current_equation.replace("×", "*").replace("÷", "/")
        
        # Validate equation
        result = self.equation_validator.validate(equation_for_eval, self.target_number)
        
        if result['valid']:
            # Check if equation is unique
            if not self.is_equation_unique(equation_for_eval):
                return "Equation already used!" # Return error message
            
            # Calculate score
            score = self.score_calculator.calculate_score(equation_for_eval)
            
            # Add equation to list
            self.equations.append({
                'equation': self.current_equation,
                'score': score
            })
            
            self.total_score += score
            self.current_equation = ""
            
            # Check if game is complete
            if len(self.equations) >= 5:
                self.complete_game()
                
            return None # IMPORTANT: Return None for success
        else:
            return result['error'] # Return the error message from the validator

    def is_equation_unique(self, equation):
        """Check if equation is unique. This is pure logic, so it stays."""
        equation_normalized = equation.replace(" ", "")
        for eq in self.equations:
            # Assuming are_equations_equivalent does not use Pygame
            if self.equation_validator.are_equations_equivalent(
                equation_normalized, 
                eq['equation'].replace("×", "*").replace("÷", "/").replace(" ", "")
            ):
                return False
        return True

    def complete_game(self):
        """Handle game completion. This now only sets the state flag."""
        self.game_completed = True

    def write_file(filename):
        """Write game state to a file."""
        pass

    def read_file(filename):
        """Read game state from a file."""
        pass
