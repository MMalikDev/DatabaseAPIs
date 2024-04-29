from collections import namedtuple

from .albums import Albums
from .artists import Artists
from .books import Book, Books
from .images import Image, Images
from .people import People, Person
from .songs import Songs
from .users import User, Users

SQL_Model = namedtuple("SQL_Model", ["db", "data"])
noSQL_Model = namedtuple("noSQL_Model", ["data"])

models_nosql = [
    noSQL_Model(Songs),
    noSQL_Model(Albums),
    noSQL_Model(Artists),
    noSQL_Model(User),
    noSQL_Model(Book),
    noSQL_Model(Image),
    noSQL_Model(Person),
]

models_sql = [
    SQL_Model(Users, User),
    SQL_Model(Books, Book),
    SQL_Model(Images, Image),
    SQL_Model(People, Person),
]
