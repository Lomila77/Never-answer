import os
import json


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


def is_wav_bytes(audio_bytes: bytes) -> bool:
    """
    檢查音頻數據是否為WAV格式。
    
    Args:
        audio_bytes: 要檢查的音頻數據
        
    Returns:
        如果是WAV格式則返回True，否則返回False
    """
    # WAV文件的標頭應該以"RIFF"開始，並在第8-12字節包含"WAVE"
    if len(audio_bytes) < 12:
        return False
    
    # 檢查RIFF標頭
    if audio_bytes[:4] != b'RIFF':
        return False
    
    # 檢查WAVE格式
    if audio_bytes[8:12] != b'WAVE':
        return False
    
    return True
