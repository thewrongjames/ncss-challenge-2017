from PIL import Image


# Everything below assumes everything is either black or white.


def get_image_with_one_dimension_of_whitespace_removed(image, vertically):
    hit_black_yet = False

    # Note order is opposite to below function.
    if vertically:
        dimension_order = (image.width, image.height)
    else:
        dimension_order = (image.height, image.width)

    for a in range(dimension_order[0]):
        for b in range(dimension_order[1]):
            if not image.getpixel((a, b) if vertically else (b, a)):
                # Just hit a black pixel
                if hit_black_yet:
                    last_hit_black = a
                else:
                    hit_black_yet = True
                    first_hit_black = a
                break

    if vertically:
        rectangle = (first_hit_black, 0, last_hit_black + 1, dimension_order[1])
    else:
        rectangle = (0, first_hit_black, dimension_order[1], last_hit_black + 1)

    return image.crop(rectangle)


def get_sections(image, separate_vertically):
    hit_black_since_last_section = False
    sections = []
    current_section_start = 0

    if separate_vertically:
        dimension_order = (image.height, image.width)
    else:
        dimension_order = (image.width, image.height)

    for a in range(dimension_order[0]):
        hit_black_in_this_section = False

        for b in range(dimension_order[1]):
            if not image.getpixel(
                    (b, a) if separate_vertically else (a, b)
            ):
                # This pixel is black
                hit_black_in_this_section = True
                hit_black_since_last_section = True
                break

        if not hit_black_since_last_section:
            current_section_start = a + 1
            continue

        if not hit_black_in_this_section:
            if separate_vertically:
                rectangle = (0, current_section_start, dimension_order[1], a)
            else:
                rectangle = (current_section_start, 0, a, dimension_order[1])
            sections.append(
                get_image_with_one_dimension_of_whitespace_removed(
                    image.crop(rectangle),
                    vertically=separate_vertically
                )
            )
            current_section_start = a + 1
            hit_black_since_last_section = False

    if dimension_order[0] > current_section_start:
        # There is another section, that doesn't have any white after it...
        if separate_vertically:
            rectangle = (
                0,
                current_section_start,
                dimension_order[1],
                dimension_order[0]
            )
        else:
            rectangle = (
                current_section_start,
                0,
                dimension_order[0],
                dimension_order[1]
            )
        sections.append(
            get_image_with_one_dimension_of_whitespace_removed(
                image.crop(rectangle),
                vertically=separate_vertically
            )
        )

    return sections


# The below has_x functions could probably have been condensed, but, I am
# running out of time.


def has_dot(image):
    half_width = int(image.width / 2)
    half_height = int(image.height / 2)
    return bool(
        not image.getpixel((int(image.width / 2), int(image.height / 2))) or
        not image.getpixel((int(image.width / 2) - 1, int(image.height / 2))) or
        not image.getpixel((int(image.width / 2), int(image.height / 2) - 1)) or
        not image.getpixel((int(image.width / 2) + 1, int(image.height / 2))) or
        not image.getpixel((int(image.width / 2), int(image.height / 2) + 1))
    )


def has_top_point(image):
    black_centre = not image.getpixel((int(image.width / 2), 0)) or \
        not image.getpixel((int(image.width / 2) - 1, 0))
    white_surroundings = image.getpixel((int(image.width / 2) - 2, 0)) and \
        image.getpixel((int(image.width / 2) + 1, 0))
    return bool(black_centre and white_surroundings)


def has_right_point(image):
    black_centre = not image.getpixel((image.width - 1, int(image.height / 2)))\
        or not image.getpixel((image.width - 1, int(image.height / 2) - 1))
    white_surroundings = (
        image.getpixel((image.width - 1, int(image.height / 2) - 2)) and
        image.getpixel((image.width - 1, int(image.height / 2) + 1))
    )
    return bool(black_centre and white_surroundings)


def has_bottom_point(image):
    black_centre = not image.getpixel((int(image.width / 2), image.height - 1))\
        or not image.getpixel((int(image.width / 2) - 1, image.height - 1))
    white_surroundings = (
        image.getpixel((int(image.width / 2) - 2, image.height - 1)) and
        image.getpixel((int(image.width / 2) + 1, image.height - 1))
    )
    return bool(black_centre and white_surroundings)


