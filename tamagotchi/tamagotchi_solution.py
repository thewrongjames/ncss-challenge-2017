from functools import wraps
from tamagotchi import Tamagotchi


COMMAND_PROMPT = 'Command: '
INVALID_COMMAND_NOTICE = 'Invalid command.'
NONE_WITH_NAME_NOTICE = 'No Tamagotchi with that name.'
ALREADY_EXISTS_NOTICE = 'You already have a Tamagotchi called that.'


def create_handler(tamagotchis, name):
    # The and will only run the second statement if the first is True.
    if name in tamagotchis and not tamagotchis[name].is_dead():
        print(ALREADY_EXISTS_NOTICE)
        return

    tamagotchis[name] = Tamagotchi(name)
    wait_handler(tamagotchis)


def tamagotchi_name_validated(function):
    # Wraps is probably overkill, but, could be useful.
    # Then again, this whole function is definately overkill.
    @wraps(function)
    def wrapper(tamagotchis, name):
        if not name in tamagotchis:
            print(NONE_WITH_NAME_NOTICE)
            return
        return function(tamagotchis, name)
    return wrapper


@tamagotchi_name_validated
def feed_handler(tamagotchis, name):
    tamagotchis[name].feed()
    wait_handler(tamagotchis)


@tamagotchi_name_validated
def play_handler(tamagotchis, name):
    tamagotchis[name].play()
    wait_handler(tamagotchis)


def wait_handler(tamagotchis, _=None):
    # Wait does not take a name.
    # This will also hence display it for all other successful commands:
    sorted_tamagotchis = [item[1] for item in sorted(list(tamagotchis.items()))]
    for tamagotchi in sorted_tamagotchis:
        print(tamagotchi)

    for tamagotchi in tamagotchis.values():
        tamagotchi.increment_time()

def invalid_first_token_handler(*args):
    # If the first token was invalid, it doesn't matter what the second token
    # is.
    print(INVALID_COMMAND_NOTICE)


first_token_handlers = {
    'create': create_handler,
    'feed': feed_handler,
    'play': play_handler,
    'wait': wait_handler
}


tamagotchis = {}
command = input(COMMAND_PROMPT)
while command:
    tokens = command.split()
    second_token = tokens[1] if len(tokens) > 1 else None
    first_token_handlers.get(tokens[0], invalid_first_token_handler)(
        tamagotchis,
        second_token
    )
    # Anything after the second word will be ignored. The second word will also
    # be ignored if the first word is wait, or is not in first_token_handlers.

    command = input(COMMAND_PROMPT)
