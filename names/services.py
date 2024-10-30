from names.helpers import most_common_prefix

def group_names(names: list[str], delimiter: str = "_") -> dict[str, list[str]]:
    """
    Group given list of names by longest possible common prefixes.

    Args:
        names: list of strings.
        delimiter: Character to distinguish prefix in list of names.

    Returns:
        JSON-like object with lists of names grouped by common prefixes.
    """
    if not names:
        return {}

    if len(names) == 1:
        return {names[0]: names}

    # convertion made to prevent duplicated from sorted list
    names = list(set(names))
    names.sort()

    result = {}

    # find most common prefix with neighbours - looking for previous and next common prefix,
    # to clarify most descriptive prefix for given element
    for idx, name in enumerate(names):
        common_prefix_prev = ""
        common_prefix_next = ""
        if idx + 1 < len(names):
            next_name = names[idx + 1]
            splitted_name = name.split(delimiter)
            splitted_next_name = next_name.split(delimiter)
            common_prefix_next = most_common_prefix(splitted_name, splitted_next_name, delimiter)
        if idx > 0:
            splitted_name = name.split(delimiter)
            splitted_prev_name = names[idx - 1].split(delimiter)
            common_prefix_prev = most_common_prefix(splitted_name, splitted_prev_name, delimiter)

        common_prefix = common_prefix_prev if len(common_prefix_prev) > len(common_prefix_next) else common_prefix_next

        # if no neighbouring common prefix, create new one containing only one element
        if not common_prefix:
            common_prefix = name

        if not common_prefix in result:
            result[common_prefix] = [name]
        else:
            result[common_prefix].append(name)

    return result
