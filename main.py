import os
from pathlib import Path
from dotenv import dotenv_values
from modules.speak_module.speak_module import Speaking_Module
config = dotenv_values(".env")
voice_model_path = Path.cwd()/"amy/en_US-amy-low.onnx"
file_exntension = f"*.{config["EXTENSION"]}"
main_reading_dir = Path.cwd()/"files"

def create_next_numbered_file(directory: str) -> None:
    """
    Creates the next numbered .txt file in the given directory
    (e.g., 1.txt, 2.txt → creates 3.txt).
    Accepts multiline user input. End input by typing 'EOF' on a new line.
    """

    try:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory does not exist: {directory}")

        # Collect existing numbered .txt files
        existing_numbers = []
        for filename in os.listdir(directory):
            name, ext = os.path.splitext(filename)
            if ext == ".txt" and name.isdigit():
                existing_numbers.append(int(name))

        next_number = max(existing_numbers, default=0) + 1
        new_filename = f"{next_number}.txt"
        new_filepath = os.path.join(directory, new_filename)

        if os.path.exists(new_filepath):
            raise FileExistsError(f"File already exists: {new_filename}")

        # Multiline input
        print("\n\nEnter file content (type 'EOF' on a new line to finish):\n\n")
        lines = []
        while True:
            line = input()
            if str(line).lower().strip() == "eof":
                break
            lines.append(line)

        content = "\n".join(lines)

        with open(new_filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\n\nFile created successfully: {new_filename} ✅\n\n")

    except (FileNotFoundError, PermissionError, FileExistsError) as e:
        print(f"Error: {e} ❌")

    except OSError as e:
        print(f"OS error occurred: {e} ❌")

    except Exception as e:
        print(f"Unexpected error: {e} ❌")


def get_file_list():
    try:
        file_list = []
        files = main_reading_dir.rglob(file_exntension)
        for f in files:
            file_list.append(f.as_posix())
        file_list.sort(key=lambda x: int(x.split("/")[-1].split(".")[0]))
        return file_list
    except Exception as e:
        print(f"\nException: {e} ❌\n\n")

def read_files():
    files = get_file_list()
    sp = Speaking_Module(voice_model_path)
    message = ""
    if files:
        for x, f in enumerate(files):
            with open(f) as single_file:
                lines = single_file.read()
            final_text = str(lines).replace("\n","")
            final_text = str(final_text.strip())
            number = f"{x+1}"
            message = f"Reading file number {number}."
            print(f"\n\n{message}\n\n")
            sp.speak(message)
            print(f"\n{final_text}\n\n")
            sp.speak(final_text)                
    else:
        main()

def check_selection(user_input):
    try:
        match(user_input):
            case 1:
                read_files()
                main()
            case 2:
                create_next_numbered_file(main_reading_dir)
                main()
            case 3:
                quit()
            case _:
                print("\nOut of bounds ❌\n\n")
                main()
    except Exception as e:
        print("Not a number ❌\n\n")
        main()
    except KeyboardInterrupt:
        print("\nQuitting\n\n")
        quit()

def main():
    user_input = input("Write in your number:\n\nType in:\n\n1. Launch recordings.\n\n2. Create a record.\n\n3. Close.\n\n")
    user_input = str(user_input).lower().strip()
    user_input = int(user_input)
    if (user_input.is_integer()):
        check_selection(user_input)
    else:
        print("\nNot a number ❌\n\n")
        main()

if __name__ == "__main__":
    main()
