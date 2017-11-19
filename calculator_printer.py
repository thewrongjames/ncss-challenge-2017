NUMBERS = {
    0: [
        ' - ',
        '|?|',
        ' ? ',
        '|?|',
        ' - ',
    ],
    1: [
        ' ? ',
        ' ?|',
        ' ? ',
        ' ?|',
        ' ? ',
    ],
    2: [
        ' - ',
        ' ?|',
        ' - ',
        '|? ',
        ' - ',
    ],
    3: [
        ' - ',
        ' ?|',
        ' - ',
        ' ?|',
        ' - ',
    ],
    4: [
        ' ? ',
        '|?|',
        ' - ',
        ' ?|',
        ' ? ',
    ],
    5: [
        ' - ',
        '|? ',
        ' - ',
        ' ?|',
        ' - ',
    ],
    6: [
        ' - ',
        '|? ',
        ' - ',
        '|?|',
        ' - ',
    ],
    7: [
        ' - ',
        ' ?|',
        ' ? ',
        ' ?|',
        ' ? ',
    ],
    8: [
        ' - ',
        '|?|',
        ' - ',
        '|?|',
        ' - ',
    ],
    9: [
        ' - ',
        '|?|',
        ' - ',
        ' ?|',
        ' - ',
    ],
}

number = input('Number: ')
width = int(input('Width: '))

rows_before_vertical_multiplication = [
    ' '.join(
        [NUMBERS[int(digit)][row_index] for digit in number]
    ).replace('-', '-' * width).replace('?', ' ' * width)
    for row_index in range(5)
]
all_rows = []
for index, row in enumerate(rows_before_vertical_multiplication):
    if index not in [1, 3]:
        all_rows.append(row)
        continue
    for _ in range(width):
        all_rows.append(row)
print('\n'.join(all_rows))
