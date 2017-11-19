MAZE_DIRECTORY = 'maze.txt'
GHOST = 'G'
WALL = '#'
PACK_MAN = 'P'
PACK_DOT = '.'
EMPTY_SPACE = ' '
UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)
RIGHT = (0, 1)
DIRECTION_SELECTION_ORDER = (UP, LEFT, DOWN, RIGHT)


def get_shortest_paths(maze, from_coordinates, to_coordinates):
    """
    An implementation of a breadth first search that keeps searching after it
    finds the shortest route, to find all the shortest routes, and returns a
    list of them.
    """
    paths_to_check = [[from_coordinates]]
    seen_coordinates = []
    shortest_paths = []
    # This first path found will be know to be of the shortest possible length,
    # any found after that will only be included if they are of the same
    # length.
    while paths_to_check:
        path = paths_to_check.pop(0)

        if path[-1] == to_coordinates:
            # The paths ends at the target
            if not shortest_paths or len(shortest_paths[0]) == len(path):
                # If this is the first solution found, or it is the same length
                # as the first solution found.
                shortest_paths.append(path)

        if path[-1] in seen_coordinates:
            # We've been here before...
            continue

        seen_coordinates.append(path[-1])

        possible_possible_next_positions = []
        for direction in DIRECTION_SELECTION_ORDER:
            # (Though, the order is not important here).
            possible_possible_next_positions.append(
                (path[-1][0] + direction[0], path[-1][1] + direction[1])
            )
        for position in possible_possible_next_positions:
            if maze[position[0]][position[1]] != WALL and position not in path:
                paths_to_check.append(path + [position])

    return shortest_paths


maze = []
with open(MAZE_DIRECTORY) as maze_file:
    for line in maze_file:
        maze.append(list(line.strip()))


coordinates_of_ghosts = []
for row_index, row in enumerate(maze):
    for column_index, value in enumerate(row):
        if value == GHOST:
            coordinates_of_ghosts.append((row_index, column_index))
        if value == PACK_MAN:
            pack_man_coordinates = (row_index, column_index)


new_coordinates_of_ghosts = []
for ghost_coordinates in coordinates_of_ghosts:
    shortest_paths = get_shortest_paths(
        maze,
        ghost_coordinates,
        pack_man_coordinates
    )
    first_directions = [
        (
            path[1][0] - ghost_coordinates[0],
            path[1][1] - ghost_coordinates[1]
        ) for path in shortest_paths
    ]

    for direction in DIRECTION_SELECTION_ORDER:
        if direction in first_directions:
            new_coordinates_of_ghosts.append(
                (
                    direction[0] + ghost_coordinates[0],
                    direction[1] + ghost_coordinates[1]
                )
            )
            break


new_maze = maze.copy()
for ghost_coordinates in coordinates_of_ghosts:
    new_maze[ghost_coordinates[0]][ghost_coordinates[1]] = EMPTY_SPACE
for new_ghost_coordinates in new_coordinates_of_ghosts:
    new_maze[new_ghost_coordinates[0]][new_ghost_coordinates[1]] = GHOST
for row in new_maze:
    print(''.join(row))
