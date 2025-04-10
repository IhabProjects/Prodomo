#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime
from colorama import init, Fore, Back, Style
import pyfiglet
from art import text2art
from timer import Timer
from ui import UI
from task import TaskManager
from stats import Statistics
from config import Config
from user_data import UserData
import select
import threading
from pynput import keyboard
import pyautogui
import pydirectinput

class ProdomoApp:
    def __init__(self):
        init()  # Initialize colorama
        self.config = Config()
        self.ui = UI()
        self.timer = Timer()
        self.user_data = UserData()
        self.task_manager = TaskManager(self.user_data)
        self.stats = Statistics()
        self.running = False
        self.current_session = 0
        self.total_sessions = 0
        self.experience_points = 0
        self.level = 1
        self.current_user = None
        self.last_level = 1
        self.nature_theme = {
            'seed': '🌱',
            'sprout': '🌿',
            'sapling': '🌳',
            'tree': '🌲',
            'forest': '🌳🌲🌳'
        }
        self.animations = {
            'growing': ['🌱', '🌿', '🌳', '🌲'],
            'working': ['🌱', '🌿', '🌳', '🌲'],
            'resting': ['💧', '💦', '🌊', '💧'],
            'recharging': ['☀️', '🌤️', '⛅', '☀️']
        }
        self.animation_frame = 0

    def _animate(self, animation_type, duration=0.5):
        """Display an animated sequence."""
        frames = self.animations[animation_type]
        for _ in range(2):  # Show animation twice
            for frame in frames:
                print(f"\r{frame}", end="", flush=True)
                time.sleep(duration / len(frames))
        print("\r", end="", flush=True)

    def display_welcome(self):
        """Display the welcome screen with epic story introduction."""
        self.ui.clear_screen()
        title = text2art("PRODOMO", font="block")
        print(Fore.CYAN + title)
        print("\nWelcome to the Garden of Productivity!")
        print("\nIn this mystical garden, every moment of focus plants a seed.")
        print("Every completed task waters the soil.")
        print("Every achievement makes the garden flourish.")
        print("\nYou are the Gardener of your own destiny.")
        print("Will you nurture your garden to greatness?")
        time.sleep(2)

    def get_username(self):
        """Get username from user and load/create user data."""
        while True:
            username = input("\nEnter your name, Gardener: ").strip()
            if username:
                user_data = self.user_data.get_or_create_user(username)
                self.level = user_data['level']
                self.last_level = self.level
                self.experience_points = user_data['experience']
                self.total_sessions = user_data['total_sessions']
                self.current_user = username
                return username
            print(Fore.RED + "Every Gardener needs a name. Please try again." + Style.RESET_ALL)

    def main_menu(self):
        """Display the main menu and handle user input."""
        while True:
            self.ui.display_menu()
            self._display_level_info()
            self._display_achievements()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.start_pomodoro()
            elif choice == '2':
                self.task_manager.manage_tasks(self.current_user)
            elif choice == '3':
                self.stats.display_statistics()
            elif choice == '4':
                self.config.show_settings()
            elif choice == '5':
                self.ui.display_help()
            elif choice == '6':
                self.quit_app()
                break
            else:
                print(Fore.RED + "⚠️ Invalid choice. Please try again." + Style.RESET_ALL)
                time.sleep(1)

    def _display_level_info(self):
        """Display current level and experience points with story elements."""
        user_data = self.user_data.get_user_stats()
        if user_data:
            print(Fore.YELLOW + "\nLevel: " + str(user_data['level']))
            print("Experience: " + str(user_data['experience']))
            print("Next Level: " + str(user_data['level'] * 100 - user_data['experience']) + " XP needed")
            streak = user_data.get('streak', 0)  # Safely get streak with default value
            print("Current Streak: " + str(streak) + " days" + Style.RESET_ALL)
            
            # Check for level up
            if user_data['level'] > self.last_level:
                self.ui.display_level_up(user_data['level'])
                self.last_level = user_data['level']
            
            # Display story progress
            self.ui.display_story_progress(user_data['level'], user_data['experience'])

    def _display_achievements(self):
        """Display unlocked achievements with stories."""
        user_data = self.user_data.get_user_stats()
        if user_data and 'achievements' in user_data:
            achievements = user_data['achievements']
            if achievements:
                print(Fore.CYAN + "\nAchievements:")
                print("-" * 50)
                for achievement_id, data in achievements.items():
                    achievement = self.user_data.achievements[achievement_id]
                    print(f"🏆 {achievement['name']}: {achievement['description']}")
                    self.ui.display_achievement_story(achievement_id)
                print("-" * 50 + Style.RESET_ALL)

    def start_pomodoro(self):
        """Start a Pomodoro session with story elements."""
        self.running = True
        self.current_session += 1
        
        while self.running:
            # Display active tasks
            active_tasks = self.task_manager.get_active_tasks(self.current_user)
            self.ui.display_tasks(active_tasks)
            
            # Work session
            self.ui.display_session_info("WORK", self.current_session)
            self.ui.display_session_commands()
            self.timer.start_work_session()
            self.user_data.update_user_stats("WORK", 25)
            
            # Handle session commands
            self._handle_session_commands(active_tasks)
            
            # Short break or long break
            if self.current_session % 4 == 0:
                self.ui.display_session_info("LONG BREAK", self.current_session)
                self.timer.start_long_break()
                self.user_data.update_user_stats("LONG_BREAK", 15)
            else:
                self.ui.display_session_info("SHORT BREAK", self.current_session)
                self.timer.start_short_break()
                self.user_data.update_user_stats("SHORT_BREAK", 5)
            
            self.total_sessions += 1
            
            # Display random quote
            self.ui.display_quote()
            
            # Check for new achievements
            user_data = self.user_data.get_user_stats()
            if user_data and 'achievements' in user_data:
                new_achievements = len(user_data['achievements'])
                if new_achievements > len(getattr(self, 'last_achievement_count', 0)):
                    print(Fore.GREEN + "\n🌟 New Achievement Unlocked! 🌟" + Style.RESET_ALL)
                    self.last_achievement_count = new_achievements
            
            # Ask if user wants to continue
            if not self.ask_to_continue():
                break

    def _handle_session_commands(self, active_tasks):
        """Handle commands during a session."""
        def input_thread():
            while self.timer.is_running:
                try:
                    # Check for key presses
                    if pydirectinput.keyDown('p'):
                        self.timer.pause()
                        time.sleep(0.2)  # Prevent multiple triggers
                    elif pydirectinput.keyDown('r'):
                        self.timer.resume()
                        time.sleep(0.2)
                    elif pydirectinput.keyDown('s'):
                        self.timer.stop()
                        break
                    elif pydirectinput.keyDown('t'):
                        self.ui.display_tasks(active_tasks)
                        time.sleep(0.2)
                    elif pydirectinput.keyDown('q'):
                        self.timer.stop()
                        self.running = False
                        break
                    elif pydirectinput.keyDown('h'):
                        self.ui.display_session_commands()
                        time.sleep(0.2)
                    elif pydirectinput.keyDown('1') and len(active_tasks) >= 1:
                        task_id = active_tasks[0]['id']
                        self.task_manager.complete_task(self.current_user, task_id)
                        self.user_data.update_tasks_completed()
                        active_tasks = self.task_manager.get_active_tasks(self.current_user)
                        self.ui.display_tasks(active_tasks)
                        time.sleep(0.2)
                    elif pydirectinput.keyDown('2') and len(active_tasks) >= 2:
                        task_id = active_tasks[1]['id']
                        self.task_manager.complete_task(self.current_user, task_id)
                        self.user_data.update_tasks_completed()
                        active_tasks = self.task_manager.get_active_tasks(self.current_user)
                        self.ui.display_tasks(active_tasks)
                        time.sleep(0.2)
                    elif pydirectinput.keyDown('3') and len(active_tasks) >= 3:
                        task_id = active_tasks[2]['id']
                        self.task_manager.complete_task(self.current_user, task_id)
                        self.user_data.update_tasks_completed()
                        active_tasks = self.task_manager.get_active_tasks(self.current_user)
                        self.ui.display_tasks(active_tasks)
                        time.sleep(0.2)
                except Exception as e:
                    print(f"Error handling key press: {e}")
                time.sleep(0.1)
        
        # Start input thread
        input_handler = threading.Thread(target=input_thread)
        input_handler.daemon = True
        input_handler.start()
        
        # Wait for timer to finish or be stopped
        while self.timer.is_running:
            time.sleep(0.1)
        
        # Clean up
        input_handler.join(timeout=0.1)

    def ask_to_continue(self):
        """Ask user if they want to continue with another session."""
        choice = input("\nContinue tending to your garden? (y/n): ").lower().strip()
        return choice == 'y'

    def quit_app(self):
        """Handle application exit with story elements."""
        user_data = self.user_data.get_user_stats()
        print(Fore.GREEN + "\nThank you for tending to your garden today!")
        print(f"\nYour Garden Stats:")
        print(f"🌱 Total Sessions: {user_data['total_sessions']}")
        print(f"🌿 Current Level: {user_data['level']}")
        print(f"🌳 Experience Points: {user_data['experience']}")
        print(f"🌲 Current Streak: {user_data['streak']} days")
        print("\nMay your garden continue to grow and flourish!")
        time.sleep(2)

def main():
    app = ProdomoApp()
    app.display_welcome()
    username = app.get_username()
    app.main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye, Gardener! May your garden continue to grow!")
        sys.exit(0) 