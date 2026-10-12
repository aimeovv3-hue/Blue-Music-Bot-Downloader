import re
import os

def clean_filename(filename: str) -> str:
    """Limpia caracteres inválidos para nombres de archivos."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def human_readable_size(size_bytes: int) -> str:
    """Convierte bytes a un formato legible (MB, GB, etc.)."""
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"

def get_readable_time(seconds: int) -> str:
    """Convierte segundos en un formato de tiempo legible."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

def ensure_dir(directory: str):
    """Se asegura de que el directorio exista, si no, lo crea."""
    if not os.path.exists(directory):
        os.makedirs(directory)
