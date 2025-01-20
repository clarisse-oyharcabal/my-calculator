import json
import os

# Define the path to the history JSON file
history_file_path = os.path.join("..", "history", "history.json")

def save_to_history(operation, result):
    # Load existing history
    history = load_history()

    # Append new operation and result
    history.append({"operation": operation, "result": result})

    # Ensure the history directory exists
    os.makedirs(os.path.dirname(history_file_path), exist_ok=True)

    # Save updated history to file
    with open(history_file_path, "w") as f:
        json.dump(history, f, indent=4)

def load_history():
    # Check if the history file exists
    if not os.path.exists(history_file_path):
        return []

    # Load history from the file
    with open(history_file_path, "r") as f:
        return json.load(f)

def clear_history():
    # Clear the history file
    with open(history_file_path, "w") as f:
        json.dump([], f, indent=4)

def view_history(): 
    history = load_history() 
    if not history: 
        print("The history is empty.") 
    else: 
        for record in history: 
            print(f"Operation: {record['operation']}, Result: {record['result']}")