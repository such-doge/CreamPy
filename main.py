import argparse
import os
from PIL import Image
from cream import MCU, compare_images, process_folder, image_difference, process_numpys
import imageio
import time


adjacency_list = {}

parser = argparse.ArgumentParser(description='Analyze images for duplicate blocks.',
                                 epilog="Don't fuck up.")
parser.add_argument('-d', '--directory', dest='directory',
                    help='Directory of images to be compressed.')
# parser.add_argument('-f', '--format', dest='format', help='Specify format as JPEG or PNG')
# parser.add_argument('-x', '--dry-run', dest='dry_run', help="Don't actually write any files.")
# parser.add_argument('-L', '--lossy', dest='lossy',
#                     help="Use this option to blend JPEGs that have artifacts that prevent " +
#                          "8x8 blocks from being recognized as identical when in fact they are.")
# parser.add_argument('-n', '--skip', dest='n',
#                     help="Only check 1/n blocks in the initial comparisons")

arguments = parser.parse_args()
files = os.listdir(arguments.directory)
os.chdir(arguments.directory)

input_files = []

# Process images through PIL
# for file in files:
#     if file.endswith('.jpg') or file.endswith('.png'):
#         input_files.append(Image.open(file))
#
# starttime = time.clock()
# picture_groups = process_folder(input_files)
# endtime = time.clock()
#
# del input_files
# input_files = []

filenames = []
for file in files:
    if file.endswith('.jpg') or file.endswith('.png'):
        input_files.append(imageio.imread(file))
        filenames.append(file)

numpy_arrays_with_names = dict(zip(filenames, input_files))

starttime2 = time.clock()
picture_groups = process_numpys(input_files)
endtime2 = time.clock()
print("Time to execute: " + str(endtime - starttime) + " seconds")
print("Time to execute: " + str(endtime2 - starttime2) + " seconds")


input("Press Enter to continue...")
