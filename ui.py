import os
import time
from colorama import Fore, Style, init
from art import text2art

class UI:
    def __init__(self):
        init()
        self.colors = {
            'primary': Fore.CYAN,
            'secondary': Fore.YELLOW,
            'success': Fore.GREEN,
            'error': Fore.RED,
            'info': Fore.BLUE,
            'reset': Style.RESET_ALL
        }
        self.symbols = {
            'work': '🌱',
            'break': '💧',
            'long_break': '☀️',
            'task': '📝',
            'stats': '📊',
            'settings': '⚙️',
            'help': '❓',
            'exit': '🚪',
            'secret': '🔮',
            'quote': '💭',
            'story': '📖',
            'achievement': '🏆',
            'level_up': '✨'
        }
        self.quotes = [
            "The secret of getting ahead is getting started.",
            "Productivity is never an accident. It is always the result of a commitment to excellence.",
            "The way to get started is to quit talking and begin doing.",
            "Focus on being productive instead of busy.",
            "Your future is created by what you do today, not tomorrow.",
            "The only limit to the height of your achievements is the reach of your dreams.",
            "Success is the sum of small efforts, repeated day in and day out.",
            "The key is not to prioritize what's on your schedule, but to schedule your priorities.",
            "You don't have to be great to start, but you have to start to be great.",
            "The expert in anything was once a beginner."
        ]
        self.secrets = {
            5: "🌱 You've discovered the first secret: The power of consistency!",
            10: "🌿 You've unlocked the second secret: Small steps lead to big changes!",
            15: "🌳 You've found the third secret: Growth happens in the quiet moments!",
            20: "🌲 You've revealed the fourth secret: Your potential is limitless!",
            25: "🌳🌲🌳 You've uncovered the final secret: You are the gardener of your own success!"
        }
        self.story_chapters = {
            1: {
                'title': "The Seed of Potential",
                'description': "In the beginning, there was a seed. A tiny spark of potential waiting to be nurtured. This is where your journey begins.",
                'milestone': "🌱 You've planted your first seed of productivity!",
                'reward': "Unlocked: Basic Focus Abilities"
            },
            3: {
                'title': "The First Sprouts",
                'description': "Your dedication begins to show. Small green shoots emerge from the soil, reaching for the light of knowledge.",
                'milestone': "🌿 Your focus is beginning to grow...",
                'reward': "Unlocked: Enhanced Concentration"
            },
            7: {
                'title': "Roots of Discipline",
                'description': "Deep beneath the surface, strong roots take hold. Your discipline grows stronger with each session.",
                'milestone': "🌳 You're developing strong roots of discipline!",
                'reward': "Unlocked: Advanced Time Management"
            },
            12: {
                'title': "The Flourishing Tree",
                'description': "Your tree of productivity stands tall, its branches reaching for the sky. Others begin to notice your growth.",
                'milestone': "🌲 Your productivity tree is flourishing!",
                'reward': "Unlocked: Master Focus Techniques"
            },
            18: {
                'title': "The Forest of Achievement",
                'description': "What started as a single seed has grown into a magnificent forest. Your achievements create an ecosystem of success.",
                'milestone': "🌳🌲🌳 You've created a forest of achievements!",
                'reward': "Unlocked: Legendary Productivity"
            },
            25: {
                'title': "The Garden of Mastery",
                'description': "You have become the master of your own garden. Every plant, every tree, every achievement is a testament to your journey.",
                'milestone': "🌳🌲🌳 You've achieved mastery over your productivity garden!",
                'reward': "Unlocked: Ultimate Focus Mastery"
            }
        }
        self.achievement_stories = {
            'first_session': {
                'title': "The First Step",
                'story': "Every great journey begins with a single step. You've taken yours, planting the first seed in your garden of productivity.",
                'reward': "Unlocked: Basic Gardening Tools"
            },
            'task_master': {
                'title': "The Task Gardener",
                'story': "Like a skilled gardener tending to their plants, you've mastered the art of task management. Your garden grows more organized with each completed task.",
                'reward': "Unlocked: Advanced Task Management"
            },
            'focus_expert': {
                'title': "The Focus Sage",
                'story': "Through dedication and practice, you've become a sage of focus. Your ability to concentrate is now legendary in the garden.",
                'reward': "Unlocked: Focus Mastery Techniques"
            },
            'early_bird': {
                'title': "The Dawn Gardener",
                'story': "You've discovered the magic of early mornings. The garden is most peaceful at dawn, and you've learned to harness this quiet power.",
                'reward': "Unlocked: Morning Productivity Boost"
            },
            'night_owl': {
                'title': "The Moonlight Gardener",
                'story': "While others sleep, you tend to your garden under the moonlight. The night has become your ally in productivity.",
                'reward': "Unlocked: Nighttime Focus Enhancement"
            },
            'consistency': {
                'title': "The Consistent Gardener",
                'story': "Day after day, you've shown up for your garden. Your consistency has created a rhythm that keeps everything growing.",
                'reward': "Unlocked: Daily Growth Bonus"
            },
            'productivity_guru': {
                'title': "The Garden Master",
                'story': "You have achieved the highest level of gardening mastery. Your garden is a testament to your dedication and skill.",
                'reward': "Unlocked: Ultimate Gardening Powers"
            }
        }

    def get_user_input(self, prompt):
        """Get user input with a styled prompt."""
        return input(f"{self.colors['primary']}{prompt}{self.colors['reset']}")

    def display_quote(self):
        """Display a random motivational quote."""
        import random
        quote = random.choice(self.quotes)
        print(f"\n{self.colors['secondary']}{self.symbols['quote']} {quote}{self.colors['reset']}\n")

    def display_secret(self, level):
        """Display a secret message when reaching certain levels."""
        if level in self.secrets:
            print(f"\n{self.colors['info']}{self.symbols['secret']} {self.secrets[level]}{self.colors['reset']}\n")
            time.sleep(2)

    def display_story_progress(self, level, experience):
        """Display story progress with rich narrative."""
        if level in self.story_chapters:
            chapter = self.story_chapters[level]
            print(f"\n{self.colors['primary']}{'=' * 50}")
            print(f"{self.symbols['story']} Chapter {level}: {chapter['title']}")
            print(f"{'=' * 50}{self.colors['reset']}")
            print(f"\n{self.colors['info']}{chapter['description']}{self.colors['reset']}")
            print(f"\n{self.colors['success']}{chapter['milestone']}{self.colors['reset']}")
            print(f"{self.colors['secondary']}{chapter['reward']}{self.colors['reset']}")
            time.sleep(2)

    def display_achievement_story(self, achievement_id):
        """Display achievement story with rich narrative."""
        if achievement_id in self.achievement_stories:
            achievement = self.achievement_stories[achievement_id]
            print(f"\n{self.colors['primary']}{'=' * 50}")
            print(f"{self.symbols['achievement']} Achievement: {achievement['title']}")
            print(f"{'=' * 50}{self.colors['reset']}")
            print(f"\n{self.colors['info']}{achievement['story']}{self.colors['reset']}")
            print(f"\n{self.colors['success']}{achievement['reward']}{self.colors['reset']}")
            time.sleep(2)

    def display_level_up(self, new_level):
        """Display level up animation and story."""
        print(f"\n{self.colors['primary']}{'=' * 50}")
        print(f"{self.symbols['level_up']} LEVEL UP! {self.symbols['level_up']}")
        print(f"{'=' * 50}{self.colors['reset']}")
        self._animate('growing')
        time.sleep(1)

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self, title):
        """Display a minimalistic header."""
        self.clear_screen()
        print(f"\n{self.colors['primary']}{'=' * 50}")
        print(f"{title.center(50)}")
        print(f"{'=' * 50}{self.colors['reset']}\n")

    def display_menu(self):
        """Display the main menu with minimalistic design."""
        self.display_header("PRODOMO")
        print(f"{self.colors['primary']}1. {self.symbols['work']} Start Focus Session")
        print(f"2. {self.symbols['task']} Manage Tasks")
        print(f"3. {self.symbols['stats']} View Statistics")
        print(f"4. {self.symbols['settings']}  Settings")
        print(f"5. {self.symbols['help']} Help")
        print(f"6. {self.symbols['exit']} Exit{self.colors['reset']}")

    def display_session_info(self, session_type, session_number):
        """Display session information with minimalistic design."""
        self.clear_screen()
        symbol = self.symbols['work'] if session_type == "WORK" else (
            self.symbols['long_break'] if session_type == "LONG BREAK" else self.symbols['break']
        )
        print(f"\n{self.colors['primary']}{symbol} Session {session_number}: {session_type}")
        print(f"{'=' * 50}{self.colors['reset']}\n")

    def display_tasks(self, tasks):
        """Display tasks in a minimalistic format."""
        if not tasks:
            print(f"\n{self.colors['info']}No tasks available.{self.colors['reset']}")
            return
        
        print(f"\n{self.colors['primary']}Active Tasks:")
        print(f"{'-' * 50}{self.colors['reset']}")
        for task in tasks:
            status = "✓" if task['completed'] else " "
            print(f"[{status}] {task['id']}. {task['name']}")
        print(f"{self.colors['primary']}{'-' * 50}{self.colors['reset']}")

    def display_help(self):
        """Display help information with minimalistic design."""
        self.display_header("HELP")
        print(f"{self.colors['info']}Session Commands:")
        print(f"{self.colors['secondary']}p{self.colors['reset']} - Pause session")
        print(f"{self.colors['secondary']}r{self.colors['reset']} - Resume session")
        print(f"{self.colors['secondary']}s{self.colors['reset']} - Stop session")
        print(f"{self.colors['secondary']}t{self.colors['reset']} - Toggle task completion")
        print(f"{self.colors['secondary']}q{self.colors['reset']} - Quit to main menu")
        print(f"\n{self.colors['info']}Task Management:")
        print(f"{self.colors['secondary']}1-9{self.colors['reset']} - Complete task with ID")
        print(f"\n{self.colors['info']}Press Enter to continue...{self.colors['reset']}")
        input()

    def display_session_commands(self):
        """Display available commands during a session."""
        print(f"\n{self.colors['info']}Commands: p(pause) r(resume) s(stop) t(tasks) q(quit){self.colors['reset']}")

    def display_success(self, message):
        """Display a success message."""
        print(f"\n{self.colors['success']}✓ {message}{self.colors['reset']}")

    def display_error(self, message):
        """Display an error message."""
        print(f"\n{self.colors['error']}✗ {message}{self.colors['reset']}")

    def display_progress(self, progress, total):
        """Display a minimalistic progress bar."""
        width = 30
        filled = int(width * progress / total)
        bar = '█' * filled + '░' * (width - filled)
        print(f"\r[{bar}] {progress}/{total}", end="", flush=True)

    def _animate(self, animation_type, duration=0.5):
        """Display an animated sequence."""
        animations = {
            'growing': ['🌱', '🌿', '🌳', '🌲'],
            'working': ['🌱', '🌿', '🌳', '🌲'],
            'resting': ['💧', '💦', '🌊', '💧'],
            'recharging': ['☀️', '🌤️', '⛅', '☀️']
        }
        
        frames = animations[animation_type]
        for _ in range(2):  # Show animation twice
            for frame in frames:
                print(f"\r{frame}", end="", flush=True)
                time.sleep(duration / len(frames))
        print("\r", end="", flush=True) 