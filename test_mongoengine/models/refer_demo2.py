# coding=utf-8
from mongoengine import connect, DynamicDocument, EmbeddedDocument
from mongoengine import ListField, StringField, IntField, ReferenceField
from mongoengine import NULLIFY, DO_NOTHING, DENY, CASCADE, PULL
import time

"""主要针对ReferenceField字段的引用删除做修改"""

connect('test12', host='mongo', port=27017)  # todo : mongo is system Hosts file


class Role(DynamicDocument):
    meta = {"collection": "role"}

    title = StringField()


class User(DynamicDocument):
    meta = {"collection": "user"}

    name = StringField()
    # role = ReferenceField(Role, reverse_delete_rule=DO_NOTHING)   # 默认情况 什么都不做，删除后可能来数据的丢失，不一致，导致查询出错误
    # role = ReferenceField(Role, reverse_delete_rule=DENY)    # 如果仍有document引用到这个对象，那么会阻止删除
    # role = ReferenceField(Role, reverse_delete_rule=CASCADE)   # 任何对象的字段引用到这个对象的会被先删除
    # role = ReferenceField(Role, reverse_delete_rule=PULL)  # 移除对于对象的引用关系
    role = ReferenceField(Role, reverse_delete_rule=NULLIFY)    # 任何对象的字段关联到这个对象的如果被删除，那么这个document也会被删除，关联关系作废。
    # todo  CASCADE 和 NULLIFY 注释有点问题 应该互换?


def clear():
    for i in Role.objects.all():
        i.delete()
    for i in User.objects.all():
        i.delete()


def create():
    role1 = Role()
    role1.title = "123"
    role1.save()
    user = User()
    user.name = "张三"
    user.role = role1
    user.save()


if __name__ == "__main__":
    # clear()
    # create()
    user = User.objects.first()
    user.delete()