from functions.get_files_info import get_files_info
import os

def main():
    try:
        test_1 = get_files_info("calculator", ".")
        print(f"{test_1}")
    except Exception as e:
        print(e)

    try:
        test_2 = get_files_info("calculator", "pkg")
        print(f"{test_2}")
    except Exception as e:
        print(e)

    try:
        test_3 = get_files_info("calculator", "/bin")
        print(f"{test_3}")
    except Exception as e:
        print(e)

    try:
        test_4 = get_files_info("calculator", "../")
        print(f"{test_4}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()