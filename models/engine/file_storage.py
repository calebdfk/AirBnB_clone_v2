#!/usr/bin/python3
"""
Contains the FileStorage class
"""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects."""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                obj_data = jo[key]
                if '__class__' in obj_data:
                    cls_name = obj_data['__class__']
                    if cls_name in classes:
                        obj = classes[cls_name](**obj_data)
                        if cls_name == 'State':
                            # Handle reloading cities relationship for State
                            if 'cities' in obj_data:
                                city_ids = obj_data['cities']
                                cities = []
                                for city_id in city_ids:
                                    city_key = "City." + city_id
                                    if city_key in self.__objects:
                                        cities.append(self.__objects[city_key])
                                obj.cities = cities
                        self.__objects[key] = obj
        except Exception as e:
            print("Exception:", e)

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside."""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects."""
        self.reload()
