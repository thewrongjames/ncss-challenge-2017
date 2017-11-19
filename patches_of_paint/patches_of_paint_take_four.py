# from generate_patches import generate_patches


PAINT = '%'
GROUND = '.'


patches = []
with open('patches.txt') as patches_file:
    WIDTH = 0

    for line in patches_file:
        line_list = list(line.strip())

        if len(line_list) > WIDTH:
            WIDTH = len(line_list)

        patches.append(line_list)


for line_list in patches:
    for _ in range(len(line_list), WIDTH):
        line_list.append(GROUND)


# patches = generate_patches(12, 11000, 0.5)


HEIGHT = len(patches)
# try:
#     WIDTH = len(patches[0])
# except IndexError:
#     WIDTH = 0


patch_count = 0
for row_index, row in enumerate(patches):
    for column_index, cell in enumerate(row):
        if cell != PAINT:
            continue

        patch_count += 1

        frontier_cells = set([(row_index, column_index)])

        while frontier_cells:
            cell_to_expand = frontier_cells.pop()

            patches[cell_to_expand[0]][cell_to_expand[1]] = patch_count

            for child in (
                    (cell_to_expand[0] - 1, cell_to_expand[1] - 1),
                    (cell_to_expand[0] - 1, cell_to_expand[1]),
                    (cell_to_expand[0] - 1, cell_to_expand[1] + 1),
                    (cell_to_expand[0], cell_to_expand[1] - 1),
                    (cell_to_expand[0], cell_to_expand[1] + 1),
                    (cell_to_expand[0] + 1, cell_to_expand[1] - 1),
                    (cell_to_expand[0] + 1, cell_to_expand[1]),
                    (cell_to_expand[0] + 1, cell_to_expand[1] + 1)
            ):
                if not 0 <= child[0] < HEIGHT or not 0 <= child[1] < WIDTH:
                    continue

                if (patches[child[0]][child[1]] == PAINT):
                    frontier_cells.add(child)


print('{} patch{}'.format(patch_count, 'es' if patch_count != 1 else ''))
