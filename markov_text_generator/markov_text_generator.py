import random


def get_file_bigrams(filename):
    words = []
    with open(filename) as file_:
        for line in file_:
            words += [word.lower() for word in line.split()]

    bigrams = {}
    for index, word in enumerate(words):
        try:
            bigrams[word].append(words[index+1])
        except IndexError:
            # If it got to the index error, then, word was in there. And as
            # there is no word following it (words[index + 1] doesn't exist),
            # there is nothing else to do here.
            pass
        except KeyError:
            # word is not yet in the dictionary
            try:
                bigrams[word] = [words[index+1]]
            except IndexError:
                # See above.
                bigrams[word] = []

    return bigrams


def generate_sentence(start_token, filenames, word_count_limit=200):
    # This assumes that start token will always be in the files.

    bigrams = {}

    for filename in filenames:
        for first_token, second_tokens in get_file_bigrams(filename).items():
            if first_token in bigrams:
                bigrams[first_token] += second_tokens
            else:
                bigrams[first_token] = second_tokens

    sentence = [start_token.lower()]

    while (
            sentence[-1] != '.'
            and len(bigrams[sentence[-1]]) > 0
            and len(sentence) < word_count_limit
    ):
        sentence.append(random.choice(bigrams[sentence[-1]]))

    return ' '.join(sentence)


if __name__ == '__main__':
    # The random number generator is initialised to zero here purely
    # for your own testing so that each time you run your code during
    # development, you will get the same output. Remove this to get
    # different output each time you run your code with the same input.
    random.seed(0)

    # Run the examples in the question.
    for i in range(4):
        print(generate_sentence('There', ['single.txt']))
    print('=' * 80)
    for i in range(4):
        print(generate_sentence('the', ['jab.txt']))
    print('=' * 80)
    for i in range(4):
        print(generate_sentence('It', ['dracula.txt', 'pandp.txt']))
    print('=' * 80)
    for i in range(10):
        print(
            generate_sentence(
                'Once', ['dracula.txt', 'jb.txt', 'pandp.txt', 'totc.txt']
            )
        )
