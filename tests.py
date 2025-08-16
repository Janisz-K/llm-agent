from functions.get_files_info import get_files_info
import os
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def main():
 
        content = run_python_file("calculator", "main.py")
        content2 = run_python_file("calculator", "main.py", ["3 + 5"])
        content3 = run_python_file("calculator", "tests.py")
        content4 = run_python_file("calculator", "../main.py")
        content5 = run_python_file("calculator", "nonexistent.py")

        print(f"{content}")
        print(f"{content2}") 
        print(f"{content3}") 
        print(f"{content4}") 
        print(f"{content5}") 



if __name__ == "__main__":
    main()