import os


def creater_path(path: str) -> None:

    if path.endswith(('docx', 'txt', 'json', 'yaml')):
        folder_dir = os.path.dirname(path) # đường dẫn của các folder
        file_name = os.path.basename(path) # tên file

        full_path = os.path.join(folder_dir, file_name) # đường dẫn đầy đủ
        os.makedirs(folder_dir, exist_ok=True) # tạo folder
        
        open(file=full_path, mode='a').close() # tạo file
    else:
        os.makedirs(path, exist_ok=True) # tạo folder
    

