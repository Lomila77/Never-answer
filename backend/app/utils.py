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
