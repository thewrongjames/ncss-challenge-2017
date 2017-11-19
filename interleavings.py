def get_remaining_interleavings(so_far, option_one, option_two):
    if not option_one:
        return [so_far + option_two]
    if not option_two:
        return [so_far + option_one]

    remaining_from_option_one = get_remaining_interleavings(
        so_far + option_one[0],
        option_one[1:],
        option_two
    )
    remaining_from_option_two = get_remaining_interleavings(
        so_far + option_two[0],
        option_one,
        option_two[1:]
    )

    return sorted(remaining_from_option_one + remaining_from_option_two)


def interleavings(a, b):
    return get_remaining_interleavings('', a, b)


if __name__ == '__main__':
    # Run the examples in the question.
    result = interleavings('ab', 'cd')
    print(result)
    result = interleavings('a', 'cd')
    print(result)
