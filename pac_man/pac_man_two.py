from copy import deepcopy


MAZE_DIRECTORY = 'maze.txt'
GHOST = 'G'
WALL = '#'
PAC_MAN = 'P'
DEAD_PAC_MAN = 'X'
PAC_DOT = '.'
EMPTY_SPACE = ' '
UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)
RIGHT = (0, 1)
DIRECTION_SELECTION_ORDER = (UP, LEFT, DOWN, RIGHT)
UP_COMMAND = 'U'
DOWN_COMMAND = 'D'
LEFT_COMMAND = 'L'
RIGHT_COMMAND = 'R'
DISPLAY_COMMAND = 'O'
DIRECTION_OF_COMMAND = {
    UP_COMMAND: UP,
    DOWN_COMMAND: DOWN,
    LEFT_COMMAND: LEFT,
    RIGHT_COMMAND: RIGHT
}


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


def pre_process_maze(maze):
    """
    Extracts the coordinates of packman and each of the ghosts from the maze
    and returns them separately.
    """
    new_maze = deepcopy(maze)

    coordinates_of_ghosts = []
    for row_index, row in enumerate(maze):
        for column_index, value in enumerate(row):
            if value == GHOST:
                coordinates_of_ghosts.append((row_index, column_index))
                new_maze[row_index][column_index] = EMPTY_SPACE
            if value == PAC_MAN:
                pac_man_coordinates = (row_index, column_index)
                new_maze[row_index][column_index] = EMPTY_SPACE

    return new_maze, pac_man_coordinates, coordinates_of_ghosts


maze, pac_man_coordinates, coordinates_of_ghosts = pre_process_maze(maze)


def get_game_over_state(maze, pac_man_coordinates, coordinates_of_ghosts):
    """
    Returns a tuple: player_has_died, player_has_won.
    """
    player_has_died = pac_man_coordinates in coordinates_of_ghosts

    player_has_won = True
    for row in maze:
        for cell_index, cell in enumerate(row):
            if cell == PAC_DOT:
                player_has_won = False

    if player_has_died: player_has_won = False

    return player_has_died, player_has_won


def display_game_state(
        points,
        maze,
        pac_man_coordinates,
        coordinates_of_ghosts
):
    player_has_died, player_has_won = get_game_over_state(
        maze,
        pac_man_coordinates,
        coordinates_of_ghosts
    )
    if player_has_died: print('You died!')
    if player_has_won: print('You won!')

    maze_to_display = deepcopy(maze)
    for ghost_coordinates in coordinates_of_ghosts:
        maze_to_display[ghost_coordinates[0]][ghost_coordinates[1]] = GHOST

    maze_to_display[pac_man_coordinates[0]][pac_man_coordinates[1]] = (
        DEAD_PAC_MAN if player_has_died else PAC_MAN
    )

    print('Points: ' + str(points))
    for row in maze_to_display:
        print(''.join(row))


def iterate_turn(
        points,
        maze,
        pac_man_coordinates,
        coordinates_of_ghosts,
        command
):
    new_maze = deepcopy(maze)
    new_points = points

    new_pac_man_coordinates = (
    pac_man_coordinates[0] + DIRECTION_OF_COMMAND[command][0],
    pac_man_coordinates[1] + DIRECTION_OF_COMMAND[command][1]
    )

    next_location = maze[new_pac_man_coordinates[0]][new_pac_man_coordinates[1]]
    if next_location == WALL:
        new_pac_man_coordinates = pac_man_coordinates
    elif next_location == PAC_DOT:
        new_points += 1
        new_maze[new_pac_man_coordinates[0]][new_pac_man_coordinates[1]] = \
            EMPTY_SPACE

    player_has_died, player_has_won = get_game_over_state(
            new_maze,
            new_pac_man_coordinates,
            coordinates_of_ghosts
    )
    if True in (player_has_died, player_has_won):
        # If thep player has one, then any pac dots just consumed count. If the
        # player has lost, then they do not.
        return (
            new_points if player_has_won else points,
            new_maze,
            new_pac_man_coordinates,
            coordinates_of_ghosts
        )

    new_coordinates_of_ghosts = []
    for ghost_coordinates in coordinates_of_ghosts:
        shortest_paths = get_shortest_paths(
            maze,
            ghost_coordinates,
            pac_man_coordinates
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
    return (
        new_points,
        new_maze,
        new_pac_man_coordinates,
        new_coordinates_of_ghosts
    )


points = 0
commands = input('Commands: ').split()
for command in commands:
    if command == DISPLAY_COMMAND:
        display_game_state(
            points,
            maze,
            pac_man_coordinates,
            coordinates_of_ghosts
        )
        continue

    points, maze, pac_man_coordinates, coordinates_of_ghosts = iterate_turn(
        points,
        maze,
        pac_man_coordinates,
        coordinates_of_ghosts,
        command
    )

    if True in get_game_over_state(
            maze,
            pac_man_coordinates,
            coordinates_of_ghosts
    ):
        display_game_state(
            points,
            maze,
            pac_man_coordinates,
            coordinates_of_ghosts
        )
        break

if not (
        True in get_game_over_state(
            maze,
            pac_man_coordinates,
            coordinates_of_ghosts
        )
):
    display_game_state(
        points,
        maze,
        pac_man_coordinates,
        coordinates_of_ghosts
    )
