import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf'}

ALLOWED_IMAGE_MIMETYPES = {'image/png', 'image/jpeg', 'image/webp', 'image/gif'}
ALLOWED_DOCUMENT_MIMETYPES = {'application/pdf'}

def get_extension(filename: str) -> str:
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

def validate_file(file_storage: FileStorage, file_type: str = 'image') -> tuple[bool, str]:
    if file_type == 'image':
        allowed_ext = ALLOWED_IMAGE_EXTENSIONS
        allowed_mime = ALLOWED_IMAGE_MIMETYPES
    elif file_type == 'document':
        allowed_ext = ALLOWED_DOCUMENT_EXTENSIONS
        allowed_mime = ALLOWED_DOCUMENT_MIMETYPES
    else:
        return False, 'Tipo de archivo no soportado'
    
    filename = secure_filename(file_storage.filename or '')
    ext = get_extension(filename)
    if ext not in allowed_ext:
        return False, f'Extensión .{ext} no permitida. Permitidas: {", ".join(allowed_ext)}'
    
    # Read first 2KB for MIME detection
    header = file_storage.read(2048)
    file_storage.seek(0)
    
    # Simple magic byte checks
    mime_type = None
    if header[:4] == b'%PDF':
        mime_type = 'application/pdf'
    elif header[:8] == b'\x89PNG\r\n\x1a\n':
        mime_type = 'image/png'
    elif header[:2] == b'\xff\xd8':
        mime_type = 'image/jpeg'
    elif header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        mime_type = 'image/webp'
    elif header[:6] in (b'GIF87a', b'GIF89a'):
        mime_type = 'image/gif'
    
    if mime_type is None or mime_type not in allowed_mime:
        return False, f'Tipo de contenido no válido. Se esperaba: {", ".join(allowed_mime)}'
    
    return True, filename

def save_file(file_storage: FileStorage, upload_folder: str, subfolder: str) -> tuple[str, str, int]:
    original_name = secure_filename(file_storage.filename or 'file')
    ext = get_extension(original_name)
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    target_dir = os.path.join(upload_folder, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, unique_name)
    file_storage.save(target_path)
    file_size = os.path.getsize(target_path)
    relative_url = f'/uploads/{subfolder}/{unique_name}'
    return relative_url, original_name, file_size
