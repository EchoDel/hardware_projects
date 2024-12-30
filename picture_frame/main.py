from pathlib import Path

import PySimpleGUI as sg
from tqdm import tqdm

from picture_frame.config_management import get_program_config, load_photo_config, sample_config_random, \
    save_config_file, sample_config_maintain_folder, ProgramConfig

config_path = Path('picture_frame/config.json')


def main(photos_config: dict, program_config: ProgramConfig):
    from picture_frame.UI import convert_to_bytes, G_SIZE, graph, window
    previous_image = ""
    keep_going = True
    while keep_going:
        if program_config['sampling_strategy'] == 'folder':
            file_to_display = sample_config_maintain_folder(photos_config, program_config)
        else:
            file_to_display = sample_config_random(photos_config)

        print(file_to_display)

        if not previous_image == file_to_display:
            try:
                img_data, img_width, img_height = convert_to_bytes(str(file_to_display), resize=G_SIZE)

                if 'image_id' in locals():
                    graph.delete_figure(image_id)

                image_id = graph.draw_image(data=img_data,
                                            location=((G_SIZE[0] - img_width) / 2,
                                                      G_SIZE[1]))
                previous_image = file_to_display
            except Exception as E:
                print(E)
                photos_config[file_to_display] = 0
                save_config_file(program_config['photos_config'], photos_config)
                continue

        for x in range(program_config['seconds_to_show'] * 10):
            event, values = window.read(timeout=100)
            if event in (sg.WINDOW_CLOSED, "-ESCAPE-"):
                keep_going = False
                break

    window.close()


if __name__ == "__main__":
    # Read the photos to display
    program_config = (
        get_program_config(config_path))
    photos_config = load_photo_config(program_config)
    # photos_config = {key: value for key, value in photos_config.items() if '2019_Bristol' in str(key)}
    main(photos_config, program_config)
