from PIL import Image
import argparse


class MCU:
    def __init__(self, low, high):
        self.current = low
        self.high = high
        self.true_high = int(self.high / 8) * 8
        if self.high % 8 > 0:
            self.true_high += 8

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.true_high:
            raise StopIteration
        elif self.current == self.true_high:
            self.current += 8
            return self.high
        elif self.current < self.true_high:
            self.current += 8
            return self.current - 8


def compare_images(image_a, image_b):
    even_counter = 0
    if image_a.size != image_b.size:
        print(image_a.filename + " is not similar to " + image_b.filename)
        return False, 0, 0
    else:
        print("Comparing:" + image_a.filename + " & " + image_b.filename)
        same_blocks = 0
        different_blocks = 0
        for right in MCU(8, image_a.size[0]):
            for bottom in MCU(8, image_a.size[1]):
                even_counter += 1
                # Only evaluate every nth block
                if even_counter % 100:
                    continue
                right_subtract = right % 8 if right % 8 else 8
                bottom_subtract = bottom % 8 if bottom % 8 else 8
                if bottom_subtract:
                    region = (right - right_subtract, bottom - bottom_subtract, right, bottom)
                    region_a = image_a.crop(region)
                    region_b = image_b.crop(region)
                    # if right % 8 > 0 or bottom % 8 > 0:
                    #     print(region)
                    #     print(region_a == region_b)
                    if region_a == region_b:
                        same_blocks += 1
                    else:
                        different_blocks += 1
        print("Same blocks " + str(same_blocks) + ", " + "Different blocks: " + str(different_blocks))
        if same_blocks / (same_blocks + different_blocks) > 0.05:
            print("Similarity % exceeded 0.05")
            return True, same_blocks, different_blocks
        else:
            return False, 0, 0


def process_folder(input_files):
    picture_groups = []
    for input_image in input_files:
        print(input_image.filename)
        similar = False
        # Present the list in reverse because the most similar group is most likely the last one.
        # It saves about 25% on time overall.
        for group in picture_groups[::-1]:
            similar, same_blocks, different_blocks = compare_images(group[0], input_image)
            if similar:
                group.append(input_image)
                # If this is not the group's first image, close it for now
                if len(group) > 1:
                    input_image.close()
                break
        if similar:
            continue
        else:
            picture_groups.append([input_image])
    # print(picture_groups)
    groupid = 0

    for group in picture_groups:
        print("Group ID:" + str(groupid))
        for img in group:
            print("Picture: " + img.filename)
            img.close()
        groupid += 1

    return picture_groups

