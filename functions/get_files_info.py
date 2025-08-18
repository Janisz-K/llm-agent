import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    project_path = os.path.abspath(working_directory)
    project_path_list = project_path.split(os.path.sep)
    full_path_list = os.path.abspath(full_path).split(os.path.sep)

    sliced_full_path = full_path_list[0:len(project_path_list)]
    

    if project_path_list != sliced_full_path:
        raise Exception (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if not os.path.isdir(full_path):
        raise Exception (f'Error: "{directory}" is not a directory')
    
    contents_list = os.listdir(full_path)

    final_list = []

    for content in contents_list:
        item_path = os.path.join(full_path, content)
        content_string = (f"- {content}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}")
        final_list.append(content_string)
    
    base_statement = ""
    if os.path.abspath(full_path) == os.path.abspath(working_directory):
        base_statement = "Result for current directory:\n"
    else:
        base_statement = f"Result for {directory}:\n"

    joined_list = "\n".join(final_list)
    return base_statement+joined_list
    