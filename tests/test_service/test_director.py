# импортируем MagicMock
from unittest.mock import MagicMock

# импортируем pytest
import pytest

# DAO для работы с БД
from dao.director import DirectorDAO
# модель, она же наша сущность
from dao.model.director import Director
# Service который мы тестируем
from service.director import DirectorService


# готовим фикстуру где мы подменяем всю логику при работе с БД
@pytest.fixture()
def director_dao():
    # мы не передаем объект сессии БД, мы симулируем работу с БД передав None
    director_dao = DirectorDAO(None)
    # готовим три вымышленных пользователя
    test_1 = Director(id=1, name='Glendyn Ivin')
    test_2 = Director(id=2, name='James Ivory')
    test_3 = Director(id=3, name='Woody Allen')

    # при вызове дао мы подменяем метод на MagicMock (вкладывая заранее подготовленные данные в наши функции)
    director_dao.get_one = MagicMock(return_value=test_1)
    director_dao.get_all = MagicMock(return_value=[test_1, test_2, test_3])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock(return_value=Director(id=3))
    return director_dao


# класс для тестирования бизнеслогики
class TestDirectorService:
    # фикстура будет подгружаться при вызове этого метода.
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        # при вызове service будет подгружаться dao из фикстуры @pytest.fixture() def dao():
        self.director_service = DirectorService(dao=director_dao)

    # функция тестирующая ф-ию get_one:
    def test_get_one(self):
        # вызывает сервис, у него вызывает get_one и передает ему (id)
        director = self.director_service.get_one(1)

        # проверяет что режиссер, который к нам вернулся должен быть не None
        assert director != None
        # проверяет что режиссер id который к нам вернулся тоже должен быть не None
        assert director.id != None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {
            "name": "Woody Allen",
        }
        director = self.director_service.create(director_d)
        assert director.id != None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Woody Allen",
        }
        self.director_service.update(director_d)
