import tkinter as tk
from tkinter import scrolledtext, filedialog
import numpy as np


def generate_list(start, end, step, template):
    try:
        generated_list = [template.replace('x.x', str(round(i, 2))) for i in np.arange(start, end+step, step)]
        return generated_list
    except Exception as e:
        raise e


def parse_list(input_string, separator):
    try:
        parsed_list = input_string.split(separator)
        return parsed_list
    except Exception as e:
        raise e

def find_and_replace(input_string, find_str, replace_str):
    try:
        workspace_string = input_string.replace(find_str, replace_str)
        return workspace_string
    except Exception as e:
        raise e

def print_list():
    error_area.delete(1.0, tk.END)
    try:
        start = float(start_entry.get())
        end = float(end_entry.get())
        step = float(step_entry.get())
        template = template_entry.get()
        generated_list = generate_list(start, end, step, template)
        list_type = list_type_var.get()
        
        workspace_area.delete(1.0, tk.END)
        if list_type == "comma-separated":
            workspace_area.insert(tk.END, ', '.join(generated_list))
        else:
            workspace_area.insert(tk.END, '\n'.join(generated_list))
    except Exception as e:
        error_area.insert(tk.END, str(e))

def preview_list():
    error_area.delete(1.0, tk.END)
    try:
        start = float(start_entry.get())
        end = float(end_entry.get())
        step = float(step_entry.get())
        template = template_entry.get()
        generated_list = generate_list(start, end, step, template)
        preview_window = tk.Toplevel(root)
        preview_window.title("Preview")
        preview_text = tk.Text(preview_window)
        preview_text.insert(tk.END, ', '.join(generated_list))
        preview_text.pack()
    except Exception as e:
        error_area.insert(tk.END, str(e))

def print_parse():
    error_area.delete(1.0, tk.END)
    try:
        input_string = workspace_area.get(1.0, tk.END).strip()
        separator = separator_entry.get()
        if not separator:
            raise ValueError("Separator is empty.")
        workspace_list = parse_list(input_string, separator)
        list_type = list_type_var.get()

        workspace_area.delete(1.0, tk.END)
        if list_type == "comma-separated":
            workspace_area.insert(tk.END, ', '.join(map(str, workspace_list)))
        else:
            workspace_area.insert(tk.END, '\n'.join(map(str, workspace_list)))
    except Exception as e:
        error_area.insert(tk.END, str(e))
        error_area.see(tk.END)


def print_find_and_replace():
    error_area.delete(1.0, tk.END)
    try:
        input_string = workspace_area.get(1.0, tk.END).strip()  # This line is changed
        find_str = find_entry.get()
        replace_str = replace_entry.get()
        workspace_string = find_and_replace(input_string, find_str, replace_str)

        workspace_area.delete(1.0, tk.END)
        workspace_area.insert(tk.END, workspace_string)
    except Exception as e:
        error_area.insert(tk.END, str(e))

def print_parse_and_generate():
    error_area.delete(1.0, tk.END)
    try:
        input_string = workspace_area.get(1.0, tk.END).strip()  # This line is changed
        separator = separator_entry.get()
        if not separator:
            raise ValueError("Separator is empty.")
        workspace_list = parse_list(input_string, separator)
        start = float(start_entry.get())
        end = float(end_entry.get())
        step = float(step_entry.get())
        template = template_entry.get()

        generated_lists = []
        for base_string in workspace_list:
            generated_list = generate_list(start, end, step, template.replace('x.x', base_string))
            generated_lists.append(', '.join(map(str, generated_list)))

        workspace_area.delete(1.0, tk.END)
        workspace_area.insert(tk.END, '\n'.join(generated_lists))
    except Exception as e:
        error_area.insert(tk.END, str(e))



def save_workspace():
    try:
        workspace = workspace_area.get(1.0, tk.END)
        with open('workspace.txt', 'w') as f:
            f.write(workspace)
    except Exception as e:
        error_area.insert(tk.END, str(e))

def clear_workspace():
    workspace_area.delete(1.0, tk.END)

def clear_errors():
    error_area.delete(1.0, tk.END)

def show_info(event):
    widget = event.widget
    info = {
        start_entry: "Enter the start value for the list.",
        end_entry: "Enter the end value for the list.",
        step_entry: "Enter the step value for the list generation.",
        template_entry: "Enter the template for list generation. Use 'x.x' as a placeholder for numbers.",
        generate_button: "Generate a list based on the start, end, step, and template values.",
        parse_entry: "Enter the string to be parsed into a list.",
        separator_entry: "Enter the separator used in the string to be parsed.",
        parse_button: "Parse the string into a list based on the separator.",
        find_replace_input_entry: "Enter the string where you want to find and replace values.",
        find_entry: "Enter the value you want to find.",
        replace_entry: "Enter the value you want to replace the found values with.",
        find_replace_button: "Find and replace values in the string."
    }
    if widget in info:
        info_text.delete(1.0, tk.END)
        info_text.insert(tk.END, info[widget])

def undo():
    workspace_area.event_generate("<<Undo>>")


# GUI
root = tk.Tk()
root.geometry("680x600")  # adjust the size as necessary
root.title("List Generator")

frame = tk.Frame(root, padx=20, pady=20)
frame.grid()

# Frames for different functionalities
generate_frame = tk.LabelFrame(frame, text="Generate List")
generate_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

parse_frame = tk.LabelFrame(frame, text="Parse List")
parse_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

workspace_frame = tk.LabelFrame(frame, text="workspace")
workspace_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

error_frame = tk.LabelFrame(frame, text="Error Messages")
error_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

info_frame = tk.LabelFrame(frame, text="Information", padx=5, pady=5)
info_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

# Widgets for generate list functionality
tk.Label(generate_frame, text="Start Value").grid(row=0, column=0)
start_entry = tk.Entry(generate_frame)
start_entry.grid(row=0, column=1)
tk.Label(generate_frame, text="End Value").grid(row=1, column=0)
end_entry = tk.Entry(generate_frame)
end_entry.grid(row=1, column=1)
tk.Label(generate_frame, text="Step").grid(row=2, column=0)
step_entry = tk.Entry(generate_frame)
step_entry.grid(row=2, column=1)
tk.Label(generate_frame, text="Template").grid(row=3, column=0)
template_entry = tk.Entry(generate_frame)
template_entry.insert(0, "x.x")  # insert default value
template_entry.grid(row=3, column=1)
generate_button = tk.Button(generate_frame, text="Generate list", command=print_list)
generate_button.grid(row=4, column=0, columnspan=2)
preview_button = tk.Button(generate_frame, text="Preview list", command=preview_list)
preview_button.grid(row=5, column=0, columnspan=2)

# Widgets for parse list functionality
tk.Label(parse_frame, text="String to parse").grid(row=0, column=0)
parse_entry = tk.Entry(parse_frame)
parse_entry.grid(row=0, column=1)
tk.Label(parse_frame, text="Separator").grid(row=1, column=0)
separator_entry = tk.Entry(parse_frame)
separator_entry.grid(row=1, column=1)
parse_button = tk.Button(parse_frame, text="Parse list", command=print_parse)
parse_button.grid(row=2, column=0, columnspan=2)
parse_generate_button = tk.Button(parse_frame, text="Parse and Generate list", command=print_parse_and_generate)
parse_generate_button.grid(row=3, column=0, columnspan=2)

find_replace_frame = tk.LabelFrame(frame, text="Find & Replace")
find_replace_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
tk.Label(find_replace_frame, text="Input String").grid(row=0, column=0)
find_replace_input_entry = tk.Entry(find_replace_frame)
find_replace_input_entry.grid(row=0, column=1)
tk.Label(find_replace_frame, text="Find").grid(row=1, column=0)
find_entry = tk.Entry(find_replace_frame)
find_entry.grid(row=1, column=1)
tk.Label(find_replace_frame, text="Replace").grid(row=2, column=0)
replace_entry = tk.Entry(find_replace_frame)
replace_entry.grid(row=2, column=1)
find_replace_button = tk.Button(find_replace_frame, text="Find & Replace", command=print_find_and_replace)
find_replace_button.grid(row=3, column=0, columnspan=2)

# Widgets for workspace and error messages
workspace_area = scrolledtext.ScrolledText(workspace_frame, wrap = tk.WORD, width = 50, height = 10)
workspace_area.pack()
workspace_area['maxundo'] = 100
error_area = scrolledtext.ScrolledText(error_frame, wrap = tk.WORD, width = 50, height = 5, foreground="red")
error_area.pack()

list_type_var = tk.StringVar(root)
list_type_var.set("comma-separated")
list_type_menu = tk.OptionMenu(workspace_frame, list_type_var, "comma-separated", "line-separated")
list_type_menu.pack(side="top")

clear_button = tk.Button(workspace_frame, text="Clear workspace", command=clear_workspace)
clear_button.pack(side="left")
save_button = tk.Button(workspace_frame, text="Save workspace", command=save_workspace)
save_button.pack(side="left")
undo_button = tk.Button(workspace_frame, text="Undo", command=undo)
undo_button.pack(side="left")


clear_error_button = tk.Button(error_frame, text="Clear errors", command=clear_errors)
clear_error_button.pack(side="left")

# Configure root's grid system
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Info box
info_text = tk.Text(info_frame, wrap=tk.WORD, width=22, height=5)
info_text.insert(tk.END, "Right click to see info")
info_text.pack()


undo_button = tk.Button(root, text="Undo", command=undo)


# Bind show_info function to all relevant widgets
for widget in [start_entry, end_entry, step_entry, template_entry, generate_button, parse_entry, separator_entry, parse_button, find_replace_input_entry, find_entry, replace_entry, find_replace_button]:
    widget.bind("<Button-3>", show_info)



root.mainloop()
