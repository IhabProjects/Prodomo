import json
import os
from datetime import datetime

class UserData:
    def __init__(self):
        self.data_file = "user_data.json"
        self.current_user = None
        self.user_data = self._load_data()
        self.achievements = {
            'first_session': {'name': 'First Step', 'description': 'Complete your first focus session', 'unlocked': False},
            'task_master': {'name': 'Task Master', 'description': 'Complete 10 tasks', 'unlocked': False},
            'focus_expert': {'name': 'Focus Expert', 'description': 'Complete 25 focus sessions', 'unlocked': False},
            'early_bird': {'name': 'Early Bird', 'description': 'Start a session before 8 AM', 'unlocked': False},
            'night_owl': {'name': 'Night Owl', 'description': 'Complete a session after 10 PM', 'unlocked': False},
            'consistency': {'name': 'Consistency', 'description': 'Complete sessions for 7 days in a row', 'unlocked': False},
            'productivity_guru': {'name': 'Productivity Guru', 'description': 'Reach level 20', 'unlocked': False}
        }

    def _load_data(self):
        """Load user data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_data(self):
        """Save user data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.user_data, f, indent=4)

    def get_or_create_user(self, username):
        """Get existing user data or create new user."""
        if username not in self.user_data:
            self.user_data[username] = {
                'created_at': datetime.now().isoformat(),
                'total_sessions': 0,
                'total_work_time': 0,
                'total_break_time': 0,
                'level': 1,
                'experience': 0,
                'last_session': None,
                'achievements': {},
                'streak': 0,
                'last_session_date': None,
                'tasks_completed': 0,
                'story_progress': 0
            }
        else:
            # Ensure all required fields exist for existing users
            user = self.user_data[username]
            required_fields = {
                'streak': 0,
                'last_session_date': None,
                'tasks_completed': 0,
                'story_progress': 0,
                'achievements': {}
            }
            for field, default_value in required_fields.items():
                if field not in user:
                    user[field] = default_value
        
        self.current_user = username
        self._save_data()
        return self.user_data[username]

    def update_user_stats(self, session_type, duration):
        """Update user statistics after a session."""
        if not self.current_user:
            return

        user = self.user_data[self.current_user]
        user['total_sessions'] += 1
        current_date = datetime.now().date().isoformat()
        
        # Update streak
        if user['last_session_date'] != current_date:
            if user['last_session_date'] and (datetime.fromisoformat(current_date) - datetime.fromisoformat(user['last_session_date'])).days == 1:
                user['streak'] += 1
            else:
                user['streak'] = 1
            user['last_session_date'] = current_date

        if session_type == "WORK":
            user['total_work_time'] += duration
            user['experience'] += 25
        else:
            user['total_break_time'] += duration
            user['experience'] += 5

        # Check for achievements
        self._check_achievements(user)

        # Level up if experience threshold is reached
        while user['experience'] >= user['level'] * 100:
            user['level'] += 1
            user['experience'] -= (user['level'] - 1) * 100
            user['story_progress'] += 1

        self._save_data()

    def _check_achievements(self, user):
        """Check and unlock achievements."""
        current_time = datetime.now()
        
        if user['total_sessions'] == 1 and 'first_session' not in user['achievements']:
            user['achievements']['first_session'] = {'unlocked_at': current_time.isoformat()}
        
        if user['tasks_completed'] >= 10 and 'task_master' not in user['achievements']:
            user['achievements']['task_master'] = {'unlocked_at': current_time.isoformat()}
        
        if user['total_sessions'] >= 25 and 'focus_expert' not in user['achievements']:
            user['achievements']['focus_expert'] = {'unlocked_at': current_time.isoformat()}
        
        if current_time.hour < 8 and 'early_bird' not in user['achievements']:
            user['achievements']['early_bird'] = {'unlocked_at': current_time.isoformat()}
        
        if current_time.hour >= 22 and 'night_owl' not in user['achievements']:
            user['achievements']['night_owl'] = {'unlocked_at': current_time.isoformat()}
        
        if user['streak'] >= 7 and 'consistency' not in user['achievements']:
            user['achievements']['consistency'] = {'unlocked_at': current_time.isoformat()}
        
        if user['level'] >= 20 and 'productivity_guru' not in user['achievements']:
            user['achievements']['productivity_guru'] = {'unlocked_at': current_time.isoformat()}

    def get_user_stats(self):
        """Get current user's statistics."""
        if not self.current_user:
            return None
        return self.user_data[self.current_user]

    def update_tasks_completed(self, count=1):
        """Update the number of completed tasks."""
        if self.current_user:
            self.user_data[self.current_user]['tasks_completed'] += count
            self._save_data() 