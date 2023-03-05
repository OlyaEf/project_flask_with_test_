# импортируем MagicMock
from unittest.mock import MagicMock
# импортируем pytest
import pytest

# модель, она же наша сущность
from dao.model.genre import Genre
# DAO для работы с БД
from dao.genre import GenreDAO
# Service который мы тестируем
from service.genre import GenreService
from setup_db import db


# готовим фикстуру где мы подменяем всю логику при работе с БД
@pytest.fixture()
def genre_dao():
    # мы не передаем объект сессии БД, мы симулируем работу с БД передав None
    genre_dao = GenreDAO(None)
    # готовим три вымышленных пользователя
    test_1 = Genre(id=1, name='comedy')
    test_2 = Genre(id=2, name='fantasy')
    test_3 = Genre(id=3, name='thriller')

    # при вызове дао мы подменяем метод на MagicMock (вкладывая заранее подготовленные данные в наши функции)
    genre_dao.get_one = MagicMock(return_value=test_1)
    genre_dao.get_all = MagicMock(return_value=[test_1, test_2, test_3])
    genre_dao.create = MagicMock(return_value=Genre(id=2))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()
    return genre_dao


# класс для тестирования бизнеслогики
class TestGenreService:
    # фикстура будет подгружаться при вызове этого метода.
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        # при вызове service будет подгружаться dao из фикстуры @pytest.fixture() def dao():
        self.genre_service = GenreService(dao=genre_dao)

    # функция тестирующая ф-ию get_one:
    def test_get_one(self):
        # вызывает сервис, у него вызывает get_one и передает ему (id)
        genre = self.genre_service.get_one(1)

        # проверяет что режиссер, который к нам вернулся должен быть не None
        assert genre != None
        # проверяет что режиссер id который к нам вернулся тоже должен быть не None
        assert genre.id != None

    def test_get_all(self):
        genre = self.genre_service.get_all()
        assert len(genre) > 0

    def test_create(self):
        genre_d = {
            "name": "comedy",
        }
        genre = self.genre_service.create(genre_d)
        assert genre.id != None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        genre_d = {
            "id": 3,
            "name": "XLL"
        }
        self.genre_service.update(genre_d)
