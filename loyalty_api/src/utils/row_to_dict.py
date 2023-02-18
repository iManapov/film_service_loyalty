from databases.interfaces import Record


def row_to_dict(row: Record) -> dict:
    """
    Converts Record object into dict

    :param row: Record object
    :return: object as dict
    """

    res = {}
    for column in row._column_map.keys():
        res[column] = str(getattr(row, column))
    return res
