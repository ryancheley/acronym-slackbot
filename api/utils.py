def string_split(input: str):
    data = input.split(":")
    if len(data) == 2:
        acronym = data[0]
        definition = data[1].strip()
        return (acronym, definition)
    else:
        return (None, None)


def acronym_checker(acronym: str):
    if len(acronym) > 8:
        raise AttributeError
    else:
        pass
