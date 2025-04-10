import json
import os
from colorama import Fore, Style
from ui import UI

class Config:
    def __init__(self):
        self.config_file = "config.json"
        self.ui = UI()
        self.default_config = {
            'work_duration': 25,  # minutes
            'short_break_duration': 5,  # minutes
            'long_break_duration': 15,  # minutes
            'sessions_before_long_break': 4,
            'enable_notifications': True,
            'enable_sound': True,
            'color_scheme': {
                'work': 'green',
                'short_break': 'blue',
                'long_break': 'cyan',
                'menu': 'yellow',
                'error': 'red',
                'success': 'green'
            }
        }
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from the JSON file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.default_config
        return self.default_config

    def save_config(self):
        """Save configuration to the JSON file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def show_settings(self):
        """Display and manage settings."""
        while True:
            self.ui.clear_screen()
            print("\nSettings:")
            print("=" * 50)
            print(f"1. Work Duration: {self.config['work_duration']} minutes")
            print(f"2. Short Break Duration: {self.config['short_break_duration']} minutes")
            print(f"3. Long Break Duration: {self.config['long_break_duration']} minutes")
            print(f"4. Sessions Before Long Break: {self.config['sessions_before_long_break']}")
            print(f"5. Enable Notifications: {'Yes' if self.config['enable_notifications'] else 'No'}")
            print(f"6. Enable Sound: {'Yes' if self.config['enable_sound'] else 'No'}")
            print("7. Color Scheme")
            print("8. Reset to Default")
            print("9. Back to Main Menu")
            
            choice = self.ui.get_user_input("\nEnter your choice: ")
            
            if choice == '1':
                self._set_duration('work_duration')
            elif choice == '2':
                self._set_duration('short_break_duration')
            elif choice == '3':
                self._set_duration('long_break_duration')
            elif choice == '4':
                self._set_sessions_before_long_break()
            elif choice == '5':
                self._toggle_setting('enable_notifications')
            elif choice == '6':
                self._toggle_setting('enable_sound')
            elif choice == '7':
                self._manage_color_scheme()
            elif choice == '8':
                self._reset_to_default()
            elif choice == '9':
                break
            else:
                self.ui.display_error("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

    def _set_duration(self, setting_name):
        """Set duration for a specific setting."""
        try:
            value = int(self.ui.get_user_input(f"Enter new {setting_name.replace('_', ' ')} (minutes): "))
            if value > 0:
                self.config[setting_name] = value
                self.save_config()
                self.ui.display_success("Setting updated successfully!")
            else:
                self.ui.display_error("Duration must be greater than 0.")
        except ValueError:
            self.ui.display_error("Please enter a valid number.")

    def _set_sessions_before_long_break(self):
        """Set the number of sessions before a long break."""
        try:
            value = int(self.ui.get_user_input("Enter number of sessions before long break: "))
            if value > 0:
                self.config['sessions_before_long_break'] = value
                self.save_config()
                self.ui.display_success("Setting updated successfully!")
            else:
                self.ui.display_error("Number of sessions must be greater than 0.")
        except ValueError:
            self.ui.display_error("Please enter a valid number.")

    def _toggle_setting(self, setting_name):
        """Toggle a boolean setting."""
        self.config[setting_name] = not self.config[setting_name]
        self.save_config()
        status = "enabled" if self.config[setting_name] else "disabled"
        self.ui.display_success(f"Setting {status} successfully!")

    def _manage_color_scheme(self):
        """Manage color scheme settings."""
        while True:
            self.ui.clear_screen()
            print("\nColor Scheme Settings:")
            print("=" * 50)
            for i, (key, value) in enumerate(self.config['color_scheme'].items(), 1):
                print(f"{i}. {key.replace('_', ' ').title()}: {value}")
            print(f"{len(self.config['color_scheme']) + 1}. Back to Settings")
            
            choice = self.ui.get_user_input("\nEnter your choice: ")
            
            if choice.isdigit() and 1 <= int(choice) <= len(self.config['color_scheme']):
                color_key = list(self.config['color_scheme'].keys())[int(choice) - 1]
                new_color = self.ui.get_user_input(f"Enter new color for {color_key.replace('_', ' ')}: ").lower()
                self.config['color_scheme'][color_key] = new_color
                self.save_config()
                self.ui.display_success("Color updated successfully!")
            elif choice == str(len(self.config['color_scheme']) + 1):
                break
            else:
                self.ui.display_error("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

    def _reset_to_default(self):
        """Reset all settings to default values."""
        self.config = self.default_config.copy()
        self.save_config()
        self.ui.display_success("Settings reset to default successfully!") 