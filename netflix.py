from functions import *
from flask import Flask, jsonify, abort

app = Flask(__name__)


@app.route('/movie/<title>')
def name_movie(title):
    """Поиск по названию. Если таких фильмов несколько, выводить самый свежий."""
    if title:
        return jsonify(movie_title(title))
    abort(404)


@app.route('/movies/year/<int:year1>/<int:year2>')
def year_movie(year1: int, year2: int):
    """Поиск по диапазону лет выпуска с ограничением вывода 100 тайтлами"""
    if year1 and year2:
        return jsonify(data_years(year1, year2))
    abort(404)


@app.route('/movies/<genre>')
def movie_genre(genre):
    """Функция получает название жанра в качестве аргумента и возвращает
   10 самых свежих фильмов в формате json. В результате должно содержаться название и описание каждого фильма."""
    if genre:
        return jsonify(data_genre(genre))
    abort(404)


@app.route('/movies/<type>/<int:year>/<genre>')
def title_movie(type, year: int, genre):
    """Передается тип картины (фильм или сериал),
    год выпуска и ее жанр в БД с помощью SQL-запроса.
    На выходе список названий картин с их описаниями в JSON."""

    if type and year and genre:
        return jsonify(type_movie(type, year, genre))
    return abort(404)


@app.route('/rating/children')
def rating_children():
    """Поиск по рейтингу. Фильмы с рейтингом G"""
    return jsonify(child_rate())


@app.route('/rating/family')
def rating_family():
    """Поиск по рейтингу. Фильмы с рейтингом PG и PG-13"""
    return jsonify(family_rate())


@app.route('/rating/adult')
def rating_adult():
    """Поиск по рейтингу. Фильмы с рейтингом R, NC-17"""
    return jsonify(adult_rate())


@app.route('/actors/<name1>/<name2>')
def cast_name(name1, name2):
    """Функцию получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз.
    В качестве теста можно передать: Rose McIver и Ben Lamb, Jack Black и Dustin Hoffman."""

    if name1 and name2:
        return make_list_name(name1, name2)
    abort(404)


@app.errorhandler(404)
def not_found_handler(request):
    return jsonify({'error': '404 Not Found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
