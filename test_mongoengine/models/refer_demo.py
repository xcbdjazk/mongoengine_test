# coding=utf-8
from mongoengine import connect, DynamicDocument
from mongoengine import ListField, StringField, IntField, ReferenceField
from mongoengine import NULLIFY, DO_NOTHING, DENY, CASCADE, PULL
import time

"""主要针对ReferenceField字段的引用删除做修改"""

connect('test1', host='mongo', port=27017)  # todo : mongo is system Hosts file


class Role(DynamicDocument):
    meta = {"collection": "role"}

    title = StringField()


class User(DynamicDocument):
    meta = {"collection": "user"}

    name = StringField()
    # roles = ListField(ReferenceField(Role, reverse_delete_rule=DO_NOTHING))    # 默认情况 什么都不做，删除后可能来数据的丢失，不一致，导致查询出错误
    # roles = ListField(ReferenceField(Role, reverse_delete_rule=DENY))    # 如果仍有document引用到这个对象，那么会阻止删除
    # roles = ListField(ReferenceField(Role, reverse_delete_rule=CASCADE))   # 任何对象的字段引用到这个对象的会被先删除
    # roles = ListField(ReferenceField(Role, reverse_delete_rule=PULL))  # 移除对于对象的引用关系
    roles = ListField(ReferenceField(Role, reverse_delete_rule=NULLIFY))    # 任何对象的字段关联到这个对象的如果被删除，那么这个document也会被删除，关联关系作废。


def clear():
    for i in Role.objects.all():
        i.delete()
    for i in User.objects.all():
        i.delete()


def create():
    role1 = Role()
    role2 = Role()
    role1.title = "123"
    role2.title = "321"
    role1.save()
    role2.save()
    user = User()
    user.name = "张三"
    user.roles = [role1, role2]
    user.save()


########################################################
"""
NULLIFY 和 PULL 的区别

"""


class Tag(DynamicDocument):
    meta = {"collection": "tag"}

    title = StringField()

    def __repr__(self):
        return "<{}> {}".format("Tag obj", self.title.encode("utf-8"))

    def __str__(self):
        return "<{}> {}".format("Tag obj", self.title.encode("utf-8"))


class Article(DynamicDocument):
    meta = {"collection": "art"}

    name = StringField()
    tag = ReferenceField(Tag, reverse_delete_rule=PULL)

    def __repr__(self):
        return "<{}> {}".format("Article obj", self.name.encode("utf-8"))

    def __str__(self):
        return "<{}> {}".format("Article obj", self.name.encode("utf-8"))


def _clear():
    for i in Article.objects.all():
        i.delete()
    for i in Tag.objects.all():
        i.delete()


def _create():
    tag1 = Tag()
    tag2 = Tag()
    tag1.title = "123"
    tag2.title = "321"
    tag1.save()
    tag2.save()
    art = Article()
    art.name = "张三"
    art.tag = tag1
    art.save()




if __name__ == "__main__":
    clear()
    # create()
    # user = User.objects.first()
    # print(user)
    # for r in user.roles:
    #     print(r)
    #     print(r.title)
    # time.sleep(1)
    # role = Role.objects(title="123").first()
    # role.delete()
    # for i in Role.objects.all():
    #     print i.title
    # time.sleep(1)
    # user = User.objects.first()
    # print(user)
    # for r in user.roles:
    #     print(r)
    #     print(r.title)
    # reverse_delete_rule=DO_NOTHING 删除被绑定的数据后查询抛出 AttributeError
    # reverse_delete_rule = DENY role被User引用的情况下 role拒绝被删除 抛出异常
    # reverse_delete_rule = CASCADE role 被删除的后，user也被删除
    # reverse_delete_rule = PULL role被删除后，user下的roles[] 移除掉被删除的role对象
    # reverse_delete_rule=NULLIFY role被删除后，user下的roles[] 全部都被移除掉
    _clear()
    _create()
    tag = Tag.objects(title="123").first()
    tag.delete()
    # PULL 模式下删除失败，会抛出异常，可能原因：pull只针对数组形式的对象 error log：Update failed (Cannot apply $pull to a non-array value)
    # NULLIFY 直接 删除引用的对象，解除关联关系
    for i in Article.objects.all():
        print(i)
        print(i.tag.delete())
    for i in Tag.objects.all():
        print(i)