import pymongo
from pymongo import MongoClient

class TagDb(object):
    client = MongoClient()
    db = client.tagdb

    def addSong(self, song):
        try:
            self.db.songs.insert_one(song)
        except pymongo.errors.DuplicateKeyError:
            # TODO: log!
            print("Can't add a duplicate key")

    def addSongs(self, songs):
        print("Adding songs!")
        bulk = self.db.songs.initialize_unordered_bulk_op()
        [bulk.insert(song) for song in songs]
        try:
            bulk.execute()
        except pymongo.errors.BulkWriteError:
            # TODO: log!
            print("Could not bulk write!")

    def readAll(self, query_obj): # TODO: how do we use default args in python?
        cursor = self.db.songs.find(query_obj)
        for document in cursor:
            print(document)

        print(cursor.count())

# To convert seconds to time:
# >>> m, s = divmod(audio.info.length, 60)
# >>> h, m = divmod(m, 60)
# >>> print("%d:%02d:%02d" % (h, m, s))
