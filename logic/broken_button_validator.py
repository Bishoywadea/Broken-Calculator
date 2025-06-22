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

import random


class BrokenButtonValidator:
    """Validates that a puzzle is solvable with broken buttons."""

    def generate_broken_buttons(self, target, count):
        """Generate broken buttons ensuring puzzle remains solvable."""
        all_buttons = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "+",
            "-",
            "*",
            "/",
            "(",
            ")",
        ]

        # Always ensure we have basic operators and some numbers
        required_working = set()

        # Need at least one way to make the target
        # For simplicity, ensure we can at least add/subtract to target
        if target <= 50:
            # For small targets, ensure we have enough small numbers
            required_working.update(["1", "+"])
        else:
            # For larger targets, ensure we have multiplication
            required_working.update(["2", "*", "+"])

        # Ensure we don't break too many critical buttons
        breakable = [b for b in all_buttons if b not in required_working]

        # Limit how many we can break
        max_breakable = min(count, len(breakable))

        # Randomly select buttons to break
        broken = random.sample(breakable, max_breakable)

        # Validate that we can still make 5 different equations
        if not self.validate_solvable(target, broken):
            # If not solvable, try again with fewer broken buttons
            return self.generate_broken_buttons(target, count - 1)

        return broken

    def validate_solvable(self, target, broken_buttons):
        """Check if target is achievable with broken buttons."""
        working_buttons = []
        all_buttons = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "+",
            "-",
            "*",
            "/",
            "(",
            ")",
        ]

        for button in all_buttons:
            if button not in broken_buttons:
                working_buttons.append(button)

        # Basic check: ensure we have at least some numbers and operators
        has_numbers = any(b.isdigit() for b in working_buttons)
        has_operators = any(b in "+-*/" for b in working_buttons)

        if not has_numbers or not has_operators:
            return False

        working_digits = [int(b) for b in working_buttons if b.isdigit()]

        if not working_digits:
            return False

        # Can we reach target with available numbers?
        # Simple check: can we add/multiply to get close?
        max_reachable = max(working_digits) * 10  # Rough estimate

        if "+" in working_buttons:
            max_reachable = sum(working_digits) * 5

        if "*" in working_buttons and len(working_digits) >= 2:
            max_reachable = max(max_reachable, max(working_digits) ** 2)

        return max_reachable >= target
