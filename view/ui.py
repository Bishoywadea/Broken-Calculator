import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class CalculatorUI:
    """
    This class is responsible for building the GTK user interface components
    for the Broken Calculator activity, *excluding* the toolbar.

    It holds references to all widgets that need to be dynamically updated
    by the main activity logic.
    """
    def __init__(self):
        # --- Publicly accessible widgets ---
        self.main_grid = None
        self.equation_display = None
        self.target_label = None
        self.score_label = None
        self.equations_vbox = None
        self.buttons = {}

        # --- Build the UI ---
        self._setup_styling()
        self._build_ui()

    def _setup_styling(self):
        """Loads and applies our custom CSS for the activity."""
        css_provider = Gtk.CssProvider()
        css = b"""
        /* Main window background */
        #main_window {
            background-color: #1e1e1e; /* A very dark grey/black */
        }
        
        /* Calculator Display Style */
        #display_frame {
            background-color: #f0f0f0;
            border-radius: 12px;
            border: none;
            padding: 5px;
        }
        #equation_display {
            color: #2e2e2e;
            background-color: #f0f0f0;
            font-size: 36pt;
            font-weight: bold;
        }
        
        /* General Button Style */
        button {
            border: none;
            border-radius: 12px;
            font-size: 20pt;
            font-weight: bold;
            color: white;
            transition: all 0.1s ease-in-out;
        }
        
        button:hover {
             background-image: image(rgba(255, 255, 255, 0.1));
        }

        button:active {
             background-image: image(rgba(0, 0, 0, 0.1));
        }

        /* Number Buttons - Medium Grey */
        .btn-num {
            background-color: #505050;
        }

        /* Operator/Function Buttons - Dark Grey */
        .btn-op {
            background-color: #333333;
        }

        /* Clear/Equals Buttons - Light Grey */
        .btn-clear {
            background-color: #d4d4d2;
            color: black;
        }
        
        button:disabled {
            background-color: #404040;
            color: #707070;
            text-decoration-line: line-through;
        }

        button.broken {
            background-color: #5d1a1a; /* Dark red */
            color: #ab9393; /* Muted text color */
            border: 2px solid #ff4d4d; /* Red border */
            text-decoration-line: line-through;
        }
        
        /* Game Info Panel on the right */
        #game_info_panel {
            background-color: #e0e0e0;
            border-radius: 12px;
            padding: 15px;
        }
        
        .title-label {
            font-size: 18pt;
            font-weight: bold;
            color: #333;
        }
        
        #target_label {
            font-size: 48pt;
            font-weight: bold;
            color: #000;
        }
        
        #score_label {
            font-size: 24pt;
            color: #4CAF50; /* Green color for score */
        }
        
        .equation-entry {
            font-size: 12pt;
            color: #555;
        }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _build_ui(self):
        """Creates the main UI based on the original Calculate activity layout."""
        self.main_grid = Gtk.Grid()
        self.main_grid.set_name("main_window") # For CSS styling
        self.main_grid.set_column_spacing(20)
        self.main_grid.set_row_spacing(10)
        self.main_grid.set_border_width(20)

        # --- LEFT SIDE: The Calculator (Takes up ~60% of width) ---
        left_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_grid.attach(left_vbox, 0, 0, 2, 1)

        self.equation_display = Gtk.Label(label="0")
        self.equation_display.set_name("equation_display")
        self.equation_display.set_halign(Gtk.Align.END)
        self.equation_display.set_valign(Gtk.Align.CENTER)

        display_frame = Gtk.Frame()
        display_frame.set_name("display_frame")
        display_frame.add(self.equation_display)
        left_vbox.pack_start(display_frame, False, False, 10)

        self._build_calculator_pad(left_vbox)

        # --- RIGHT SIDE: Game Information (Takes up ~40% of width) ---
        right_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        right_vbox.set_name("game_info_panel")
        self.main_grid.attach(right_vbox, 2, 0, 1, 1)

        target_title = Gtk.Label(label="Target")
        target_title.get_style_context().add_class("title-label")

        self.target_label = Gtk.Label()
        self.target_label.set_name("target_label")

        score_title = Gtk.Label(label="Total Score")
        score_title.get_style_context().add_class("title-label")

        self.score_label = Gtk.Label()
        self.score_label.set_name("score_label")

        equations_title = Gtk.Label(label="Your Equations")
        equations_title.get_style_context().add_class("title-label")

        self.equations_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        right_vbox.pack_start(target_title, False, False, 0)
        right_vbox.pack_start(self.target_label, False, False, 10)
        right_vbox.pack_start(Gtk.Separator(), False, False, 10)
        right_vbox.pack_start(score_title, False, False, 0)
        right_vbox.pack_start(self.score_label, False, False, 10)
        right_vbox.pack_start(Gtk.Separator(), False, False, 10)
        right_vbox.pack_start(equations_title, False, False, 0)
        right_vbox.pack_start(self.equations_vbox, True, True, 0)

    def _build_calculator_pad(self, parent_box):
        """Creates and lays out the calculator buttons with complex sizes."""
        pad_grid = Gtk.Grid()
        pad_grid.set_row_spacing(8)
        pad_grid.set_column_spacing(8)
        pad_grid.set_vexpand(True)
        pad_grid.set_hexpand(True)
        parent_box.pack_start(pad_grid, True, True, 0)

        button_layout = [
            ['C', 'C', 0, 0, 2, 1, 'btn-clear'], ['⌫', 'backspace', 2, 0, 2, 1, 'btn-op'],
            ['7', '7', 0, 1, 1, 1, 'btn-num'], ['8', '8', 1, 1, 1, 1, 'btn-num'], ['9', '9', 2, 1, 1, 1, 'btn-num'], ['÷', '/', 3, 1, 1, 1, 'btn-op'],
            ['4', '4', 0, 2, 1, 1, 'btn-num'], ['5', '5', 1, 2, 1, 1, 'btn-num'], ['6', '6', 2, 2, 1, 1, 'btn-num'], ['×', '*', 3, 2, 1, 1, 'btn-op'],
            ['1', '1', 0, 3, 1, 1, 'btn-num'], ['2', '2', 1, 3, 1, 1, 'btn-num'], ['3', '3', 2, 3, 1, 1, 'btn-num'], ['-', '-', 3, 3, 1, 1, 'btn-op'],
            ['0', '0', 0, 4, 2, 1, 'btn-num'], ['.', '.', 2, 4, 1, 1, 'btn-num'], ['+', '+', 3, 4, 1, 1, 'btn-op'],
            ['(', '(', 0, 5, 1, 1, 'btn-op'], [')', ')', 1, 5, 1, 1, 'btn-op'], ['=', '=', 2, 5, 2, 1, 'btn-clear']
        ]

        for (text, value, c, r, w, h, style) in button_layout:
            button = Gtk.Button(label=text)
            button.set_hexpand(True)
            button.set_vexpand(True)
            button.get_style_context().add_class(style)

            button.game_value = value
            
            pad_grid.attach(button, c, r, w, h)
            self.buttons[value] = button