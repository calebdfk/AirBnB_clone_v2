#!/usr/bin/python3
""" holds class State"""
from models.base_model import BaseModel, Base
from models.city import City
import models
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """Representation of state"""
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """Getter for list of city instances related to the state"""
            return [city for city in models.storage.all(City).values() if city.state_id == self.id]
