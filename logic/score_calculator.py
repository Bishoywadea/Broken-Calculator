class ScoreCalculator:
    """Calculates scores for equations based on complexity."""
    
    def calculate_score(self, equation):
        """Calculate score for an equation."""
        score = 10  # Base score
        
        # Remove spaces
        equation = equation.replace(" ", "")
        
        # Bonus for each operator
        operators = ['+', '-', '*', '/']
        operator_count = sum(equation.count(op) for op in operators)
        score += operator_count * 5
        
        # Extra bonus for multiplication and division
        score += equation.count('*') * 3
        score += equation.count('/') * 3
        
        # Bonus for parentheses
        score += equation.count('(') * 10
        
        # Bonus for equation length
        score += min(len(equation) // 3, 20)
        
        # Bonus for using different operators
        unique_operators = sum(1 for op in operators if op in equation)
        if unique_operators >= 3:
            score += 15
        elif unique_operators >= 2:
            score += 10
        
        # Bonus for numbers with multiple digits
        numbers = self.extract_numbers(equation)
        for num in numbers:
            if len(num) > 1:
                score += len(num) * 2
        
        return score
    
    def extract_numbers(self, equation):
        """Extract all numbers from equation."""
        numbers = []
        current_num = ""
        
        for char in equation:
            if char.isdigit():
                current_num += char
            else:
                if current_num:
                    numbers.append(current_num)
                    current_num = ""
        
        if current_num:
            numbers.append(current_num)
        
        return numbers