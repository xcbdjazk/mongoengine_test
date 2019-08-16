# coding=utf-8
from mongoengine import connect, DynamicDocument, EmbeddedDocument
from mongoengine import ListField, StringField, IntField, ReferenceField, EmbeddedDocumentField
from mongoengine import NULLIFY, DO_NOTHING, DENY, CASCADE, PULL
import time

"""主要针对ReferenceField字段的引用删除做修改"""

connect('test2', host='mongo', port=27017)  # todo : mongo is system Hosts file


class BA(EmbeddedDocument):

    mm = StringField()

    @property
    def dd1(self):
        return self.mm[0:1]


class A(DynamicDocument):

    ddd = StringField()
    aa = EmbeddedDocumentField(BA)



if __name__ == '__main__':
    # ba = BA(mm='111')
    a = A.objects(ddd='1ddd').first()
    print a.aa.dd1
    # a.save()