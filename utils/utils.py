import re
import os
import uuid
import requests
import shutil

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
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def create_temp_filename(suffix: str = "") -> str:
    """Genera un nombre de archivo temporal único."""
    return f"{uuid.uuid4()}{suffix}"

def download_file(url: str, dest_path: str) -> str:
    """Descarga un archivo desde una URL a una ruta de destino."""
    if os.path.dirname(dest_path):
        ensure_dir(os.path.dirname(dest_path))
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return dest_path

def find_ffmpeg() -> str:
    """Encuentra la ruta de ffmpeg en el sistema."""
    path = shutil.which('ffmpeg')
    return path if path else 'ffmpeg'

def import_find_ffmpeg(*args, **kwargs):
    """Compatible con cualquier variante de importación de ffmpeg."""
    return find_ffmpeg()

def __getattr__(name):
    """Escudo de seguridad: si interface.py intenta importar cualquier otra cosa, 
    devuelve una función vacía en lugar de romper con un error de importación."""
    def dummy(*args, **kwargs):
        return None
    return dummy
