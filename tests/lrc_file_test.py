import unittest
from pathlib import Path

import pendulum

from pylrctool import LRCFile, LRCEvent


TEST_STRING = """
[ti:Don't Be Afraid]
[length:02:52]
[00:29.13]And I ain't gon' kill my vibe
[00:30.99]Put me to the test
[00:32.58]And then push me trough this life
[00:35.06]Don't be afraid
"""


class TestLRCFile(unittest.TestCase):
    def setUp(self):
        self.file = Path(__file__).resolve().with_name("test.lrc")
        self.file2 = Path(__file__).resolve().with_name("test2.lrc")
        self.file_len = len(self.file.read_text().splitlines())

    def test_parsing_from_file(self):
        lrc_file = LRCFile()
        lrc_file.from_file(self.file)

        event = LRCEvent(
            time=pendulum.duration(minutes=0, seconds=29, milliseconds=130),
            data="And I ain't gon' kill my vibe",
        )

        self.assertEqual(event, lrc_file[0])
        self.assertEqual(len(lrc_file), self.file_len)

    def test_parsing_from_string(self):
        lrc_file = LRCFile()
        lrc_file.from_string(TEST_STRING)

        title = LRCEvent(data="Don't Be Afraid", type=LRCEvent.Type.Title)
        lrc_file.add(title)

        self.assertEqual(lrc_file[0], title)

        event = LRCEvent(
            time=pendulum.duration(minutes=0, seconds=35, milliseconds=60),
            data="Don't be afraid",
        )
        lrc_file.add(event)
        self.assertEqual(lrc_file[-1], event)

    def test_add_new_event(self):
        lrc_file = LRCFile()
        lrc_file.from_file(self.file)

        event = LRCEvent(
            time=pendulum.duration(minutes=1, seconds=10, milliseconds=820),
            data="Oh, oh",
        )
        lrc_file.add(event)

        self.assertEqual(len(lrc_file), self.file_len + 1)
        self.assertEqual(lrc_file[-3], event)

        event2 = LRCEvent(
            time=pendulum.duration(minutes=0, seconds=27, milliseconds=320),
            data="When I wakeing up I'm feeling blessed",
        )
        lrc_file.add(event2)

        self.assertEqual(len(lrc_file), self.file_len + 2)
        self.assertEqual(lrc_file[0], event2)

    def test_dumps(self):
        lrc_file = LRCFile()
        lrc_file.from_file(self.file)
        self.assertEqual(lrc_file.dumps(), self.file.read_text())

    def test_merge_lines(self):
        lrc_file = LRCFile()
        lrc_file.from_file(self.file)
        lrc_file.merge_lines()

    def test_new_events(self):
        lrc_file = LRCFile()
        lrc_file.from_file(self.file)

        author = LRCEvent(data="Azahriah / BLANKS", type=LRCEvent.Type.Author)
        lrc_file.add(author)
        self.assertEqual(lrc_file[0], author)

        title = LRCEvent(data="Don't Be Afraid", type=LRCEvent.Type.Title)
        lrc_file.add(title)
        self.assertEqual(lrc_file[1], title)

        length = LRCEvent(data="02:52", type=LRCEvent.Type.Length)
        lrc_file.add(length)
        self.assertEqual(lrc_file[2], length)

    def test_for_empty_lines(self):
        lrc_file = LRCFile()
        lrc_file.from_file(self.file2)
        
        self.assertEqual(lrc_file[-1].data, "")

if __name__ == "__main__":
    unittest.main()
