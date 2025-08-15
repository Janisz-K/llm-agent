from functions.get_files_info import get_files_info
import os
from functions.get_files_content import get_file_content

def main():
    try: 
        content = get_file_content("calculator", "main.py")
        content2 = get_file_content("calculator", "pkg/calculator.py")
        content3 = get_file_content("calculator", "/bin/cat")
        content4 = get_file_content("calculator", "pkg/does_not_exist.py")

        print(f"{content}")
        print(f"{content2}") 
        print(f"{content3}") 
        print(f"{content4}") 

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()