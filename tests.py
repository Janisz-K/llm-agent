from functions.get_files_info import get_files_info
import os
from functions.get_files_content import get_file_content
from functions.write_file import write_file

def main():
 
        content = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        content2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        content3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        #content4 = get_file_content("calculator", "pkg/does_not_exist.py")

        print(f"{content}")
        print(f"{content2}") 
        print(f"{content3}") 
        #print(f"{content4}") 



if __name__ == "__main__":
    main()