import re

class EquationValidator:
    """Validates mathematical equations."""
    
    def validate(self, equation, target):
        """Validate if equation equals target and is valid."""
        result = {
            'valid': False,
            'error': '',
            'value': None
        }
        
        # Remove spaces
        equation = equation.replace(" ", "")
        
        # Check if empty
        if not equation:
            result['error'] = "Equation is empty"
            return result
        
        # Check for invalid characters
        valid_chars = r'^[0-9+\-*/()\.]+$'
        if not re.match(valid_chars, equation):
            result['error'] = "Invalid characters in equation"
            return result
        
        # Check for balanced parentheses
        if not self.check_balanced_parentheses(equation):
            result['error'] = "Unbalanced parentheses"
            return result
        
        # Check for valid operator placement
        if not self.check_valid_operators(equation):
            result['error'] = "Invalid operator placement"
            return result
        
        # Try to evaluate
        try:
            value = eval(equation)
            result['value'] = value
            
            # Check if equals target (allow for floating point)
            if abs(value - target) < 0.0001:
                result['valid'] = True
            else:
                result['error'] = f"Equals {value:.2f}, not {target}"
        except ZeroDivisionError:
            result['error'] = "Division by zero"
        except Exception:
            result['error'] = "Invalid equation"
        
        return result
    
    def check_balanced_parentheses(self, equation):
        """Check if parentheses are balanced."""
        count = 0
        for char in equation:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            if count < 0:
                return False
        return count == 0
    
    def check_valid_operators(self, equation):
        """Check for valid operator placement."""
        # Can't start or end with operator (except minus at start)
        if equation[0] in '+*/':
            return False
        if equation[-1] in '+-*/.':
            return False
        
        # Check for consecutive operators
        operators = '+-*/'
        for i in range(len(equation) - 1):
            if equation[i] in operators and equation[i+1] in operators:
                # Allow for negative numbers after operators
                if not (equation[i+1] == '-' and equation[i] in '+-*/('):
                    return False
        
        # Check for decimal point validity
        parts = equation.split('.')
        if len(parts) > 2:
            # Check each potential decimal number
            for i in range(1, len(parts)):
                # Must have digits before and after decimal
                if i >= len(parts) or not parts[i-1] or not parts[i]:
                    return False
                if not parts[i-1][-1].isdigit() or not parts[i][0].isdigit():
                    return False
        
        return True
    
    def are_equations_equivalent(self, eq1, eq2):
        """Check if two equations are essentially the same."""
        # Normalize equations
        eq1 = eq1.replace(" ", "")
        eq2 = eq2.replace(" ", "")
        
        # Direct comparison
        if eq1 == eq2:
            return True
        
        # Check if they evaluate to the same expression
        try:
            # Simple check for now - could be enhanced
            return eval(eq1) == eval(eq2) and len(eq1) == len(eq2)
        except:
            return False