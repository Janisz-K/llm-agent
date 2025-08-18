import os
from functions.config import *
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of a specified file provided the file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file the content will be retrieved from, relative to the working directory. Content is truncated at 10000 characters and needs to be a file not a directory",
            ),
        },
    ),
)

def get_file_content(working_dir, file_path):

    print(f"get file content: working dir {working_dir}, filepath {file_path}")

    try: 
        project_path = os.path.abspath(working_dir)
        project_path_list = project_path.split(os.path.sep)
        item_path = os.path.join(project_path, file_path)
        item_path_abs = os.path.abspath(item_path)
        item_path_list = item_path_abs.split(os.path.sep)



        if project_path_list != item_path_list[0:len(project_path_list)]:
            raise Exception (f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(item_path_abs):
            raise Exception (f'Error: File not found or is not a regular file: "{file_path}"')
    
        with open(item_path_abs, "r") as f:
            file_content = f.read(CHARACTER_LIMIT)
            complete_content = f.read()
            if len(complete_content) > 10000:
                end_text_msg = f"[...File: {file_path}, truncated at 10000 characters]"
                file_content = file_content + end_text_msg
    
        return file_content
    
    except Exception as e:
        print(f"Error: {e}")
