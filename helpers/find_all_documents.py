from pprint import pprint
from pymongo import MongoClient


def find_all_documents():
    with MongoClient('mongodb://localhost:27017') as client:
        db = client.fmajil
        cursor = db.stacks.find()

    return list(cursor)


if __name__ == '__main__':
    pprint(find_all_documents())
