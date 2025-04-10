import json
import os
from datetime import datetime
from ui import UI

class TaskManager:
    def __init__(self, user_data):
        self.user_data = user_data
        self.tasks_file = "tasks.json"
        self.tasks = self._load_tasks()
        self.ui = UI()

    def _load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_tasks(self):
        """Save tasks to JSON file."""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def get_user_tasks(self, username):
        """Get tasks for a specific user."""
        if username not in self.tasks:
            self.tasks[username] = []
        return self.tasks[username]

    def add_task(self, username, task_name):
        """Add a new task for a user."""
        if username not in self.tasks:
            self.tasks[username] = []
        
        task = {
            'id': len(self.tasks[username]) + 1,
            'name': task_name,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        self.tasks[username].append(task)
        self._save_tasks()
        self.ui.display_success("Task added successfully!")
        return task

    def complete_task(self, username, task_id):
        """Mark a task as completed."""
        if username in self.tasks:
            for task in self.tasks[username]:
                if task['id'] == task_id:
                    task['completed'] = True
                    task['completed_at'] = datetime.now().isoformat()
                    self._save_tasks()
                    self.ui.display_success("Task marked as completed!")
                    return True
        return False

    def delete_task(self, username, task_id):
        """Delete a task."""
        if username in self.tasks:
            self.tasks[username] = [t for t in self.tasks[username] if t['id'] != task_id]
            self._save_tasks()
            self.ui.display_success("Task deleted successfully!")
            return True
        return False

    def display_tasks(self, username):
        """Display tasks in a formatted way."""
        tasks = self.get_user_tasks(username)
        if not tasks:
            print("\nNo tasks available. Add some tasks to get started!")
            return
        
        print("\nYour Tasks:")
        print("-" * 50)
        for task in tasks:
            status = "✓" if task['completed'] else " "
            print(f"[{status}] {task['id']}. {task['name']}")
        print("-" * 50)

    def manage_tasks(self, username):
        """Interactive task management menu."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_tasks(username)
            print("\nTask Management:")
            print("1. Add new task")
            print("2. Complete task")
            print("3. Delete task")
            print("4. Back to main menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                task_name = input("Enter task name: ").strip()
                if task_name:
                    self.add_task(username, task_name)
                else:
                    self.ui.display_error("Task name cannot be empty!")
            
            elif choice == '2':
                task_id = input("Enter task ID to complete: ").strip()
                if task_id.isdigit():
                    if self.complete_task(username, int(task_id)):
                        print("Task marked as completed!")
                    else:
                        self.ui.display_error("Task not found!")
                else:
                    self.ui.display_error("Invalid task ID!")
            
            elif choice == '3':
                task_id = input("Enter task ID to delete: ").strip()
                if task_id.isdigit():
                    if self.delete_task(username, int(task_id)):
                        print("Task deleted successfully!")
                    else:
                        self.ui.display_error("Task not found!")
                else:
                    self.ui.display_error("Invalid task ID!")
            
            elif choice == '4':
                break
            
            else:
                self.ui.display_error("Invalid choice!")
            
            input("\nPress Enter to continue...")

    def get_active_tasks(self, username):
        """Get all active (incomplete) tasks for a user."""
        tasks = self.get_user_tasks(username)
        return [task for task in tasks if not task['completed']]

    def get_completed_tasks(self, username):
        """Get all completed tasks for a user."""
        tasks = self.get_user_tasks(username)
        return [task for task in tasks if task['completed']] 