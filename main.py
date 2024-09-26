import os
from tkinter import Tk, Label, Button, Text, Listbox, filedialog, messagebox, Checkbutton, IntVar
import time

# Variables
selected_original_folder = ''
selected_destination_folder = ''
log_file_path = 'assets/logs/file_actions.log'
window_width = 1200  # Set your desired width
window_height = 600  # Set your desired height
last_position = 0  # Initialize the position tracker


# Function to log actions
def log_action(action, file_name):
    timestamp = time.strftime("%Y-%m-%d|%H:%M:%S")
    log_entry = f"{user} || {timestamp} || {action}: {file_name}\n"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)


def display_logs():
    global last_position  # Use global to modify the variable across function calls

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            # Move to the last read position
            log_file.seek(last_position)

            # Read new lines from the current position
            new_logs = log_file.readlines()

            # If there are new logs, insert them into the log_text widget
            if new_logs:
                for log in new_logs:
                    log_text.insert('end', log.strip() + '\n')  # Add a newline after each log entry

                # Update the last read position to the current end of file
                last_position = log_file.tell()

        log_text.see('end')  # Scroll to the end of the Text widget


# Function to get the current user.
def get_current_user():
    global user
    user = os.getlogin()  # Returns the current user's login name


# Function to choose original folder
def choose_original_folder():
    # Open a folder selection dialog
    get_current_user()

    folder_original_path = filedialog.askdirectory()

    # If a folder is selected, show its contents
    if folder_original_path:
        if folder_original_path == selected_destination_folder:
            messagebox.showerror('Error', 'Original and destination folders cannot be the same.')
            return

    # If a folder is selected, show its contents
    if folder_original_path:
        print(f"\033[34m - User {user} choose the original file as: {folder_original_path}\033[0m")
        log_action("Original Folder selected:", folder_original_path)  # Log the copy action
        display_logs()
        selected_original_folder_label.config(text=f'Selected Folder: {folder_original_path}')
        list_files(folder_original_path, 1)
        global selected_original_folder
        selected_original_folder = folder_original_path


# Function to choose the destination folder
def choose_destination_folder():
    # Open a folder selection dialog
    folder_destination_path = filedialog.askdirectory()

    # If a folder is selected, show its contents
    if folder_destination_path:
        if folder_destination_path == selected_original_folder:
            messagebox.showerror('Error', 'Original and destination folders cannot be the same.')
            return

    # If a folder is selected, show its contents
    if folder_destination_path:
        print(f"\033[34m - User {user} choose the original file as: {folder_destination_path}\033[0m")
        log_action("Destination Folder selected:", folder_destination_path)  # Log the copy action
        display_logs()
        selected_destination_folder_label.config(text=f'Selected Folder: {folder_destination_path}')
        list_files(folder_destination_path, 2)
        global selected_destination_folder
        selected_destination_folder = folder_destination_path


# Function to list all files and directories in the selected folder
def list_files(folder_path, list_number):
    try:
        items = os.listdir(folder_path)  # Get list of files and directories

        if list_number == 1:
            file_original_listbox.delete(0, 'end')  # Clear listbox
        elif list_number == 2:
            file_destination_listbox.delete(0, 'end')  # Clear listbox

        for item in items:
            item_path = os.path.join(folder_path, item)

            # Distinguish between files and directories
            if os.path.isdir(item_path):
                display_text = f'{"[Fold]"} - {item} '  # Label directories
            else:
                display_text = f'{"[File]"} - {item} '  # Normal file display

            # Insert into the appropriate listbox
            if list_number == 1:
                file_original_listbox.insert('end', display_text)
            elif list_number == 2:
                file_destination_listbox.insert('end', display_text)
    except Exception as e:
        messagebox.showerror('Error', f'Could not list files and directories: {e}')


# Function to delete files that no longer exist in the original folder
def delete_sync(destination):

    os.remove(destination)
    log_action("Deleted", destination)  # Log the deletion


# Function to sync the file between the original and destination folders
def sync_file(original, destination):
    try:
        # Check if the destination file exists
        if os.path.exists(destination):
            # Read the contents of both files to compare
            with open(original, 'rb') as f_original:
                original_content = f_original.read()

            with open(destination, 'rb') as f_destination:
                destination_content = f_destination.read()

            # Compare the contents
            if original_content == destination_content:
                print(f"\033[32m No changes detected for {original}. Skipping copy.\033[0m")
                log_action("Skipped (No Changes)", original)  # Log the skip action
            else:
                # If contents differ, copy the file
                with open(destination, 'wb') as f_destination:
                    f_destination.write(original_content)
                print(f"\033[34m File {original} updated in {destination}.\033[0m")
                log_action("Updated", original)  # Log the update action

        else:
            # Destination file does not exist, copy the original file
            with open(original, 'rb') as f_original:
                original_content = f_original.read()

            with open(destination, 'wb') as f_destination:
                f_destination.write(original_content)
            print(f"\033[34m File {original} copied to {destination}.\033[0m")
            log_action("Copied", original)  # Log the copy action

        # Refresh the destination folder list to reflect the change
        list_files(selected_destination_folder, 2)

    except Exception as e:
        print(f"\033[31m An error occurred while syncing the file: {e} \033[0m")
        log_action("Error Syncing", f"{original}: {e}")  # Log the error
        display_logs()  # Update the log display


