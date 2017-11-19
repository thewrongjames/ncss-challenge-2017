import re
from functools import wraps


WHITE_CELL = '.'
BLACK_UNNUMBERED_CELL = 'X'
NUMBERED_BLACK_CELLS = ['0', '1', '2', '3', '4']
BLACK_CELLS = [BLACK_UNNUMBERED_CELL] + NUMBERED_BLACK_CELLS
LAMP_CELL = 'L'


"""
All functions below assume that:
    Every row on a particular board has the same number of cells as every other
        row.
"""


def number_of_columns_in_board(board):
    # As boards can have rows or columns, we may not be able to index the first
    # row to find that the length of the columns is zero
    return len(board[0]) if board else 0


def get_columns(board):
    # Board is a list of strings which represent rows, below is a list of
    # strings that represent the columns.
    return [''.join([row[index] for row in board]) for index in #
        range(number_of_columns_in_board(board))]


def no_lamps_in_line_of_sight_of_each_other(board):
    for line in board + get_columns(board):
        lines_of_sight = re.split('|'.join(BLACK_CELLS), line)
        for line_of_sight in lines_of_sight:
            if line_of_sight.count(LAMP_CELL) > 1:
                return False

    return True


def coordinates_on_board(board, row_index, column_index):
    return (
        0 <= row_index < len(board)
        and 0 <= column_index < number_of_columns_in_board(board)
    )


def content_of_adjacent_cells(board, row_index, column_index):
    adjacent_cells_coordinates = []
    for position_change in (-1, 1):
        adjacent_cells_coordinates.append((row_index + position_change, column_index))
        adjacent_cells_coordinates.append((row_index, column_index + position_change))

    content_of_adjacent_cells = []
    for adjacent_row_index, adjacent_column_index in adjacent_cells_coordinates:
        if coordinates_on_board(
                board,
                adjacent_row_index,
                adjacent_column_index
        ):
            content_of_adjacent_cells.append(
                board[adjacent_row_index][adjacent_column_index]
            )

    return content_of_adjacent_cells


# Due to this wrapper the two functions below it may look counter intuitive,
# sorry, this seemed the best way to do it.
def for_numbered_black_cells_return_false_if_number_of_lamps(function):
    @wraps(function)
    def wrapper(board):
        for row_index, row in enumerate(board):
            for column_index, cell in enumerate(row):
                if not (cell in NUMBERED_BLACK_CELLS):
                    continue

                number_of_lamps = 0
                for adjacent_cell in content_of_adjacent_cells(board, \
                        row_index, column_index):
                    number_of_lamps += 1 if adjacent_cell == LAMP_CELL else 0

                if function(number_of_lamps, cell):
                    return False
        return True

    return wrapper


@for_numbered_black_cells_return_false_if_number_of_lamps
def numbered_black_cells_dont_have_too_many_lamps(number_of_lamps, cell):
    return number_of_lamps > int(cell)


@for_numbered_black_cells_return_false_if_number_of_lamps
def numbered_black_cells_have_right_number_of_lamps(number_of_lamps, cell):
    return number_of_lamps != int(cell)


def lamp_in_line_line_of_sight(line, position_in_line):
    line_of_sight = [line[position_in_line]]

    for position_to_check in range(position_in_line, len(line)):
        if line[position_to_check] in BLACK_CELLS:
            break
        line_of_sight.append(line[position_to_check])

    for position_to_check in range(position_in_line, -1, -1):
        if line[position_to_check] in BLACK_CELLS:
            break
        line_of_sight.insert(0, line[position_to_check])

    return LAMP_CELL in line_of_sight


def white_cell_is_illuminated(board, row_index, column_index):
    if board[row_index][column_index] != WHITE_CELL:
        raise ValueError(
            'cell at (row_index, column_index) is not a white cell.'
        )

    row, column = board[row_index], get_columns(board)[column_index]
    return (
        lamp_in_line_line_of_sight(line=row, position_in_line=column_index)
        or lamp_in_line_line_of_sight(line=column, position_in_line=row_index)
    )


def all_white_cells_are_illuminated(board):
    for row_index, row in enumerate(board):
        for column_index, cell in enumerate(row):
            if (
                    cell == WHITE_CELL
                    and not white_cell_is_illuminated(
                        board,
                        row_index,
                        column_index
                    )
            ):
                return False
    return True


def board_is_happy(board):
    return (
        no_lamps_in_line_of_sight_of_each_other(board)
        and numbered_black_cells_dont_have_too_many_lamps(board)
    )


def board_is_solved(board):
    return (
        board_is_happy(board)
        and numbered_black_cells_have_right_number_of_lamps(board)
        and all_white_cells_are_illuminated(board)
    )


def get_board_state(board):
    if board_is_happy(board):
        if board_is_solved(board):
            return 'solved'
        else:
            return 'happy'
    else:
        return 'unhappy'


if __name__ == '__main__':
    # Example board, happy state.
    print(get_board_state('''
...1.0.
X......
..X.X..
X...L.X
..X.3..
.L....X
L3L2...'''.strip().split('\n')))
    # Example board, solved state.
    print(get_board_state('''
..L1.0.
X...L..
L.X.X.L
X...L.X
..XL3L.
.L....X
L3L2L..'''.strip().split('\n')))
    # Example board, unhappy state.
    print(get_board_state('''
L..1L0.
X.L....
L.X.X.L
X...L.X
..XL3L.
.L....X
L3L2L..'''.strip().split('\n')))
    # Different board, happy state.
    print(get_board_state('''
L1.L.
..L3L
..X1.
.1...
.....'''.strip().split('\n')))
