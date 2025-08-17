import os
from .constants import MAX_CHARS
from google import genai
from google.genai import types

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

schema_get_file_content=types.FunctionDeclaration(
    name="get_file_content",
    description="Opens and returns a file's content, truncated if exceeds 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path the file resides",
            )
        }
    )
)