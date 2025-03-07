from pymongo.cursor import Cursor


def paginate_query(query: Cursor, limit: int, offset: int) -> Cursor:
    return query.skip(offset).limit(limit)
