import sqlite3


def run_sql(sql):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        results = cur.execute(sql).fetchall()
    return results


def make_list_name(results):
    list_name = []
    list_final_name = []
    for names in results:
        for name in names:
            if name != 'name1' and name != 'name2':
                list_name.append(name)

    if list_name.count('name') > 2:
        list_final_name.append('name')
    return True
