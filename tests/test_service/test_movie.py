# импортируем MagicMock
from unittest.mock import MagicMock

# импортируем pytest
import pytest

from dao.model.director import Director
from dao.model.genre import Genre
from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


# готовим фикстуру где мы подменяем всю логику при работе с БД
@pytest.fixture()
def movie_dao():
    director = Director(id=1, name='Glendyn Ivin')
    genre = Genre(id=1, name='comedy')

    # мы не передаем объект сессии БД, мы симулируем работу с БД передав None
    movie_dao = MovieDAO(None)
    # готовим три вымышленных пользователя
    test_1 = Movie(id=1, title="title1", description="description1", trailer="trailer1", year=1990, rating=3,
                   director=director, genre=genre)
    test_2 = Movie(id=2, title="title2", description="description2", trailer="trailer2", year=2000, rating=6,
                   director=director, genre=genre)
    test_3 = Movie(id=3, title="title3", description="description3", trailer="trailer3", year=2020, rating=9,
                   director=director, genre=genre)

    # при вызове дао мы подменяем метод на MagicMock (вкладывая заранее подготовленные данные в наши функции)
    movie_dao.get_one = MagicMock(return_value=test_1)
    movie_dao.get_all = MagicMock(return_value=[test_1, test_2, test_3])
    movie_dao.create = MagicMock(return_value=Movie(id=2))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock(return_value=Movie(id=2))
    return movie_dao


# класс для тестирования бизнеслогики
class TestMovieService:
    # фикстура будет подгружаться при вызове этого метода.
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        # при вызове service будет подгружаться dao из фикстуры @pytest.fixture() def dao():
        self.movie_service = MovieService(dao=movie_dao)

    # функция тестирующая ф-ию get_one:
    def test_get_one(self):
        # вызывает сервис, у него вызывает get_one и передает ему (id)
        movie = self.movie_service.get_one(1)

        # проверяет что фильм, который к нам вернулся должен быть не None
        assert movie != None
        # проверяет что фильм id который к нам вернулся тоже должен быть не None
        assert movie.id != None

    def test_get_all(self):
        movie = self.movie_service.get_all()
        assert len(movie) > 0

    def test_create(self):
        movie_d = {
            "title": "title2",
            "description": "description2",
            "trailer": "trailer2",
            "year": 2000,
            "rating": 6,
            "director_id": 1,
            "genre_id": 1
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id != None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "id": 2,
            "title": "title2",
            "description": "description2",
            "trailer": "trailer2",
            "year": 2000,
            "rating": 6,
            "director_id": 1,
            "genre_id": 1
        }
        self.movie_service.update(movie_d)
