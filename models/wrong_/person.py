# coding=utf-8
from mongoengine import connect, DynamicDocument, Document
from mongoengine import ListField, StringField, IntField, ReferenceField, ObjectIdField
try:
    from models.wrong_.user import User
except ImportError:
    # 触发循环导入包的错误
    print('ImportError')
connect('wrong_', host='mongo', port=27017) # wrong_  不存在就会自动创建


class Person(Document):

    person = StringField()

    def user(self):
        # 解决方法
        from models.wrong_.user import User
        return