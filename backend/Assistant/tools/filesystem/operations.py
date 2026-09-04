"""
Low-level filesystem operations (read, write, list, move, delete, etc.)
used by the filesystem tool.
"""
import os
import shutil


class FilesystemOperations:

    def create_folder(self, path: str):
        if os.path.exists(path):
            return False

        os.makedirs(path)
        return True

    def create_file(self, path: str):
        if os.path.exists(path):
            return False

        parent = os.path.dirname(path)

        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(path, "w", encoding="utf-8"):
            pass

        return True

    def delete(self, path: str):
        if not os.path.exists(path):
            return False

        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

        return True

    def rename(self, source: str, destination: str):
        if not os.path.exists(source):
            return False

        os.rename(source, destination)
        return True

    def move(self, source: str, destination: str):
        if not os.path.exists(source):
            return False

        shutil.move(source, destination)
        return True

    def copy(self, source: str, destination: str):
        if not os.path.exists(source):
            return False

        if os.path.isdir(source):
            shutil.copytree(
                source,
                destination,
                dirs_exist_ok=True,
            )
        else:
            shutil.copy2(source, destination)

        return True

    def list_directory(self, path: str):
        if not os.path.isdir(path):
            return []

        return os.listdir(path)

    def find(self, query: str, root="."):

        matches = []

        for current_root, dirs, files in os.walk(root):

            for name in dirs + files:

                if query.lower() in name.lower():
                    matches.append(
                        os.path.join(
                            current_root,
                            name,
                        )
                    )

        return matches

    def open_path(self, path: str):

        if not os.path.exists(path):
            return False

        try:
            os.startfile(path)
            return True
        except Exception:
            return False