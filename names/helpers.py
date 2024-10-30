def most_common_prefix(list1: list[str], list2: list[str], delimiter: str) -> str:
    """
    Find most common part of beginning elements of two lists and return it as a string joined by given delimiter.

    Args:
        list1: First list of strings to compare.
        list2: Second list of strings to compare.
        delimiter: Character to join common part of elements as a string.

    Returns:
        Common elements in lists as a string joined with delimiter.
    """
    i, common_prefix_parts = 0, []
    while i < len(list1) and i < len(list2) and list1[i] == list2[i]:
        common_prefix_parts.append(list1[i])
        i += 1
    return delimiter.join(common_prefix_parts)
