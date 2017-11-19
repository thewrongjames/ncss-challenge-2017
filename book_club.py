who_has_read_book = {}
friends = set()


line = input('Book read: ')
while line:
    book, friend = line.split(':')

    friends.add(friend)

    if book in who_has_read_book:
        who_has_read_book[book].add(friend)
    else:
        who_has_read_book[book] = {friend}

    line = input('Book read: ')


who_hasnt_read_book = {}
for book, friends_who_have_read_book in who_has_read_book.items():
    who_hasnt_read_book[book] = friends - friends_who_have_read_book


for book in sorted(who_hasnt_read_book.keys()):
    # If who_hasnt_read_book[book] was empty, the join will also be empty.
    who_hasnt_read_this_book_string = ', '.join(sorted(list(\
        who_hasnt_read_book[book]))) or 'Everyone has read this!'

    print(book + ': ' + who_hasnt_read_this_book_string)
