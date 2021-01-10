from typing import List


def prepare_sql(sql):
    sql = sql.replace(',', ', ')
    sql = sql.replace('=', ' = ')
    sql = sql.replace('\'', '')

    sql = ' '.join(sql.split())
    keywords = ['SET', 'WHERE']
    for kw in keywords:
        sql = sql.replace(f' {kw} ', f'\n{kw} ')
    return sql


def find_table(line: str) -> str:
    return line.replace('UPDATE ', '')


def find_set_variables(line: str) -> dict:
    sql = line.replace('SET ', '')
    variables = sql.split(', ')
    data = {}
    for var in variables:
        key, value = var.split(' = ')
        data[key] = value
    return data


def create_select_query(table: str, id_field_name: str, set_variables: dict, where: str) -> str:
    return f"""
SELECT {id_field_name}, {', '.join(list(set_variables.keys()))}
FROM {table}
{where}
"""


def get_results_from_select(sql_select: str) -> List[dict]:
    return [
        {
            'id': 1, 'firstname': 'Hugo', 'lastname': 'Sandoval'
        }
    ]


def create_audit_trail(table: str, set_variables: dict, id_field_name: str, results: List[dict]) -> str:
    sql_insert = ''
    sql_insert_head = "INSERT INTO KONFIO.SYS_AUDIT_TRAIL(table, field, id, field_update, old_value, new_value) VALUES"
    for key, value in set_variables.items():
        sql = ''
        for result in results:
            sql += f"('{table}', '{id_field_name}', '{result[id_field_name]}', '{key}', '{result[key]}', '{value}'),"
        sql_insert += f'{sql_insert_head}\n{sql[:-1]};\n'
    return sql_insert


def main():
    id_field_name = 'id'
    sql = "UPDATE SCHEMA.USERS SET firstname = 'John',lastname='Deere' WHERE id = 1;"

    sql = prepare_sql(sql)
    lines = sql.split('\n')
    n = len(lines)
    if n != 3:
        print(f'Invalid!', n)
        return

    table = find_table(lines[0])
    set_variables = find_set_variables(lines[1])
    where = lines[2]

    sql_select = create_select_query(table, id_field_name, set_variables, where)
    results = get_results_from_select(sql_select)
    sql_insert = create_audit_trail(table, set_variables, id_field_name, results)

    print('sql:\n', sql)
    print('table:', table)
    print('set_variables:', set_variables)
    print('where:', where)
    print('id_field_name:', id_field_name)
    print('sql_select:', sql_select)
    print('sql_insert:\n', sql_insert)


if __name__ == '__main__':
    main()
