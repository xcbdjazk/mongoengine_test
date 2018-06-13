# -*- coding:utf-8 -*-

from mongoengine import *

connect('test', host='mongo', port=27017)  # todo : mongo is system Hosts file
size = (("zzzz", 1), ("2", 2))


class User(Document):
    meta = {"collection": "user"}
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
    pppp = StringField()


class Comment(EmbeddedDocument):
    # meta = {"collection": "list"}
    com = ListField(StringField())


class Page(DynamicDocument):
    meta = {"collection": "page"}
    pages = ListField(EmbeddedDocumentField(Comment))


if __name__ == "__main__":
    # r = Role()
    # r.role_id = 1
    # r.aa = "a"
    # r.save()
    # u = User(username="zzzz", pwd="111222333")
    # setattr(u, "a", "1")
    # u.aa = 1
    # u.save()
    # print(u)
    # us = User.objects(pwd="111222333").first()
    # us = User.objects(pwd="111222333").count()
    # print us, type(us.username)
    # for u in us:
    #     print us.pwd
    # p = Post()
    # p.post = ["a", "b"]
    # p.save()
    # c1 = Comment(com=["a", "b"])
    # c2 = Comment(com=["1", "2"])
    # p = Page(pages=[c1, c2])
    # p.save()
    # p = Page.objects.first()
    # print p.pages[0].com
    # for c in p.pages:
    #     print c.com
    # u = User.objects(pwd="111222333").first()
    # sub = SubUser()
    # sub.sub_user = u
    # sub.save()
    # u = SubUser.objects.first()
    # print u.sub_user.username
    ps = Posts()
    ps.post = ["1"]
    ps.pppp = "123"
    ps.save()
    print(ps.id)
    ps.pppp = "a"
    ps.save()