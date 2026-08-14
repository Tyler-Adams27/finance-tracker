"""
Gives the linecount of the project
"""
from pathlib import Path

def get_files():
    """
    Calculates the total line count by traversing every immediate subdirectory
    under 'src', finding all .py files, and summing their lines efficiently.
    Also counts files directly in the root source directory itself.
    """
    line_count = 0
    try:
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent.parent
        root_path = project_root / "src" 

    except NameError:
        return

    if not root_path.is_dir():
        return
    
    try:
        for file_path in root_path.glob("*.py"):
            if file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        count = len(lines)
                        line_count += count
                except UnicodeDecodeError:
                    print(f"  ! WARNING: Skipping {file_path.name} due to encoding error (not UTF-8).")
    except FileNotFoundError:
        print("FILE NOT FOUND!")
    for sub_dir_path in root_path.iterdir():
        # Only process items that are directories
        if sub_dir_path.is_dir():
            try:
                file_count = 0
                for file_path in sub_dir_path.glob("*.py"):
                    if file_path.is_file():
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                lines = f.readlines()
                                count = len(lines)
                                line_count += count
                            file_count += 1

                        except UnicodeDecodeError:
                            print(f"  ! WARNING: Skipping {file_path.name} due to encoding error (not UTF-8)."))
            except FileNotFoundError:
                print("File not found!")
    print(f"Line count: {line_count}")
get_files()
