import sys
import json
import os


def load_url():
    try:
        with open("settings.json", "r", encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
            return settings.get("vatglasses_url")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading settings: {e}")
        sys.exit(1)


def load_sector_settings():
    sector_settings = []

    def process_folder(folder_path):
        # print(f"Processing folder: {folder_path}")

        folder_contents = os.listdir(folder_path)

        for item in folder_contents:
            item_path = os.path.join(folder_path, item)

            if os.path.isdir(item_path):
                # Process sub directories
                process_folder(item_path)
            elif item_path.endswith(".json"):
                # Process json files
                print(f"Processing file: {item_path}")
                process_file(item_path, folder_path)

    def process_file(file_path, folder_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    # If data is a list, iterate through each element
                    for element in data:
                        element["folder_path"] = folder_path
                        sector_settings.append(element)
                elif isinstance(data, dict):
                    # If data is a dictionary (single object), append it
                    data["folder_path"] = folder_path
                    sector_settings.append(data)
            return
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

    base_dir = "data"

    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)

        if os.path.isdir(item_path):
            process_folder(item_path)

    return sector_settings
