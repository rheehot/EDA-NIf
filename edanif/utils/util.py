import os
from io import StringIO


def find_all_files(top_folder_path: str, include_word: str) -> list:
    all_file_pathes = []
    for (root, directories, files) in os.walk(top_folder_path):
        for file in files:
            if include_word in file:
                detect_file_path = os.path.join(root, file)
                all_file_pathes.append(detect_file_path)

    return all_file_pathes
    

def save_print_instance(*message):
    io = StringIO()
    print(*message, file=io, end="")
    return io.getvalue()

