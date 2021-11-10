import argparse
import numpy as np
import pandas as pd
from skimage import io
from tqdm.autonotebook import tqdm
from pathlib import Path
import csv

import color_extractor
from color_extractor import ImageToColor

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--img_folder_path",
        required=True,
        help="Path to folder with images from which to get color"
        )
    parser.add_argument(
        "--output_csv_path",
        required=True,
        help="Path where to save file with results"
        )
    args = parser.parse_args()
    return args

def main(img_folder_path, output_csv_path):
    '''
    Extracts hex color from each image in a folder, results are saved to a csv file
    '''
    settings = {'debug': {}}
    npz = np.load('color_names.npz')
    img_to_color = ImageToColor(npz['samples'], npz['labels'], settings)
    fls = sorted(list(Path(img_folder_path).glob("*.jpg")))

    open(output_csv_path, 'w').close()
    with open(output_csv_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['fname', "hex_color"])
        writer.writeheader()
        for fl in tqdm(fls):
            img = io.imread(fl)
            hex_colors = ", ".join(img_to_color.get_hex_colors(img))
            writer.writerow({'fname': fl.name, "hex_color": hex_colors})
    
    return res

if __name__ == "__main__":
    args = _parse_args()
    main(
        args.img_folder_path,
        args.output_csv_path
        )