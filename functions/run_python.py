import os
import subprocess

def run_python_file(working_dir, file_path, args=[]):

    project_path = os.path.abspath(working_dir)
    project_path_list = project_path.split(os.path.sep)
    item_path = os.path.join(project_path, file_path)
    item_path_abs = os.path.abspath(item_path)
    item_path_list = item_path_abs.split(os.path.sep)

    if project_path_list != item_path_list[0:len(project_path_list)]:
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    if not os.path.exists(item_path_abs):
        return (f'Error: File "{file_path}" not found.')

 
    if not item_path_abs.endswith(".py"):
        return (f'Error: "{file_path}" is not a Python file.')

    command_list = ["python",item_path_abs]

    if args:
        command_list.extend(args)
    try:
        completed_process = subprocess.run(command_list, capture_output=True, text=True, timeout=30, cwd=project_path)
    
    except Exception as e:
        return (f"Error: executing Python file: {e}")
    
    final_string = ""
    if completed_process.stdout:
        stdout = completed_process.stdout
        final_string = final_string + f"STDOUT: {stdout} "

    if completed_process.stderr:
        stderr = completed_process.stderr
        final_string = final_string + f"STDERR: {stderr} "

    if not completed_process.stdout and not completed_process.stderr:
        return f"No output produced."


    if completed_process.returncode != 0:
        return_code = completed_process.returncode
        return_code_string = f"Process exited with code {return_code}"
        final_string = final_string + return_code_string


    return final_string