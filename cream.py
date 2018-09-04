from PIL import Image
import imageio
import numpy as np
import time


class MCU:
    def __init__(self, low, high):
        """ An iterator that increments by 8 between low and high. When high is not a multiple of 8,
            it returns high instead. Useful for generating pixel coordinates of MCU boundaries in
            JPEG images. """
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


def compare_images(image_a, image_b, skip=100):
    if image_a.size != image_b.size:
        # print(image_a.filename + " is not similar to " + image_b.filename)
        return False, 0, 0
    else:
        counter = 0
        print("Comparing:" + image_a.filename + " & " + image_b.filename)
        same_blocks = 0
        different_blocks = 0
        for right in MCU(8, image_a.size[0]):
            for bottom in MCU(8, image_a.size[1]):
                counter += 1
                # Only evaluate every nth block
                if counter % skip:
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


def image_difference(np_a, np_b):
    """Images are fed in as numpy arrays formatted as [Y, X, RGB]"""
    if np_a.shape != np_b.shape:
        return False, 0, 0
    else:
        counter = 0
        same_regions = []
        same_blocks = 0
        diff_blocks = 0
        max_x = np_a.shape[1] # 800
        max_y = np_a.shape[0] # 600
        for right in MCU(8, max_x): # 8 to 800
            for bottom in MCU(8, max_y): # 8 to 600
                counter += 1
                if counter % 100:
                    continue
                left = right - 8 if right % 8 == 0 else right - (right % 8)
                top = bottom - 8 if bottom % 8 == 0 else bottom - (bottom % 8)
                if False not in (np_a[top:bottom, left:right] == np_b[top:bottom, left:right]):
                    same_blocks += 1
                    same_regions.append((left, top, right, bottom))
                else:
                    diff_blocks += 1
        print("Same blocks: " + str(same_blocks) + ", Different blocks: " + str(diff_blocks))
        if same_blocks / (same_blocks + diff_blocks) > 0.05:
            return same_regions
            # return True, same_blocks, diff_blocks
        else:
            return False, 0, 0


def is_similar_lossy(image_a, image_b, skip=1, difference_threshold=12, similarity_threshold=0.05,
                     mode="lossy"):
    if image_a.shape != image_b.shape:
        return False, 0, 0
    else:
        counter = 0
        same_blocks = 0
        different_blocks = 0
        difference = abs(np.int16(image_a) - np.int16(image_b))
        same_regions = []
        for right in MCU(8, image_a.shape[1]):
            for bottom in MCU(8, image_a.shape[0]):
                counter += 1
                if counter % skip:
                    continue
                left = right - 8 if right % 8 == 0 else right - (right % 8)
                top = bottom - 8 if bottom % 8 == 0 else bottom - (bottom % 8)
                if mode == "lossy":
                    if difference[top:bottom, left:right].max() <= difference_threshold:
                        same_blocks += 1
                        same_regions.append((left, top, right, bottom))
                    else:
                        different_blocks += 1
                elif mode == "lossless":
                    if difference[top:bottom, left:right].max() == 0:
                        same_blocks += 1
                        same_regions.append((left, top, right, bottom))
                    else:
                        different_blocks += 1
        if same_blocks / (same_blocks + different_blocks) > similarity_threshold:
            # print(same_blocks)
            # print(different_blocks)
            return True, same_blocks, different_blocks, same_regions
        else:
            # print(same_blocks)
            # print(different_blocks)
            return False, same_blocks, different_blocks, same_regions


def is_similar_lossy_fast(image_a, image_b):
    result = is_similar_lossy(image_a, image_b, skip=12, mode="lossy")
    return result[0]


def similar_blocks_lossy(image_a, image_b):
    result = is_similar_lossy(image_a, image_b, skip=1, mode="lossy")
    return result[1]


def is_similar_lossless_fast(image_a, image_b):
    result = is_similar_lossy(image_a, image_b, skip=12, mode="lossless")
    return result[0]


def similar_blocks_lossless(image_a, image_b):
    result = is_similar_lossy(image_a, image_b, skip=1, mode="lossless")
    return result[1]
