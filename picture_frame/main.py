from pathlib import Path

from picture_frame.config_management import get_program_config, load_photo_config

config_path = Path('picture_frame/config.json')

# Read the photos to display
photo_folder, photos_config, disallowed_folders = get_program_config(config_path)
photos_config = load_photo_config(photo_folder, photos_config, disallowed_folders)




from PIL import Image

im = Image.open("//rhino/photos/photos/south_africa/_MG_2603.CR2")
im.show()
