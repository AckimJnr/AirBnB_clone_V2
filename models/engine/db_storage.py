#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        from models.city import City
        from models.state import State
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.
                format(os.getenv('HBNB_MYSQL_USER'), os.getenv(
                    'HBNB_MYSQL_PWD'), os.getenv(
                        'HBNB_MYSQL_HOST'), os.getenv('HBNB_MYSQL_DB')),
                pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def new(self, obj):
        """
        add object to current db session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete obj from the current db session if its none
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in db and in current session
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """
        Retrieve all objects
        """
        from models import storage

        if cls:
            objects = self.__session.query(cls).all()
        else:
            from models import base_model
            classes = [City, State]
            objects = []
            for cls in classes:
                objects += self.__session.query(cls).all()

        obj_dict = {}
        for obj in objects:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            obj_dict[key] = obj

        return obj_dict

    def close(self):
        """
        close current connection
        """
        self.__session.remove()
