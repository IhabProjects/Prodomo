import time
import threading
import os
from colorama import Fore, Style
import sys
from config import Config

class Timer:
    def __init__(self):
        self.config = Config()
        self.work_duration = self.config.config['work_duration'] * 60  # Convert to seconds
        self.short_break_duration = self.config.config['short_break_duration'] * 60
        self.long_break_duration = self.config.config['long_break_duration'] * 60
        self.remaining_time = 0
        self.is_running = False
        self.is_paused = False
        self.current_session = None
        self.nature_symbols = {
            'work': '🌱',
            'short_break': '💧',
            'long_break': '☀️',
            'growing': '🌱',
            'resting': '💧'
        }
        self.animations = {
            'growing': ['🌱', '🌿', '🌳', '🌲'],
            'working': ['🌱', '🌿', '🌳', '🌲'],
            'resting': ['💧', '💦', '🌊', '💧'],
            'recharging': ['☀️', '🌤️', '⛅', '☀️']
        }

    def _animate(self, animation_type, duration=0.5):
        """Display an animated sequence."""
        frames = self.animations[animation_type]
        for _ in range(2):  # Show animation twice
            for frame in frames:
                print(f"\r{frame}", end="", flush=True)
                time.sleep(duration / len(frames))
        print("\r", end="", flush=True)

    def start_work_session(self):
        """Start a work session."""
        self.work_duration = self.config.config['work_duration'] * 60  # Update from config
        self._start_timer(self.work_duration, "WORK")
        self._animate('working')

    def start_short_break(self):
        """Start a short break."""
        self.short_break_duration = self.config.config['short_break_duration'] * 60  # Update from config
        self._start_timer(self.short_break_duration, "SHORT BREAK")
        self._animate('resting')

    def start_long_break(self):
        """Start a long break."""
        self.long_break_duration = self.config.config['long_break_duration'] * 60  # Update from config
        self._start_timer(self.long_break_duration, "LONG BREAK")
        self._animate('recharging')

    def _start_timer(self, duration, session_type):
        """Start the timer with the specified duration and session type."""
        self.remaining_time = duration
        self.current_session = session_type
        self.is_running = True
        self.is_paused = False
        self._countdown()

    def _countdown(self):
        """Handle the countdown logic."""
        while self.remaining_time > 0 and self.is_running:
            if not self.is_paused:
                self._display_time()
                time.sleep(1)
                self.remaining_time -= 1
            else:
                time.sleep(0.1)
        
        if self.remaining_time == 0:
            self._notify_completion()

    def _display_time(self):
        """Display the current time with a nature-themed progress bar."""
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        progress = 1 - (self.remaining_time / (self.work_duration if self.current_session == "WORK" else 
                                             self.short_break_duration if self.current_session == "SHORT BREAK" else 
                                             self.long_break_duration))
        
        symbol = self.nature_symbols['growing' if self.current_session == "WORK" else 'resting']
        filled_length = int(30 * progress)
        bar = symbol * filled_length + '░' * (30 - filled_length)
        
        print(f"\r[{bar}] {minutes:02d}:{seconds:02d}", end="", flush=True)

    def _notify_completion(self):
        """Display a completion message with nature-themed notification."""
        print("\n")
        if self.current_session == "WORK":
            print(f"{Fore.GREEN}✨ Focus session completed! Time to rest and recharge.{Style.RESET_ALL}")
            self._animate('resting')
        else:
            print(f"{Fore.CYAN}✨ Break time is over! Ready to grow your focus again.{Style.RESET_ALL}")
            self._animate('working')
        print("\a")  # Terminal bell sound

    def pause(self):
        """Pause the timer."""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            print(f"\n{Fore.YELLOW}⏸️ Timer paused{Style.RESET_ALL}")

    def resume(self):
        """Resume the timer."""
        if self.is_running and self.is_paused:
            self.is_paused = False
            print(f"\n{Fore.GREEN}▶️ Timer resumed{Style.RESET_ALL}")

    def stop(self):
        """Stop the timer."""
        self.is_running = False
        print(f"\n{Fore.RED}⏹️ Timer stopped{Style.RESET_ALL}") 