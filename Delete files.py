import os
import shutil

# Define the path to the problematic directory
root_directory = r"C:\Users\marqu\Desktop\CopiedFolder"  # Replace with the path to your directory


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
