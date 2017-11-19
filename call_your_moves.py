shorthand_to_long = {
    'g': 'Guard!',
    'p': 'Parry!',
    'd': 'Dodge!',
    's': 'Spin!',
    't': 'THRUST!'
}

UNKNOWN_SHORTHAND = 'SPROING!'

script_list = list(input('Script: '))

for script_item in script_list:
    print(shorthand_to_long.get(script_item, UNKNOWN_SHORTHAND))
