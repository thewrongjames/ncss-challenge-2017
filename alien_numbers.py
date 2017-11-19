BASE = 5

CHARACTER_VALUES = {
    'a': 0,
    'e': 1,
    'i': 2,
    'o': 3,
    'u': 4
}


VALID_CHARACTERS = list(CHARACTER_VALUES.keys()) + [character.upper() for \
    character in CHARACTER_VALUES.keys()]


def alien2float(string):
    index_in_string = 0
    integer_components = []
    fractional_components = []
    moved_to_fractional_component = False

    for character in string:
        if character not in VALID_CHARACTERS:
            # The string is invalid, so, return None as instructed.
            return
        if character.isupper():
            if moved_to_fractional_component:
                # See above.
                return
            integer_components.append(CHARACTER_VALUES[character.lower()])
        if character.islower():
            moved_to_fractional_component = True
            fractional_components.append(CHARACTER_VALUES[character])

    values_to_sum = []

    for index, integer_component in enumerate(integer_components):
        values_to_sum.append(
            integer_component * (BASE**(len(integer_components) - index - 1))
        )

    for index, fractional_component in enumerate(fractional_components):
        values_to_sum.append(fractional_component * (BASE**(-index - 1)))

    # Adding in reverse because the hint said so (hence not using sum, as I
    # have no idea what order it does it in).
    value = 0.0
    for component in reversed(values_to_sum):
        value += component

    return value


if __name__ == '__main__':
    # Run the examples in the question.
    print(repr(alien2float('IUae')))
    print(repr(alien2float('OUAooea')))
    print(repr(alien2float('iuAE')))
    print(repr(alien2float('EIOU')))
    print(repr(alien2float('sdlkfjs;fl')))
