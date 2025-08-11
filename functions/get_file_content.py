import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory,file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, "r") as f:
            string = f.read(MAX_CHARS)
            next_char = f.read(1)
            if next_char:
                return f'{string}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            else:
                return string
    except Exception as e:
        return f"Error: {e}"