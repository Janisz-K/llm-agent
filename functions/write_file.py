import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write over the content of a specified file provided the file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file the content will be overwritten using the provided content, relative to the working directory. Target file_path needs to be a file not a directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written over the target file",
            ),
        },
    ),
)

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



