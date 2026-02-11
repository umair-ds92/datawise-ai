"""
File Handler Utility
Manages data file upload, storage, and retrieval
"""

import os
import shutil
from pathlib import Path
from typing import Optional
from config.constants import UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


class FileHandler:
    """
    Handles all file operations for DataWise AI
    """

    def __init__(self):
        # Create required directories
        for directory in [UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR]:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def save_upload(self, file_content: bytes, filename: str) -> Optional[str]:
        """
        Save an uploaded file to the uploads directory

        Args:
            file_content: File content as bytes
            filename: Original filename

        Returns:
            str: Path where file was saved, or None on failure
        """
        try:
            # Validate extension
            if not self._is_valid_extension(filename):
                raise ValueError(
                    f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
                )

            # Validate file size
            size_mb = len(file_content) / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                raise ValueError(
                    f"File too large ({size_mb:.1f}MB). Max: {MAX_FILE_SIZE_MB}MB"
                )

            # Save file
            save_path = Path(UPLOAD_DIR) / filename
            with open(save_path, 'wb') as f:
                f.write(file_content)

            # Also copy to temp for agent access
            temp_path = Path(TEMP_DIR) / filename
            shutil.copy2(save_path, temp_path)

            return str(save_path)

        except Exception as e:
            print(f"❌ Error saving upload: {e}")
            return None

    def get_output_path(self, filename: str) -> str:
        """
        Get path for an output file

        Args:
            filename: Output filename

        Returns:
            str: Full path for output file
        """
        return str(Path(OUTPUT_DIR) / filename)

    def get_temp_path(self, filename: str) -> str:
        """
        Get path for a temp file (accessible by Docker agents)

        Args:
            filename: Temp filename

        Returns:
            str: Full path for temp file
        """
        return str(Path(TEMP_DIR) / filename)

    def output_exists(self, filename: str) -> bool:
        """
        Check if an output file exists

        Args:
            filename: Filename to check

        Returns:
            bool: True if file exists
        """
        return Path(OUTPUT_DIR / filename).exists() or \
               Path(TEMP_DIR / filename).exists()

    def get_output_file(self, filename: str) -> Optional[bytes]:
        """
        Read and return an output file

        Args:
            filename: File to read

        Returns:
            bytes: File content, or None if not found
        """
        # Check temp dir first (agents save here)
        for directory in [TEMP_DIR, OUTPUT_DIR]:
            file_path = Path(directory) / filename
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    return f.read()
        return None

    def list_outputs(self) -> list:
        """
        List all output files

        Returns:
            list: List of output filenames
        """
        outputs = []
        for directory in [OUTPUT_DIR, TEMP_DIR]:
            for file in Path(directory).iterdir():
                if file.is_file() and not file.name.startswith('.'):
                    outputs.append(file.name)
        return list(set(outputs))

    def cleanup_temp(self) -> int:
        """
        Clean up temporary files

        Returns:
            int: Number of files deleted
        """
        count = 0
        for file in Path(TEMP_DIR).iterdir():
            if file.is_file():
                file.unlink()
                count += 1
        return count

    def _is_valid_extension(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        return ext in ALLOWED_EXTENSIONS

    def get_file_info(self, filename: str) -> Optional[dict]:
        """
        Get information about a file

        Args:
            filename: File to get info about

        Returns:
            dict: File information or None
        """
        for directory in [UPLOAD_DIR, TEMP_DIR, OUTPUT_DIR]:
            file_path = Path(directory) / filename
            if file_path.exists():
                stat = file_path.stat()
                return {
                    'name': filename,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'path': str(file_path),
                }
        return None


# Global instance
file_handler = FileHandler()


if __name__ == "__main__":
    print("🧪 Testing File Handler...")

    handler = FileHandler()

    # Test save upload
    test_content = b"col1,col2\n1,2\n3,4"
    path = handler.save_upload(test_content, 'test_data.csv')
    print(f"✅ Save upload: {path}")

    # Test file info
    info = handler.get_file_info('test_data.csv')
    print(f"✅ File info: {info}")

    # Test output path
    output_path = handler.get_output_path('output.png')
    print(f"✅ Output path: {output_path}")

    # Test list outputs
    outputs = handler.list_outputs()
    print(f"✅ Listed outputs: {len(outputs)} files")

    print("\n✅ File Handler working correctly!")