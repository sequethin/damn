import os

import mutagen
from mutagen import flac
from mutagen import mp3
from mutagen import mp4

from dbwriter import TagDb
from hasher import Hasher


class TagReader(object):
    # TODO: this should be config
    rootdir = '/Volumes/Sequethin Drive/Music Collection/Alpha by Artist/R/R23X - サウンド - ＲＰＧ'
    hasher = Hasher();
    db = TagDb()

    tag_map = {
        mutagen.mp4.MP4: {
            'track title': '\xa9nam',
            'album': '\xa9alb',
            'artist': '\xa9ART',
            'album artist': 'aART',
            'composer': '\xa9wrt',
            'year': '\xa9day',
            'comment': '\xa9cmt',
            'description': 'desc',
            'purchase date': 'purd',
            'grouping': '\xa9grp',
            'genre': '\xa9gen',
            'lyrics': '\xa9lyr',
            'podcast URL': 'purl',
            'podcast episode GUID': 'egid',
            'podcast category': 'catg',
            'podcast keywords': 'keyw',
            'encoded by': '\xa9too',
            'copyright': 'cprt',
            'album sort order': 'soal',
            'album artist sort order': 'soaa',
            'artist sort order': 'soar',
            'title sort order': 'sonm',
            'composer sort order': 'soco',
            'show sort order': 'sosn',
            'show name': 'tvsh',
            'part of a compilation': 'cpil',
            'part of a gapless album': 'pgap',
            'track': 'trkn',
            'disc': 'disk',
            'tempo': 'tmpo',




        }
    }

    def should_add(self, attr, value):
        if attr == 'bitrate_mode':
            return value != mutagen.mp3.BitrateMode.UNKNOWN
        elif attr == 'channels':
            return value != 2
        else:
            return value is not None and value

    def read_all_metadata(self):
        song_list = []
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                fname = os.path.join(subdir, file)
                print("Looking at " + fname)
                with open(fname, 'rb') as afile:
                    audio = mutagen.File(fname)
                    if audio is None:
                        # TODO: Log for debugging
                        continue

                    hash = self.hasher.getHash(afile)

                # Every song will have these
                dict_to_write = { "path" : fname, "hash" : hash }

                # Get the "Attributes" - not tags
                attrs = self.get_attrs_from_audio(audio)
                dict_to_write = {**dict_to_write, **attrs}

                # Get the tags
                tags = self.get_tags(audio)
                dict_to_write = {**dict_to_write, **tags}

                song_list.append(dict_to_write)

        self.db.addSongs(song_list)
        self.db.readAll({})

    def get_attrs_from_audio(self, audio):
        dict_to_return = {}
        info_attrs_to_get = "bitrate", "length", "channels", "sample_rate", "bits_per_sample", "codec", "sketchy", "track_gain", "track_peak", "album_gain", "protected", "bitrate_mode"
        for attr in info_attrs_to_get:
            try:
                attr_value = getattr(audio.info,attr)
                if self.should_add(attr, attr_value):
                    dict_to_return[attr] = attr_value
            except AttributeError:
                "" # TODO: at least log it

        return dict_to_return

    def get_tags(self, audio):
        file_type = type(audio)
        tags = {}
        for key in self.tag_map[file_type]:
            type_key = self.tag_map[file_type][key]
            if type_key in audio.tags:
                tags[key] = audio.tags[type_key]

        if file_type == mutagen.mp4.MP4:
            "" # get tags MP4 style
        elif file_type == mutagen.mp3.MP3:
            "" # get tags MP3 style
        elif file_type == mutagen.flac.FLAC:
            "" # get tags Flac style

        return tags
