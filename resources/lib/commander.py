import sys

def handle_command():
    command = get_command()
    if 'mode' not in command or not command['mode']:
        return # notify, log, something
    if command['mode'] == 'something':
        pass # No commands yet

def get_command():
    """Build a dictionary of all arguments. The arguements are split key, value on '=' with the keys lowercased to ease comparison. Arguments without '=' are just set to True with a lowercased key, but you can just check if it exists ('if <key> in command')."""
    command = {}
    for x in range(1, len(sys.argv)):
        arg = sys.argv[x].split("=", 1)
        command[arg[0].strip().lower()] = arg[1].strip() if len(arg) > 1 else True

    return command
