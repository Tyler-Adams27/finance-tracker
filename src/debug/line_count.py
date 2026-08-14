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
         print("FATAL ERROR: Cannot determine script location (__file__ is unavailable). Please run this file normally.")
         return

    if not root_path.is_dir():
        print("\n==========================================================")
        print(f"FATAL ERROR: Root directory NOT found at {root_path}.{root_path.resolve()}")
        print("ACTION REQUIRED: The path calculation failed.")
        print("Please adjust the script's relative path logic if 'src' is not in this expected location.")
        print("==========================================================")
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
                except Exception as e:
                    print(f"  ! ERROR reading {file_path.name}: {e}")
    except Exception as e:
        print(f"  ! CRITICAL ERROR during root file scan: {e}")

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
                             print(f"  ! WARNING: Skipping {file_path.name} due to encoding error (not UTF-8).")
                        except Exception as e:
                            print(f"  ! ERROR reading {file_path.name}: {e}")
            except Exception as e:
                print(f"  ! CRITICAL ERROR processing directory {sub_dir_path.name}: {e}")
    print(f"Line count: {line_count}")
get_files()
