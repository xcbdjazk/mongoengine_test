# -*- coding:utf-8 -*-

from mongoengine import *
connect('test_mongo122', host='mongo', port=27017)  # todo : mongo is system Hosts file
import pymongo

from collections import Iterable
class D(EmbeddedDocument):
    k = StringField()
    v = IntField()
    o = IntField()

import asyncio
from mongoengine.context_managers import set_write_concern
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateMany, ReplaceOne

class MyQuerySet(QuerySet):

    async def _my_bulk_write(self, collection, l):
        collection.bulk_write(l)

    def insert_or_update(self, doc_or_docs, write_concern=None):
        if not isinstance(doc_or_docs, Iterable):
            doc_or_docs = [doc_or_docs]
        update_docs = list(doc.to_mongo() for doc in doc_or_docs if doc.pk)
        add_docs = list(doc.to_mongo() for doc in doc_or_docs if not doc.pk)
        write_concern = write_concern or {}
        with set_write_concern(self._collection, write_concern) as collection:
            collection = collection

        if not update_docs:
            collection.insert_many(add_docs)
        else:
            loop = asyncio.get_event_loop()
            l = []
            append = l.append
            for i in add_docs:
                append(InsertOne(i))
            for i in update_docs:
                append(ReplaceOne({"_id": i['_id']}, i))
                # append(UpdateMany({"_id": i['_id']}, {"$set": i}))
            collection.bulk_write(l)
            # task = asyncio.ensure_future(self._my_bulk_write(collection, l ))
            # loop.run_until_complete(task)


class User(Document):
    meta = {"collection": "user", 'indedx':{} ,'queryset_class': MyQuerySet}
    int_id = SequenceField()
    q = StringField()
    name = StringField()
    d = ListField(EmbeddedDocumentField(D))

    def __str__(self):
        return "<class {0} {1}>".format(self.__class__.__name__, self.int_id)


if __name__ == "__main__":
    # d = User()
    # d.name = '111'
    # d.save()im
    import time
    t1 = time.time()

    # for i in range(20000):
        # User().save()
        # a.append(User())
    # print(time.time() - t1)
    # User.objects.update(d=[D(v=1)])
    # d = User.objects.first().to_mongo().to_dict()
    # print(d)
    # import json
    # print(json.dumps(d))

    # o = []
    # for i in range(20000):
    #     u = User()
    #     u.name = str(i)
    #     o.append(u)
    # User.objects.insert_or_update(o)

    d = User.objects.all()
    a = []
    for i in d:
        i.name = 'ddd333dd1'
        a.append(i)
    print(1)
    User.objects.insert_or_update(a)
    # myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    # mydb = myclient["test_mongo122"]
    # mycol = mydb["user"]
    # data = mycol.find({})
    # n = []
    ######################################################################

    # from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateMany
    #
    # mylist = []
    # for i in range(1000):
    #     mylist.append({'int_id': i})
    # mycol.insert_many(mylist)
    # print(time.time()-t1)
    # for i in range(10000):
    #     if i % 1000 == 0 and i != 0:
    #         mycol.bulk_write(n)
    #         n = []
    #     n.append(UpdateMany({'int_id': i}, {"$set": {"name": '1123'}}))
    # print(time.time() - t1)
    # mycol.bulk_write(n)

    ######################################################################
    # mylist = []
    #
    # for i in range(1, 20001):
    #     user = User()
    #     # print(type(user.to_mongo()))
    #     mylist.append(user.to_mongo())
    # #     mylist.append({
    # #         "int_id": i,
    # #         "d": []
    # #     })
    # #
    # x = mycol.insert_many(mylist)
    # print(time.time() - t1)