import json
import os
from datetime import datetime, timedelta
from ui import UI

class Statistics:
    def __init__(self):
        self.stats_file = "stats.json"
        self.ui = UI()
        self.stats = {
            'total_sessions': 0,
            'total_time': 0,
            'tasks_completed': 0,
            'daily_stats': {},
            'weekly_stats': {},
            'productivity_score': 0
        }
        self.load_stats()

    def load_stats(self):
        """Load statistics from the JSON file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except json.JSONDecodeError:
                self.stats = self._init_stats()

    def save_stats(self):
        """Save statistics to the JSON file."""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=4)

    def _init_stats(self):
        """Initialize statistics with default values."""
        return {
            'total_sessions': 0,
            'total_time': 0,
            'tasks_completed': 0,
            'daily_stats': {},
            'weekly_stats': {},
            'productivity_score': 0
        }

    def update_stats(self, session_count, session_type):
        """Update statistics after a session."""
        today = datetime.now().strftime('%Y-%m-%d')
        week = datetime.now().strftime('%Y-W%W')
        
        # Update daily stats
        if today not in self.stats['daily_stats']:
            self.stats['daily_stats'][today] = {
                'sessions': 0,
                'time': 0,
                'tasks_completed': 0
            }
        
        # Update weekly stats
        if week not in self.stats['weekly_stats']:
            self.stats['weekly_stats'][week] = {
                'sessions': 0,
                'time': 0,
                'tasks_completed': 0
            }
        
        # Update session counts
        self.stats['total_sessions'] += 1
        self.stats['daily_stats'][today]['sessions'] += 1
        self.stats['weekly_stats'][week]['sessions'] += 1
        
        # Update time (in minutes)
        time_spent = 25 if session_type == "work" else (15 if session_type == "long_break" else 5)
        self.stats['total_time'] += time_spent
        self.stats['daily_stats'][today]['time'] += time_spent
        self.stats['weekly_stats'][week]['time'] += time_spent
        
        # Calculate productivity score
        self._calculate_productivity_score()
        
        self.save_stats()

    def _calculate_productivity_score(self):
        """Calculate the overall productivity score."""
        if self.stats['total_sessions'] == 0:
            self.stats['productivity_score'] = 0
            return
        
        # Calculate based on completed tasks and time spent
        task_completion_rate = (self.stats['tasks_completed'] / self.stats['total_sessions']) * 100
        time_efficiency = min(100, (self.stats['total_time'] / (self.stats['total_sessions'] * 25)) * 100)
        
        self.stats['productivity_score'] = int((task_completion_rate + time_efficiency) / 2)

    def display_statistics(self):
        """Display the statistics menu and show statistics."""
        while True:
            self.ui.clear_screen()
            print("\nStatistics Options:")
            print("1. View Daily Statistics")
            print("2. View Weekly Statistics")
            print("3. View Overall Statistics")
            print("4. Back to Main Menu")
            
            choice = self.ui.get_user_input("\nEnter your choice: ")
            
            if choice == '1':
                self._display_daily_stats()
            elif choice == '2':
                self._display_weekly_stats()
            elif choice == '3':
                self._display_overall_stats()
            elif choice == '4':
                break
            else:
                self.ui.display_error("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

    def _display_daily_stats(self):
        """Display daily statistics."""
        self.ui.clear_screen()
        print("\nDaily Statistics:")
        print("=" * 50)
        for date, stats in sorted(self.stats['daily_stats'].items(), reverse=True):
            print(f"\nDate: {date}")
            print(f"Sessions: {stats['sessions']}")
            print(f"Time Spent: {stats['time']} minutes")
            print(f"Tasks Completed: {stats['tasks_completed']}")

    def _display_weekly_stats(self):
        """Display weekly statistics."""
        self.ui.clear_screen()
        print("\nWeekly Statistics:")
        print("=" * 50)
        for week, stats in sorted(self.stats['weekly_stats'].items(), reverse=True):
            print(f"\nWeek: {week}")
            print(f"Sessions: {stats['sessions']}")
            print(f"Time Spent: {stats['time']} minutes")
            print(f"Tasks Completed: {stats['tasks_completed']}")

    def _display_overall_stats(self):
        """Display overall statistics."""
        self.ui.clear_screen()
        print("\nOverall Statistics:")
        print("=" * 50)
        print(f"Total Sessions: {self.stats['total_sessions']}")
        print(f"Total Time Spent: {self.stats['total_time']} minutes")
        print(f"Total Tasks Completed: {self.stats['tasks_completed']}")
        print(f"Productivity Score: {self.stats['productivity_score']}%") 