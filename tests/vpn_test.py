import unittest


class MyTestCase(unittest.TestCase):
    COUNTRY_CONV = {
        "usa": "United States",
        "uk": "United Kingdom",
        "india": "India"
    }

    def test_something(self):
        print("PrintSomething")
        pass
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
