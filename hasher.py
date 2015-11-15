import hashlib

class Hasher(object):
    BLOCKSIZE = 65536

    def __init__(self):
        self.hasher = hashlib.sha1()

    def getHash(self, file):
        buf = file.read(self.BLOCKSIZE)
        while len(buf) > 0:
            self.hasher.update(buf)
            buf = file.read(self.BLOCKSIZE)

        return self.hasher.hexdigest()
