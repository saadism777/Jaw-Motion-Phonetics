import tkinter as tk
from tkinter import messagebox, simpledialog
from keywords import *
# Create a dictionary to store the phonetic types and their corresponding initial keyword lists
initial_keywords_dict = keywords_dict

# Create a dictionary to store the current keyword lists for each phonetic type
keywords_dict = {}

global category_listbox, keyword_entry, keyword_listbox, category_frame

def initialize_keywords_dict():
    global keywords_dict
    for phonetic_type, keywords in initial_keywords_dict.items():
        keywords_dict[phonetic_type] = keywords[:]

def remove_keyword(category, keyword):
    if keyword in keywords_dict[category]:
        keywords_dict[category].remove(keyword)
        update_listbox(category)

def clear_all(category):
    keywords_dict[category] = []
    update_listbox(category)

def save_changes():
    try:
        with open("keywords.py", "w") as file:
            file.write("keywords_dict = {\n")
            for phonetic_type, keywords in keywords_dict.items():
                file.write(f"    '{phonetic_type}': {keywords},\n")
            file.write("}\n")
        messagebox.showinfo("Saved", "Changes have been saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def add_keyword(category, keyword):
    if keyword.strip() != "":
        keywords_dict[category].append(keyword.strip())
        keyword_entry.delete(0, tk.END)
        update_listbox(category)

def update_listbox(category):
    keyword_listbox.delete(0, tk.END)
    for keyword in keywords_dict[category]:
        keyword_listbox.insert(tk.END, keyword)

def on_select(event):
    selected_category = category_listbox.get(tk.ACTIVE)
    update_listbox(selected_category)

def add_phonetic_type(phonetic_type, initial_keywords):
    global keywords_dict
    initial_keywords_dict[phonetic_type] = initial_keywords
    keywords_dict[phonetic_type] = initial_keywords[:]
    category_listbox.insert(tk.END, phonetic_type)

def remove_phonetic_type(phonetic_type):
    global keywords_dict
    if phonetic_type in keywords_dict:
        del keywords_dict[phonetic_type]
        category_listbox.delete(tk.ACTIVE)

def create_gui():
    initialize_keywords_dict()
    root = tk.Tk()
    root.title("Phonetic Keywords Editor")

    # Set the window icon
    icon_path = '..\images\logo.ico'   # Replace with the path to your icon file
    root.iconbitmap(icon_path)
    # Frames
    category_frame = tk.Frame(root)
    category_frame.pack(side=tk.LEFT, padx=10, pady=10)

    keyword_frame = tk.Frame(root)
    keyword_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Remove Keyword Button
    remove_button = tk.Button(keyword_frame, text="Remove Keyword", command=lambda: remove_keyword(category_listbox.get(tk.ACTIVE), keyword_listbox.get(tk.ACTIVE)))
    remove_button.pack()

    # Clear All Button
    clear_all_button = tk.Button(keyword_frame, text="Clear All", command=lambda: clear_all(category_listbox.get(tk.ACTIVE)))
    clear_all_button.pack()

    # Category Listbox
    global category_listbox, keyword_listbox, keyword_entry
    category_listbox = tk.Listbox(category_frame, width=20)
    for category in keywords_dict:
        category_listbox.insert(tk.END, category)
    category_listbox.pack()

    # Keyword Listbox
    keyword_listbox = tk.Listbox(keyword_frame, width=30)
    keyword_listbox.pack()

    # Keyword Entry
    keyword_entry = tk.Entry(keyword_frame, width=30)
    keyword_entry.pack()

    # Buttons
    add_button = tk.Button(keyword_frame, text="Add Keyword", command=lambda: add_keyword(category_listbox.get(tk.ACTIVE), keyword_entry.get()))
    add_button.pack()

    save_button = tk.Button(root, text="Save Changes", command=save_changes)
    save_button.pack(pady=10)

    # Bind event
    category_listbox.bind("<<ListboxSelect>>", on_select)

    # Add Phonetic Type Button
    add_type_button = tk.Button(category_frame, text="Add Phonetic Type", command=add_new_type)
    add_type_button.pack()

    # Remove Phonetic Type Button
    remove_type_button = tk.Button(category_frame, text="Remove Phonetic Type", command=remove_selected_type)
    remove_type_button.pack()

    root.mainloop()

def add_new_type():
    phonetic_type = simpledialog.askstring("New Phonetic Type", "Enter the new phonetic type:")
    if phonetic_type:
        add_phonetic_type(phonetic_type, [])

def remove_selected_type():
    selected_type = category_listbox.get(tk.ACTIVE)
    if selected_type:
        remove_phonetic_type(selected_type)

if __name__ == "__main__":
    create_gui()
