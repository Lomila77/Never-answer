import os
import json
import mimetypes


def get_file_list(directory_path: str) -> list[str]:
    return os.listdir(directory_path)


def get_json_content(json_file: str) -> dict:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_all_json_content(directory_path: str) -> list[dict]:
    jsons_paths = get_file_list(directory_path)
    content = []
    for json_file in jsons_paths:
        full_path = os.path.join(directory_path, json_file)
        content.append(get_json_content(full_path))
    return content


def is_wav_file(filename: str = None, mime_type: str = None) -> bool:
    """
    Vérifie si le fichier est bien un WAV selon l'extension et/ou le type MIME.
    """
    wav_mime_types = {"audio/wav", "audio/x-wav", "audio/wave", "audio/x-pn-wav"}
    wav_extensions = {".wav"}

    # Vérification par extension
    if filename:
        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
        if f".{ext}" in wav_extensions:
            return True

    # Vérification par type MIME
    if mime_type and mime_type.lower() in wav_mime_types:
        return True

    # Tentative de déduction par mimetypes (si filename fourni)
    if filename:
        guessed_type, _ = mimetypes.guess_type(filename)
        if guessed_type in wav_mime_types:
            return True

    return False


def is_wav_bytes(audio_bytes: bytes) -> bool:
    """
    Vérifie si les bytes correspondent à un fichier WAV (header RIFF/WAVE).
    """
    if not isinstance(audio_bytes, (bytes, bytearray)):
        return False
    if len(audio_bytes) < 12:
        return False
    # Vérifie le header RIFF et WAVE
    return (
        audio_bytes[0:4] == b'RIFF'
        and audio_bytes[8:12] == b'WAVE'
    )
