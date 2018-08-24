import argparse
import os
from PIL import Image
from iterator import MCU, compare_images, process_folder
import time


adjacency_list = {}

parser = argparse.ArgumentParser(description='Analyze images for duplicate blocks.',
                                 epilog="Don't fuck up.")
parser.add_argument('-d', '--directory', dest='directory',
                    help='Directory of images to be compressed.')
# parser.add_argument('-f', '--format', dest='format', help='Specify format as JPEG or PNG')
# parser.add_argument('-x', '--dry-run', dest='dry_run', help="Don't actually write any files.")
# parser.add_argument('-L', '--lossy', dest='lossy', help="Blend 8x8 tiles in JPEGs
arguments = parser.parse_args()
files = os.listdir(arguments.directory)
os.chdir(arguments.directory)

input_files = []

for file in files:
    if file.endswith('.jpg') or file.endswith('.png'):
        input_files.append(Image.open(file))

starttime = time.clock()
picture_groups = process_folder(input_files)
endtime = time.clock()

print("Time to execute: " + str(endtime - starttime) + " seconds")
input("Press Enter to continue...")
