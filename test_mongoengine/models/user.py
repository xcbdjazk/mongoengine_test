# -*- coding:utf-8 -*-

from mongoengine import *

connect('test_mongo1', host='mongo', port=27017)  # todo : mongo is system Hosts file
size = (("zzzz", 1), ("2", 2))


class User(Document):
    meta = {"collection": "user"}
    int_id = SequenceField()
    username = StringField(choices=size)
    pwd = StringField()

    def __str__(self):
        return "<class {0} {1}>".format(self.__class__.__name__, self.username)


class SubUser(DynamicDocument):
    meta = {"collection": "sub_user"}
    name = StringField()
    sub_user = ReferenceField(User)


class Role(DynamicDocument):
    meta = {"collection": "role"}
    role_id = IntField()


class Post(DynamicDocument):
    meta = {"allow_inheritance": True, "collection": "list"}
    post = ListField(StringField())


class Posts(Post):
    ids = IntField()
    pppp = StringField()


class Comment(EmbeddedDocument):
    # meta = {"collection": "list"}
    com = ListField(StringField())


class Page(DynamicDocument):
    meta = {"collection": "page"}
    pages = ListField(EmbeddedDocumentField(Comment))


if __name__ == "__main__":

    # for i in range(20):
    #     p = Posts()
    #     p.ids = i
    #     p.save()
    #     print ('save ok!!!')
    user = User()
    user.username = 'zzzz'
    user.save()