import uuid

class FileService:
    
    def get_random_filename(self, ext: str) -> str:
        return f"{uuid.uuid4()}.{ext}"  
    
    def get_file(self, path: str):
        with open(path, 'rb') as file:
            image = file.read()
            file.close()
        return image
    
    def save_file(self, content: str, file_path: str) -> None:
        with open(file_path, 'wb') as file:
            file.write(content)
            file.close()        