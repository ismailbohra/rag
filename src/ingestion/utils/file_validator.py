import os

class FileValidator:

    @staticmethod
    def validate(file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if os.path.isdir(file_path):
            raise ValueError("Directory given instead of file.")