def has_left_point(image):
    black_centre = not image.getpixel((0, int(image.height / 2))) or \
        not image.getpixel((0, int(image.height / 2) - 1))
    white_surroundings = image.getpixel((0, int(image.height / 2) - 2)) and \
        image.getpixel((0, int(image.height / 2) + 1))
    return bool(black_centre and white_surroundings)


def has_top_right_corner(image):
    return bool(
        not image.getpixel((image.width - 2, 0)) and
        not image.getpixel((image.width - 1, 0)) and
        not image.getpixel((image.width - 1, 1))
    )


def has_bottom_right_corner(image):
    return bool(
        not image.getpixel((image.width - 1, image.height - 2)) and
        not image.getpixel((image.width - 1, image.height - 1)) and
        not image.getpixel((image.width - 2, image.height - 1))
    )


def has_bottom_left_corner(image):
    return bool(
        not image.getpixel((1, image.height - 1)) and
        not image.getpixel((0, image.height - 1)) and
        not image.getpixel((0, image.height - 2))
    )


def has_top_left_corner(image):
    return bool(
        not image.getpixel((0, 1)) and
        not image.getpixel((0, 0)) and
        not image.getpixel((1, 0))
    )


def get_from_image_character(image):
    # This should be indexed with a tuple in the form:
    # (
    #     has_dot,
    #     has_top_point,
    #     has_right_point,
    #     has_bottom_point,
    #     has_left_point,
    #     has_top_right_corner,
    #     has_bottom_right_corner,
    #     has_bottom_left_corner,
    #     has_top_left_corner
    # )
    character_from_characteristics = {
        (False, False, False, False, False, False, True, False, False): 'A',
        (False, False, False, False, False, False, True, True, False): 'B',
        (False, False, False, False, False, False, False, True, False): 'C',
        (False, False, False, False, False, True, True, False, False): 'D',
        (False, False, False, False, False, True, True, True, True): 'E',
        (False, False, False, False, False, False, False, True, True): 'F',
        (False, False, False, False, False, True, False, False, False): 'G',
        (False, False, False, False, False, True, False, False, True): 'H',
        (False, False, False, False, False, False, False, False, True): 'I',

        (True, False, False, False, False, False, True, False, False): 'J',
        (True, False, False, False, False, False, True, True, False): 'K',
        (True, False, False, False, False, False, False, True, False): 'L',
        (True, False, False, False, False, True, True, False, False): 'M',
        (True, False, False, False, False, True, True, True, True): 'N',
        (True, False, False, False, False, False, False, True, True): 'O',
        (True, False, False, False, False, True, False, False, False): 'P',
        (True, False, False, False, False, True, False, False, True): 'Q',
        (True, False, False, False, False, False, False, False, True): 'R',

        (False, False, False, True, False, False, False, False, False): 'S',
        (False, False, True, False, False, False, False, False, False): 'T',
        (False, False, False, False, True, False, False, False, False): 'U',
        (False, True, False, False, False, False, False, False, False): 'V',

        (True, False, False, True, False, False, False, False, False): 'W',
        (True, False, True, False, False, False, False, False, False): 'X',
        (True, False, False, False, True, False, False, False, False): 'Y',
        (True, True, False, False, False, False, False, False, False): 'Z',

        (False, True, True, True, True, False, False, False, False): ' ',
    }

    return character_from_characteristics[
        (
            has_dot(image),
            has_top_point(image),
            has_right_point(image),
            has_bottom_point(image),
            has_left_point(image),
            has_top_right_corner(image),
            has_bottom_right_corner(image),
            has_bottom_left_corner(image),
            has_top_left_corner(image)
        )
    ]


path = input('Enter path: ')

whole_image = Image.open(path)
lines = get_sections(whole_image, separate_vertically=True)
character_images = []
for line in lines:
    character_images += get_sections(line, separate_vertically=False)
string_translation = ''
for character_index, character_image in enumerate(character_images):
    string_translation += get_from_image_character(character_image)
print(string_translation)
