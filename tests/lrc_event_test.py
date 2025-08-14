import unittest

from pylrctool import LRCEvent

from pylrctool.exceptions import LRCParseError


class TestLRCEvent(unittest.TestCase):
    def test_parsing_normal_lyric(self):
        """Test parsing of LRCEvent from a string."""
        event = LRCEvent.from_string("[00:01.23]Hello World")
        self.assertEqual(event.time_code, "00:01.23")
        self.assertEqual(event.data, "Hello World")
        self.assertEqual(event.type, LRCEvent.Type.TimedLyric)
        self.assertEqual(event.compose, "[00:01.23]Hello World")

    def test_parsing_normal_lyric_fail(self):
        """Test parsing of LRCEvent from a string."""
        with self.assertRaises(LRCParseError):
             LRCEvent.from_string("00:01.23Hello World")
            
        with self.assertRaises(LRCParseError):
            LRCEvent.from_string("")

    def test_parsing_id_like_line(self):
        event = LRCEvent.from_string("[ti:Don't Be Afraid]")
        self.assertEqual(event.data, "Don't Be Afraid")
        self.assertEqual(event.type, LRCEvent.Type.Title)
    
    def test_parsing_with_repeat_lyric(self):
        event = LRCEvent.from_string("[00:21.10][00:45.10]Repeating lyrics (e.g. chorus)")
        self.assertEqual(event.time_code, "00:21.10")
        self.assertEqual(event.repeat_time_code, "00:45.10")
        self.assertEqual(event.data, "Repeating lyrics (e.g. chorus)")
        

if __name__ == "__main__":
    unittest.main()
