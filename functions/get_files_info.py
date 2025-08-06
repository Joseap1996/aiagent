import os
def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory,directory)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    try:
        content = os.listdir(full_path)
        lines= []
        for i in sorted(content):
            item_path = os.path.join(full_path,i)
            lines.append(f' - {i}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}')
    
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

