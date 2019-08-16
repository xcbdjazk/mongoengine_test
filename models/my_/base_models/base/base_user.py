# coding=utf-8
from mongoengine import connect, DynamicDocument, Document
from mongoengine import ListField, StringField, IntField, ReferenceField, ObjectIdField

connect('wrong_', host='mongo', port=27017) # wrong_  不存在就会自动创建


class User(Document):
    meta = {'allow_inheritance': True, 'collection': 'user'}