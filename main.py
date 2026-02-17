from pathlib import Path
from dotenv import dotenv_values
from modules.speak_module.speak_module import Speaking_Module
config = dotenv_values(".env")
voice_model_path = Path.cwd()/"amy/en_US-amy-low.onnx"

def get_file_list():
    try:
        file_list = []
        main_reading_dir = Path.cwd()/"files"
        file_exntension = f"*.{config["EXTENSION"]}"
        files = main_reading_dir.rglob(file_exntension)
        for f in files:
            file_list.append(f.as_posix())
        return file_list
    except Exception as e:
        print(f"\nException: {e}\n\n")

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
            case _:
                print("\nOut of bounds\n\n")
                main()
    except Exception as e:
        print("Not a number\n\n")
        main()
    except KeyboardInterrupt:
        print("\nQuitting\n\n")
        quit()

def main():
    user_input = input("Write in your number:\n\nType in:\n\n1. Launch recordings.\n\n")
    user_input = str(user_input).lower().strip()
    user_input = int(user_input)
    if (user_input.is_integer()):
        check_selection(user_input)
    else:
        print("\nNot a number\n\n")
        main()

if __name__ == "__main__":
    main()
