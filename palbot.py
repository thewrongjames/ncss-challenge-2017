for number in range(int(input('Enter begin: ')), int(input('Enter end: ')) + 1):
    print(str(number) + ''.join(list(reversed(str(number)))))
