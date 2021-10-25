from functions import *
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/movie/<title>')
def name_movie(title):
    if title:
        sql = f"SELECT title, country, release_year, listed_in, description FROM netflix" \
              f"WHERE lower(title) like '%{title.lower()}%' " \
              f"ORDER BY release_year DESC limit 1"
        results = run_sql(sql)
        return jsonify([{"title": title, "country": country, "release_year": release_year,
                         "listed_in": listed_in, "description": description}
                        for title, country, release_year, listed_in, description in results]), 200
    return "Некорректный запрос", 404


@app.route('/movies/year/<int:year1>/<int:year2>')
def year_movie(year1: int, year2: int):
    """Поиск по диапазону лет выпуска с ограничением вывода 100 тайтлами"""
    if year1 and year2:
        sql = f"SELECT title, release_year FROM netflix " \
              f"WHERE type = 'Movie' AND release_year BETWEEN {year1} AND {year2} limit 100 "
        results = run_sql(sql)
        return jsonify([{"title": title, "release_year": release_year} for title, release_year in results]), 200
    return "Некорректный запрос", 404


@app.route('/movies/<genre>')
def movie_genre(genre):
    """Функция получает название жанра в качестве аргумента и возвращает
   10 самых свежих фильмов в формате json. В результате должно содержаться название и описание каждого фильма."""
    if genre:
        sql = f"SELECT title, description FROM netflix " \
              f"WHERE type = 'Movie' AND lower(listed_in) like '%{genre.lower()}%' " \
              f"ORDER BY release_year DESC limit 10"
        results = run_sql(sql)
        return jsonify([{"title": title, "description": description} for title, description in results])

    return "Некорректный запрос", 404


@app.route('/movies/<type>/<int:year>/<genre>')
def title_movie(type, year: int, genre):
    """Передается тип картины (фильм или сериал),
    год выпуска и ее жанр в БД с помощью SQL-запроса.
    На выходе список названий картин с их описаниями в JSON."""

    if type and year and genre:

        sql = f"SELECT title, description FROM netflix " \
              f"WHERE lower(type) like '%{type.lower()}%' AND release_year like '%{year}%' " \
              f"and lower(listed_in) like '%{genre.lower()}%'"
        results = run_sql(sql)
        return jsonify([{"title": title, "description": description} for title, description in results])

    return "Некорректный запрос", 404


@app.route('/rating/children')
def rating_children():
    """Поиск по рейтингу. Фильмы с рейтингом G"""

    sql = f"SELECT title, rating, description FROM netflix " \
          f"WHERE rating LIKE 'G%'"
    results = run_sql(sql)
    return jsonify([{"title": title, "rating": rating, "description": description}
                    for title, rating, description in results])


@app.route('/rating/family')
def rating_family():
    """Поиск по рейтингу. Фильмы с рейтингом PG и PG-13"""

    sql = f"SELECT title, rating, description FROM netflix " \
          f"WHERE rating LIKE 'P%'"
    results = run_sql(sql)
    return jsonify([{"title": title, "rating": rating, "description": description}
                    for title, rating, description in results])


@app.route('/rating/adult')
def rating_adult():
    """Поиск по рейтингу. Фильмы с рейтингом R, NC-17"""

    sql = f"SELECT title, rating, description FROM netflix " \
          f"WHERE rating in ('NC-17','R')"
    results = run_sql(sql)
    return jsonify([{"title": title, "rating": rating, "description": description}
                    for title, rating, description in results])


@app.route('/actors/<name1>/<name2>')
def cast_name(name1, name2):
    if name1 and name2:
        sql = f"SELECT cast FROM netflix " \
              f"WHERE lower(cast like) '%{name1.lower()}% AND lower(cast) like '%{name2.lower()}%'"
        results = run_sql(sql)
        return make_list_name(results), 200
    return "Некорректный запрос", 404


if __name__ == '__main__':
    app.run(debug=True)
