from hasher import Hasher
from dbwriter import TagDb
import os
import mutagen

# TODO: this should be config
# rootdir = '/Volumes/Sequethin Drive/Music Collection/Alpha by Artist/P/Phil Collins'
rootdir = '/Volumes/Sequethin Drive/Music Collection/Alpha by Artist/C/Common/Common - Can I Borrow A Dollar'
hasher = Hasher();
db = TagDb()

# TODO: this needs tests
# TODO: this belongs in a class
def should_add(attr, value):
    if attr == 'bitrate_mode':
        return value != mutagen.mp3.BitrateMode.UNKNOWN
    elif attr == 'channels':
        return value != 2
    else:
        return value is not None and attr_value

song_list = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        fname = os.path.join(subdir, file)
        with open(fname, 'rb') as afile:
            audio = mutagen.File(fname)
            if audio is None:
                # TODO: Log for debugging
                continue

            # Get hash
            hash = hasher.getHash(afile)

        info_attrs_to_get = "bitrate", "length", "channels", "sample_rate", "bits_per_sample", "codec", "sketchy", "track_gain", "track_peak", "album_gain", "protected", "bitrate_mode"

        dict_to_write = { "path" : fname, "hash" : hash }

        for attr in info_attrs_to_get:
            try:
                attr_value = getattr(audio.info,attr)
                if should_add(attr, attr_value):
                    dict_to_write[attr] = attr_value
            except AttributeError:
                "" # assign null or something? TODO: at least log it

        #db.addSong(dict_to_write)
        song_list.append(dict_to_write)


db.addSongs(song_list)
db.readAll({})

