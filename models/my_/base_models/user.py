# coding=utf-8
from mongoengine import connect, DynamicDocument, Document
from mongoengine import ListField, StringField, IntField, ReferenceField
from models.my_.base_models.base.base_person import Person
from models.my_.base_models.base.base_user import User as U
connect('wrong_', host='mongo', port=27017) # wrong_  不存在就会自动创建


class User(U):

    person = ReferenceField(Person)

