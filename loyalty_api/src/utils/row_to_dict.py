from databases.interfaces import Record


def row_to_dict(row: Record) -> dict:
    """
    Функция конвертирующая sqlalchemy.Table объект в dict

    :param row: объект sqlalchemy.Table
    :return: словарь
    """

    res = {}
    for column in row._column_map.keys():
        res[column] = str(getattr(row, column))
    return res
