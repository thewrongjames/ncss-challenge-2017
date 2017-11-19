from math import sqrt as square_root
from string import punctuation


word_length_frequencies = {}


def increment_value_at_index(index, list_):
    try:
        list_[index] += 1
    except IndexError:
        list_ += [0 for _ in range(len(list_), index)] + [1]


def word_frequencies(file_name):
    word_frequencies = []

    with open(file_name) as file_:
        for line in file_:
            for word in line.strip().split():
                if word.strip(punctuation):
                    increment_value_at_index(
                        len(word.strip(punctuation)) - 1,
                        word_frequencies
                    )

    return word_frequencies


with open('texts.txt') as texts_file:
    for line in texts_file:
        file_name = line.strip()
        word_length_frequencies[file_name] = word_frequencies(file_name)


unknown_word_length_frequences = word_frequencies('unknown.txt')


def get(iterable, index, default):
    try:
        return iterable[index]
    except IndexError:
        return default


def cosine_similarity(a, b):
    length = len(a) if len(a) > len(b) else len(b)
    numerator = sum(
        [get(a, index, 0) * get(b, index, 0) for index in range(length)]
    )
    denominator = square_root(
        sum([value**2 for value in a]) * sum([value**2 for value in b])
    )
    return numerator / denominator


text_cosine_similarities = {}
for file_name in word_length_frequencies.keys():
    text_cosine_similarities[file_name] = cosine_similarity(
        word_length_frequencies[file_name],
        unknown_word_length_frequences
    )


for file_name, similarity in sorted(
        text_cosine_similarities.items(),
        key=lambda item: item[1],
        reverse=True
):
    print(similarity, file_name)
