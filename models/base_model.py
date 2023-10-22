#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow(),
            onupdate=datetime.utcnow()
            )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if '__class__' in kwargs:
                del kwargs['__class__']

            if isinstance(kwargs.get('updated_at'), str):
                kwargs['updated_at'] = datetime.strptime(
                        kwargs['updated_at'],
                        '%Y-%m-%dT%H:%M:%S.%f'
                        )
            if isinstance(kwargs.get('created_at'), str):
                kwargs['created_at'] = datetime.strptime(
                        kwargs['created_at'],
                        '%Y-%m-%dT%H:%M:%S.%f'
                        )
            for key, value in kwargs.items():
                if not hasattr(self, key):
                    setattr(self, key, value)
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                if value:
                    dictionary[key] = value.isoformat()
            else:
                dictionary[key] = value

        dictionary['__class__'] = type(self).__name__
        dictionary.pop('_sa_instance_state', None)

        return dictionary

    def delete(self):
        from models import storage
        """Delete current Instance from storage"""
        if hasattr(models, 'storage') and callable(
                getattr(models.storage, 'delete', None)):
            models.storage.delete(self)
