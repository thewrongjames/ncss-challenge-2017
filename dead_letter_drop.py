number = input('Phone number: ')
if (
        number[0] == '0'
        and sum([int(number[index]) for index in range(-3, 0)]) == 9
):
    number = number[-3:] + number[3:-3] + number[:3]
print(number)
