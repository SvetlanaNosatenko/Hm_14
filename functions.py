import sqlite3
from flask import jsonify


def run_sql(sql):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        results = cur.execute(sql).fetchall()
        cur.close()
    return results


def movie_title(title):
    sql = f"SELECT title, country, release_year, listed_in, description FROM netflix" \
          f"WHERE lower(title) like '%{title.lower()}%' " \
          f"ORDER BY release_year DESC limit 1"
    results = run_sql(sql)
    return [{"title": title, "country": country, "release_year": release_year,
                     "listed_in": listed_in, "description": description}
                      for title, country, release_year, listed_in, description in results]


def data_years(year1, year2):
    sql = f"SELECT title, release_year FROM netflix " \
          f"WHERE type = 'Movie' AND release_year BETWEEN {year1} AND {year2} limit 100 "
    results = run_sql(sql)
    return [{"title": title, "release_year": release_year} for title, release_year in results]


def data_genre(genre):
    sql = f"SELECT title, description FROM netflix " \
          f"WHERE type = 'Movie' AND lower(listed_in) like '%{genre.lower()}%' " \
          f"ORDER BY release_year DESC limit 10"
    results = run_sql(sql)
    return [{"title": title, "description": description} for title, description in results]


def type_movie(type, year, genre):
    sql = f"SELECT title, description FROM netflix " \
          f"WHERE lower(type) like '%{type.lower()}%' AND release_year like '%{year}%' " \
          f"and lower(listed_in) like '%{genre.lower()}%'"
    results = run_sql(sql)
    return [{"title": title, "description": description} for title, description in results]


def child_rate():
    sql = f"SELECT title, rating, description FROM netflix " \
          f"WHERE rating LIKE 'G%'"
    results = run_sql(sql)
    return [{"title": title, "rating": rating, "description": description}
                    for title, rating, description in results]


def family_rate():
    sql = f"SELECT title, rating, description FROM netflix " \
          f"WHERE rating LIKE 'P%'"
    results = run_sql(sql)
    return [{"title": title, "rating": rating, "description": description}
                    for title, rating, description in results]


def adult_rate():
    sql = f"SELECT title, rating, description FROM netflix " \
          f"WHERE rating in ('NC-17','R')"
    results = run_sql(sql)
    return [{"title": title, "rating": rating, "description": description}
                    for title, rating, description in results]


def make_list_name(name1, name2):
    sql = f"SELECT cast FROM netflix " \
          f"WHERE lower(cast like) '%{name1.lower()}% AND lower(cast) like '%{name2.lower()}%'"
    results = run_sql(sql)  #получение списка кортежей имен из cast, где есть name1 и name2
    list_name = []
    list_final_name = []
    for names in results:
        for name in names:
            if name != 'name1' and name != 'name2':
                list_name.append(name)  # получение списка имен актеров, которые играли с name1 и name2

    if list_name.count('name') > 2: # составление списка имен, кто играет в паре с name1 и name2 больше 2 раз
        list_final_name.append('name')
    return list_final_name
