import json
import random
from pathlib import Path
from typing import Iterable

CURRENT_FOLDER = None
SEEN_PICTURES = []
DISALLOWED_EXTENSION = ['.xmp', '.XMP', '.db', '.pp3']


def get_program_config(config_path: Path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    photo_folder = Path(config['photo_folder'])
    photos_config = Path(config['photos_config'])
    disallowed_folders = config['disallowed_folders']
    seconds_to_show = config['second_to_show']
    sampling_strategy = config['sampling_strategy']
    return photo_folder, photos_config, disallowed_folders, seconds_to_show, sampling_strategy


def load_folder(photo_sub_folder: Path, photos: dict):
    photo_sub_folder.is_dir()
    for photo_path in photo_sub_folder.glob('*'):
        if photo_path.is_dir():
            load_folder(photo_path, photos)
        if photo_path.suffix in DISALLOWED_EXTENSION:
            continue
        if photo_path not in photos:
            photos[photo_path] = 100


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
            load_folder(photo_sub_folder, photos)

    save_config_file(photos_config, photos)

    return photos


def save_config_file(photos_config_path: Path, photos_config: dict):
    photos_tmp = {}
    for key, value in photos_config.items():
        photos_tmp[str(key)] = value
    with open(photos_config_path, 'w') as f:
        json.dump(photos_tmp, f)


def sample_config_maintain_folder(config_dict: dict, new_folder: bool = False):
    global CURRENT_FOLDER
    global SEEN_PICTURES
    if CURRENT_FOLDER is None or random.random() < 0.05 or new_folder:
        CURRENT_FOLDER = choose_folder(config_dict)
        SEEN_PICTURES = []

    images_to_pick_from = {key: value for key, value in config_dict.items()
                           if get_root_folder(key) == CURRENT_FOLDER and key not in SEEN_PICTURES}
    if len(images_to_pick_from) == 0:
        image = sample_config_maintain_folder(config_dict, True)
    else:
        image = sample_config_random(images_to_pick_from)
    SEEN_PICTURES.append(image)
    print(SEEN_PICTURES)
    return image


def get_root_folder(photo_path: Path):
    return photo_path.parents[len(photo_path.parents) - 3]


def choose_folder(config_dict: dict):
    folders = {get_root_folder(x) for x in config_dict}
    folder = random.sample(list(folders), 1)[0]
    return folder


def sample_config_random(config_dict: dict):
    config = {key: random.random() * value for key, value in config_dict.items()}
    return max(config, key=config.get)
