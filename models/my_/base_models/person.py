# coding=utf-8
from mongoengine import connect, DynamicDocument, Document
from mongoengine import ListField, StringField, IntField, ReferenceField, ObjectIdField
from models.my_.base_models.base.base_user import User
from models.my_.base_models.base.base_person import Person as P
connect('wrong_', host='mongo', port=27017) # wrong_  不存在就会自动创建


class Person(P):

    person = StringField()

    def user(self):
        # 解决方法

        return