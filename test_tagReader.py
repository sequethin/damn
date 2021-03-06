from unittest import TestCase
from tagreader import TagReader
import mutagen

class TestTagReader(TestCase):
    def test_should_add(self):
        reader = TagReader()
        self.assertFalse(reader.should_add('bitrate_mode', mutagen.mp3.BitrateMode.UNKNOWN))
        self.assertFalse(reader.should_add('channels', 2))
        self.assertFalse(reader.should_add('arbitrary_tag', None))
        self.assertFalse(reader.should_add('arbitrary_tag', False))
