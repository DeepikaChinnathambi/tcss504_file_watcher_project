import os
import random
import time

class LotrFileManager:
    def __init__(self, target_directory):
        self.names = [
            "Frodo Baggins", "Samwise Gamgee", "Gandalf", "Aragorn", "Legolas", "Gimli", "Boromir", "Gollum",
            "Arwen", "Galadriel", "Elrond", "Saruman", "Bilbo Baggins", "Merry Brandybuck", "Pippin Took",
            "Theoden", "Eowyn", "Faramir", "Treebeard", "Eomer", "Celeborn", "Denethor", "Glorfindel",
            "Radagast", "Shelob", "Sauron"
        ]
        self.target_directory = target_directory
        self.created_files = []
        self.start_time = time.time()

        # Ensure the target directory exists
        if not os.path.exists(self.target_directory):
            os.makedirs(self.target_directory)

    def create_text_file(self, name):
        """Creates a text file with the given name."""
        file_path = os.path.join(self.target_directory, f"{name}.txt")
        with open(file_path, 'w') as file:
            file.write(f"This is the file for {name}.")
        self.created_files.append(file_path)

    def edit_text_file(self):
        """Randomly selects a file and edits it."""
        if not self.created_files:
            return

        file_to_edit = random.choice(self.created_files)
        with open(file_to_edit, 'a') as file:
            file.write("\nThis file has been edited.")

    def rename_text_file(self):
        """Randomly selects a file to rename with an unused name."""
        if not self.created_files:
            return

        file_to_rename = random.choice(self.created_files)
        available_names = [name for name in self.names if f"{name}.txt" not in self.created_files]

        if not available_names:
            return

        new_name = random.choice(available_names)
        new_file_path = os.path.join(self.target_directory, f"{new_name}.txt")

        os.rename(file_to_rename, new_file_path)
        self.created_files.remove(file_to_rename)
        self.created_files.append(new_file_path)

    def delete_text_file(self):
        """Randomly selects a file and deletes it."""
        if not self.created_files:
            return

        file_to_delete = random.choice(self.created_files)
        os.remove(file_to_delete)
        self.created_files.remove(file_to_delete)

    def create_new_file(self):
        """Creates a new file with a name that is not already used."""
        available_names = [name for name in self.names if f"{name}.txt" not in self.created_files]

        if not available_names:
            return

        new_name = random.choice(available_names)
        self.create_text_file(new_name)

    def perform_random_action(self):
        """Performs one of the following actions randomly: edit, rename, delete, create new."""
        action = random.choice([self.edit_text_file, self.rename_text_file, self.delete_text_file, self.create_new_file])
        action()

    def run(self):
        """Run the process for up to 5 minutes."""
        while time.time() - self.start_time < 300:  # 300 seconds (5 minutes)
            self.perform_random_action()
            time.sleep(random.randint(1, 5))  # Wait for 1 to 5 seconds between actions


if __name__ == "__main__":
    # Usage
    directory = r"C:\Users\lwilk\Desktop\test"
    manager = LotrFileManager(directory)

    # Create initial files
    for name in manager.names[:5]:  # Create a handful of initial files
        manager.create_text_file(name)

    manager.run()
