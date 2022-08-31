def find_slot(values, start_index, end_index, value_to_find):
    """
    Given a sorted list of values (increasing in value) this function returns the index of
    the smallest value in the list that is greater than or equal to the value to be found.
    """
    if start_index == end_index:
        return start_index  # Slot was found

    midpoint = (start_index + end_index) // 2
    if value_to_find <= values[midpoint]:
        return find_slot(values, start_index, midpoint, value_to_find)
    return find_slot(values, midpoint + 1, end_index, value_to_find)
