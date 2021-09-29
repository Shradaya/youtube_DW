def query(filepath):
    with open(filepath, 'r') as file:
        sql_query = "".join(file.readlines())
    return sql_query