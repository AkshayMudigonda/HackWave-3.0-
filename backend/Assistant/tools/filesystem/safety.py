"""
Filesystem-specific safety checks (path validation, blocked
directories, destructive-operation guards).
"""
import os


class FilesystemSafety:

    def exists(self, path: str) -> bool:
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def is_folder(self, path: str) -> bool:
        return os.path.isdir(path)

    def can_delete(self, path: str) -> bool:
        return os.path.exists(path)

    def can_create(self, path: str) -> bool:
        return not os.path.exists(path)

    def is_hidden(self, path: str) -> bool:

        try:
            return bool(
                os.stat(path).st_file_attributes
                & 0x2
            )
        except Exception:
            return False