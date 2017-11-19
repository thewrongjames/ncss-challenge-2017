def author_rankings(thread_list):
    author_upvotes = {}
    for thread in thread_list:
        for post in thread['posts']:
            if post['author'] in author_upvotes:
                author_upvotes[post['author']] += post['upvotes']
            else:
                author_upvotes[post['author']] = post['upvotes']

    ranking_minimums = {
          0: 'Insignificantly Evil',
          1: 'Cautiously Evil',
         20: 'Justifiably Evil',
        100: 'Wickedly Evil',
        500: 'Diabolically Evil'
    }

    rankings = []
    for author, upvotes in author_upvotes.items():
        current_ranking_id = 0
        for ranking_id in ranking_minimums.keys():
            if upvotes >= ranking_id and  ranking_id > current_ranking_id:
                current_ranking_id = ranking_id

        rankings.append((author, upvotes, ranking_minimums[current_ranking_id]))

    rankings.sort(key=lambda ranking: ranking[0],)
    # Previously tied items should remain the same in the next sort.
    rankings.sort(key=lambda ranking: ranking[1], reverse=True)

    return rankings


if __name__ == '__main__':
    # Example calls to your function.
    print(author_rankings([
        {
            'title': 'Invade Manhatten, anyone?',
            'tags': ['world-domination', 'hangout'],
            'posts': [
                {
                    'author': 'Mr. Sinister',
                    'content': "I'm thinking 9 pm?",
                    'upvotes': 2,
                },
                {
                    'author': 'Mystique',
                    'content': "Sounds fun!",
                    'upvotes': 0,
                },
                {
                    'author': 'Magneto',
                    'content': "I'm in!",
                    'upvotes': 0,
                },
            ],
        }
    ]))
