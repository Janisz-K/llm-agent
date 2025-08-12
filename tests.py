from functions.get_files_info import get_files_info
import os
from functions.get_files_content import get_file_content

def main():

    content = get_file_content("calculator", "lorem.txt")

    print(f"is this workign? {content}")


if __name__ == "__main__":
    main()