def copy_folder_files(original_folder, destination_folder, auto):
    try:
        # Ensure destination folder exists
        if not os.path.exists(destination_folder):
            os.mkdir(destination_folder)

        items = os.listdir(original_folder)  # List all items in the original folder

        # Create a set of original items for easier comparison
        original_items_set = set(items)

        # Process each item in the original folder
        for item in items:
            # Create full paths for source and destination
            source_path = os.path.join(original_folder, item)
            dest_path = os.path.join(destination_folder, item)

            # If it's a directory, recursively copy its contents
            if os.path.isdir(source_path):
                copy_folder_files(source_path, dest_path, auto)
            else:
                # If it's a file, sync it
                sync_file(source_path, dest_path)

        # After processing, check for items in the destination folder that are not in the original
        dest_items = os.listdir(destination_folder)  # List items in the destination folder
        for item in dest_items:
            dest_path = os.path.join(destination_folder, item)

            # If an item in the destination is not found in the original, delete it
            if item not in original_items_set:
                print(f"\033[31m File {item} was removed from original. Deleting from destination.\033[0m")
                os.remove(dest_path)  # Remove the file from the destination
                log_action("Deleted", item)  # Log the deletion action

    except Exception as e:
        messagebox.showerror('Error', f'Could not copy folder: {e}')


# Function to handle copying the entire folder
def sync_folder(auto):
    if selected_original_folder == '':
        print("\033[31mError - User tried to sync folder without selecting original Folder\033[0m")
        messagebox.showerror('Error', 'Please select an original folder')
    elif selected_destination_folder == '':
        print("\033[31mError - User tried to sync folder without selecting destination Folder\033[0m")
        messagebox.showerror('Error', 'Please select a destination folder')
    else:
        new_folder = os.path.join(selected_destination_folder, 'CopiedFolder')
        try:
            copy_folder_files(selected_original_folder, new_folder, auto)
        except Exception as e:
            print(f'\033[31mError - Could not copy the folder: {e}\033[0m')
            messagebox.showerror('Error', f'Could not copy folder: {e}')
            log_action('Error syinking the files error:', e)
            display_logs()


# Timer function to update file lists
def update_file_lists():
    if timer_var.get():  # Check if the timer is activated
        sync_folder(True)  # Start copying if the timer is enabled
        if selected_original_folder:
            list_files(selected_original_folder, 1)
        if selected_destination_folder:
            list_files(selected_destination_folder, 2)
        root.after(30000, update_file_lists)  # Schedule the next update in 60 seconds


# Function to start the timer
def toggle_timer():
    if timer_var.get():
        update_file_lists()  # Start updating if the timer is enabled
        display_logs()  # Display logs


# Function to show keynotes
def show_keynotes():
    keynotes = (
        "Keynotes:\n"
        "1 - Removed the progress bar as it is irrelevant without a thread process"
        "2 - Well, please use small directories to test, as implementing thread or batch process will complicate the project and async will restructure the project, it works, but is very slow\n"
    )
    messagebox.showinfo("Keynotes", keynotes)


# Function to show help
def show_help():
    help_text = (
        "Help:\n"
        "This application allows you to copy files from one folder to another.\n"
        "Steps to use the application:\n"
        "1. Click 'Choose Original Folder' to select the folder with files.\n"
        "2. Click 'Choose Destination Folder' to select where to copy files.\n"
        "3. Click 'Copy Folder Manually' to start the copying process.\n"
        "If you encounter any issues, please check folder permissions."
    )
    messagebox.showinfo("Help", help_text)


# Create the main window
root = Tk()
root.title('Folder Copier')

# Get user screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position for centering
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

# Set the window geometry (size and position)
root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

# Set the window icon
root.iconbitmap('assets/images/software_icon.ico')  # Replace 'your_icon.ico' with your icon file name

# Configure grid
# Don't mess with this, not worth it
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)  # List boxes
root.grid_rowconfigure(7, weight=1)  # Log Text Box

# Original folder column button
choose_original_folder_button = Button(root, text='Choose Original Folder', command=choose_original_folder)
choose_original_folder_button.grid(row=0, column=0, pady=(20, 0), padx=(20, 20))

# Original folder label
selected_original_folder_label = Label(root, text='Select a folder')
selected_original_folder_label.grid(row=1, column=0, pady=(10, 20), padx=(20, 20))

# List Original Files/Folders
file_original_listbox = Listbox(root, width=50, height=10)
file_original_listbox.grid(row=2, column=0, padx=(20, 10), pady=(10, 20))

# Button Destination folder
choose_destination_folder_button = Button(root, text='Choose Destination Folder', command=choose_destination_folder)
choose_destination_folder_button.grid(row=0, column=1, pady=(20, 0), padx=(20, 20))

# Label select destination folder list
selected_destination_folder_label = Label(root, text='Select a folder')
selected_destination_folder_label.grid(row=1, column=1, pady=(10, 20), padx=(20, 20))

# List the destination folders
file_destination_listbox = Listbox(root, width=50, height=10)
file_destination_listbox.grid(row=2, column=1, padx=(10, 20), pady=(10, 20))

# Copy folder button centered below both columns
copy_button = Button(root, text='Sync Folder Manually', command=lambda: sync_folder(False))
copy_button.grid(row=3, column=0, columnspan=2, pady=20)

# Switch for the timer
timer_var = IntVar()
timer_switch = Checkbutton(root, text='Enable Auto Update (30 seconds)', variable=timer_var, command=toggle_timer)
timer_switch.grid(row=4, column=0, columnspan=2, pady=(10, 20), sticky='ew')

# Keynotes button
keynotes_button = Button(root, text='Keynotes', command=show_keynotes)
keynotes_button.grid(row=3, column=0, pady=(10, 20))

# Help button
help_button = Button(root, text='Help', command=show_help)
help_button.grid(row=3, column=1, pady=(10, 20))

# Text widget for displaying logs
log_text = Text(root, wrap='word')
log_text.grid(row=7, column=0, columnspan=2, padx=20, pady=(10, 20), sticky='nsew')
display_logs()

# Configure the grid row for the log text
root.grid_rowconfigure(7, weight=1)

# Start the GUI main loop
root.mainloop()
