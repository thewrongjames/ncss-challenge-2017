from generate_patches import generate_patches


PAINT = '%'
GROUND = '.'


patches = []
with open('patches.txt') as patches_file:
    width = 0

    for line in patches_file:
        line_list = list(line.strip())

        if len(line_list) > width:
            width = len(line_list)

        patches.append(line_list)


for line_list in patches:
    for _ in range(len(line_list), width):
        line_list.append(GROUND)


# patches = generate_patches(1000, 1000, 0.6)


def get_adjacent_numbers(patches, row_index, column_index):
    adjacent_numbers = []

    for vertical_displacement in (-1, 0, 1):
        for horizontal_displacement in (-1, 0, 1):
            if vertical_displacement == 0 and horizontal_displacement == 0:
                continue

            vertical_index = row_index + vertical_displacement
            horizontal_index = column_index + horizontal_displacement
            if vertical_index < 0 or horizontal_index < 0:
                # (As negative indexes will work fine otherwise).
                continue

            try:
                adjacent_number = int(patches[vertical_index][horizontal_index])
            except (IndexError, ValueError):
                # Not in the space, or not an integer.
                continue
            else:
                adjacent_numbers.append(adjacent_number)

    return adjacent_numbers


patch_index = 0 # Some patches may have multiple indices.
for row_index, row in enumerate(patches):
    for column_index, cell in enumerate(row):
        if cell == GROUND:
            continue

        adjacent_numbers = get_adjacent_numbers(patches, row_index, \
            column_index)
        if adjacent_numbers:
            # This is in at least one already found patch, just give it the
            # number of the first one. They will be joined later.
            patches[row_index][column_index] = adjacent_numbers[0]
        else:
            # This is a new patch.
            patches[row_index][column_index] = patch_index
            patch_index += 1


def get_touching_indices(patches):
    """
    Returns a list of sets of the patch indices which are touching, though not
    necessarily all of them. This assumes all paint has been replaced with an
    index.
    """
    touching_indices = []

    for row_index, row in enumerate(patches):
        for column_index, cell in enumerate(row):
            if cell == GROUND:
                continue
            adjacent_numbers = get_adjacent_numbers(
                patches,
                row_index,
                column_index
            )
            for adjacent_number in adjacent_numbers:
                if cell != adjacent_number:
                    new_set = set((cell, adjacent_number))
                    if new_set not in touching_indices:
                        touching_indices.append(new_set)

    return touching_indices


touching_indices = get_touching_indices(patches)
while touching_indices:
    for touching_pairs in touching_indices:
        list_of_pair = list(touching_pairs)

        for row_index, row in enumerate(patches):
            for column_index in range(len(row)):
                if patches[row_index][column_index] == list_of_pair[0]:
                    patches[row_index][column_index] = list_of_pair[1]

    touching_indices = get_touching_indices(patches)


remaining_indicies = set()
for row_index, row in enumerate(patches):
    for column_index, cell in enumerate(row):
        if cell != GROUND:
            remaining_indicies.add(cell)


# for line in patches:
#     print(''.join([str(item) for item in line]))


patch_count = len(remaining_indicies)
print('{} patch{}'.format(patch_count, 'es' if patch_count != 1 else ''))
