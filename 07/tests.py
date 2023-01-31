from command import COMMANDS, Command

def command_parse_and_set_command():
    for k, v in COMMANDS.items():
        c = Command(k)
        try:
            c.parse_and_set_command(c.sanitized)
            assert c.type == v
        except  AssertionError:
            print(c.type, v)


if "__main__" == __name__:
    tests = [
        command_parse_and_set_command,
        
        ]
    for test in tests:
        test()
