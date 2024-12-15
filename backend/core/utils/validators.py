def is_safe_filename(filename: str) -> bool:
    # Add logic to prevent directory traversal, etc.
    return ".." not in filename and "/" not in filename
