import json
import random
from pathlib import Path
from typing import Iterable


def get_program_config(config_path: Path):
    with open(config_path, 'r') as f:
        config = json.load(f)
        photo_folder = Path(config['photo_folder'])
        photos_config = Path(config['photos_config'])
        disallowed_folders = config['disallowed_folders']
    return photo_folder, photos_config, disallowed_folders


def load_photo_config(photo_folder: Path, photos_config: Path, disallowed_folders: Iterable):
    if photos_config.exists():
        with open(photos_config, 'r') as f:
            photos_tmp = json.load(f)
            photos = {}
            for key, value in photos_tmp.items():
                photos[Path(key)] = value
    else:
        photos = {}

    for photo_sub_folder in photo_folder.glob('*'):
        if photo_sub_folder.stem in disallowed_folders:
            continue
        else:
            for photo_path in photo_sub_folder.glob('*'):
                photos[photo_path] = 100

    save_config_file(photos_config, photos)

    return photos


def save_config_file(photos_config_path: Path, photos_config: dict):
    photos_tmp = {}
    for key, value in photos_config.items():
        photos_tmp[str(key)] = value
    with open(photos_config_path, 'w') as f:
        json.dump(photos_tmp, f)


def sample_config(config_dict: dict):
    config = {key: random.random() * value for key, value in config_dict.items()}
    return max(config, key=config.get)
