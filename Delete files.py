import os
import shutil
# This is a safety code, in case the software goes in a loop and creates a
# million of subfolders that crash any system, not that happened to me.
# I am not telling you ideas to crash your friends computer, change to .bat
# Define the path to the problematic directory
root_directory = r"Hard drive path here"  # Replace with the path to your directory


def delete_nested_folders(directory):
    try:
        # First, check if the directory exists
        if os.path.exists(directory):
            # Use shutil.rmtree to delete the directory and all its contents
            shutil.rmtree(directory)
            print(f"Successfully deleted: {directory}")
        else:
            print(f"The directory {directory} does not exist.")
    except Exception as e:
        print(f"Error deleting {directory}: {e}")


# Call the function to delete the deeply nested folders
delete_nested_folders(root_directory)
