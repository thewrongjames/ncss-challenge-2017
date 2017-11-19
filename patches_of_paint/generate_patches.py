from random import random


PAINT = '%'
GROUND = '.'


def generate_patches(width, height, ground_to_paint_ratio=0.5):
    patches = []
    for _ in range(height):
        row = []

        for _ in range(width):
            row.append(PAINT if random() > ground_to_paint_ratio else GROUND)

        patches.append(row)

    return patches
