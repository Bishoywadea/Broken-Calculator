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

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

import main as main
from logic.game_manager import GameManager
from view.ui import CalculatorUI
from gettext import gettext as _


class BrokenCalculator(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.main_instance = main.main()
        self.game = GameManager()

        self.ui = CalculatorUI()

        self.build_toolbar()

        self.set_canvas(self.ui.main_grid)
        self.main_instance.set_activity(self)

        self._connect_signals()
        self._on_new_game_clicked(None)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)

        new_game_button = Gtk.ToolButton(icon_name="view-refresh")
        new_game_button.set_tooltip_text("New Game")

        self.new_game_button = new_game_button
        toolbar_box.toolbar.insert(new_game_button, -1)

        help_button = Gtk.ToolButton(icon_name="help-about")
        help_button.set_tooltip_text("Help")
        help_button.connect("clicked", self._on_help_clicked)
        toolbar_box.toolbar.insert(help_button, -1)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)

    def _on_help_clicked(self, button):
        """Handle help button click."""
        if hasattr(self.main_instance, 'toggle_help'):
            self.main_instance.toggle_help()

    def _connect_signals(self):
        """Connects widget signals to their handler methods."""
        self.new_game_button.connect("clicked", self._on_new_game_clicked)

        # Connect all the calculator pad buttons from the UI instance
        for value, button in self.ui.buttons.items():
            button.connect("clicked", self._on_button_clicked)

    def _on_button_clicked(self, button):
        value = button.game_value
        if self.game.game_completed:
            return

        if value == "C":
            self.game.current_equation = ""
        elif value == "backspace":
            self.game.current_equation = self.game.current_equation[:-1]
        elif value == "=":
            error_message = self.game.submit_equation()
            if error_message:
                print(f"Error submitting equation: {error_message}")
                self._show_error_dialog(error_message)
        else:
            self.game.current_equation += value

        self._update_ui_from_gamestate()

    def _update_ui_from_gamestate(self):
        """Synchronizes the GTK view with the GameManager model."""
        # Update display with formatted equation
        display_text = (
            self.game.current_equation.replace("*", "×")
            .replace("/", "÷")
        )
        self.ui.equation_display.set_text(
            display_text if display_text else "0"
        )

        # Update game info using widgets from the ui object
        self.ui.target_label.set_text(str(self.game.target_number))
        self.ui.score_label.set_text(str(self.game.total_score))

        # Rebuild equations list
        for child in self.ui.equations_vbox.get_children():
            self.ui.equations_vbox.remove(child)

        for eq_data in self.game.equations:
            eq_text = (
                f"{eq_data['equation'].replace('*', '×').replace('/', '÷')} = "
                f"{self.game.target_number}"
            )
            score_markup = (
                f"<span color='#4CAF50' weight='bold'>"
                f"(+{eq_data['score']} pts)</span>"
            )

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            eq_label = Gtk.Label(label=eq_text)
            eq_label.get_style_context().add_class("equation-entry")
            score_label = Gtk.Label()
            score_label.set_markup(score_markup)

            hbox.pack_start(eq_label, True, True, 0)
            hbox.pack_end(score_label, False, False, 0)
            self.ui.equations_vbox.pack_start(hbox, False, False, 0)

        # Check for game completion
        if self.game.game_completed:
            self._show_completion_dialog()

        self.show_all()

    def _show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            parent=self.get_toplevel(),
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=_("Invalid Equation"),
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def _show_completion_dialog(self):
        dialog = Gtk.MessageDialog(
            parent=self.get_toplevel(),
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Excellent Work!"),
        )
        dialog.format_secondary_text(
            _("Final Score: {score}\n\nClick OK to start a new game.").format(
                score=self.game.total_score
            )
        )
        dialog.run()
        dialog.destroy()
        self._on_new_game_clicked(None)

    def _on_new_game_clicked(self, widget):
        """Starts a new game and resets the UI."""
        self.game.start_level()

        # Re-enable all buttons and then disable the broken for the new game
        for value, button in self.ui.buttons.items():
            button.set_sensitive(True)
            button.get_style_context().remove_class("broken")
        for broken_value in self.game.broken_buttons:
            if broken_value in self.ui.buttons:
                button = self.ui.buttons[broken_value]
                button.set_sensitive(False)
                button.get_style_context().add_class("broken")

        self._update_ui_from_gamestate()

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass
