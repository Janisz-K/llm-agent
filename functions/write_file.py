import os

def write_file(working_dir, file_path, content):
    project_path = os.path.abspath(working_dir)
    project_path_list = project_path.split(os.path.sep)
    item_path = os.path.join(project_path, file_path)
    item_path_abs = os.path.abspath(item_path)
    item_path_list = item_path_abs.split(os.path.sep)

    if project_path_list != item_path_list[0:len(project_path_list)]:
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    item_path_dir = os.path.dirname(item_path_abs)

    if not os.path.exists(item_path_dir):
        try:
            os.makedirs(item_path_dir, mode=0o777, exist_ok=True)
        except Exception as e:
            return (f"Error: {e}")

    try:
        with open(item_path_abs, "w") as f:
            f.write(content)

    except Exception as e:
        return (f"Error: {e}")
    
    return (f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)")



