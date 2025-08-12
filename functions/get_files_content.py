import os
from config import *

def get_file_content(working_dir, file_path):

    try: 
        project_path = os.path.abspath(working_dir)
        project_path_list = project_path.split(os.path.sep)
        file_path_abs = os.path.abspath(file_path)
        file_path_list = file_path_abs.split(os.path.sep)

        if project_path != file_path_list[0:len(project_path_list)]:
            raise Exception (f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(file_path):
            raise Exception (f'Error: File not found or is not a regular file: "{file_path}"')
    
        with open(file_path_abs, "r") as f:
            file_content = f.read(CHARACTER_LIMIT)
    
        return file_content
    
    except Exception as e:
        print(e)
