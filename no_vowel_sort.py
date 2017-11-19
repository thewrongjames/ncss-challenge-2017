def novowelsort(the_list):
    ignored_characters = ['a', 'e', 'i', 'o', 'u']
    ignored_characters += [
        character.upper() for character in ignored_characters
    ]

    the_list.sort(key=lambda string: ''.join([character for character in \
        string if character not in ignored_characters]))

    return the_list


if __name__ == '__main__':
    # Example calls to your function.
    print(novowelsort(['alpha', 'beta']))
    print(
        novowelsort(
            ['once', 'upon', 'abc', 'time', 'there', 'were', 'some', 'words']
        )
    )
    print(novowelsort(['ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON']))
