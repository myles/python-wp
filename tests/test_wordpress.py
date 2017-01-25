import unittest

from wordpress import WordPress


class TestWordPress(unittest.TestCase):

    def setUp(self):
        self.wp = WordPress('http://demo.wp-api.org/wp-json/')

    def test_list_post(self):
        posts = self.wp.list_post()
        posts.ids()

    def test_get_post(self):
        post = self.wp.get_post(470)
        post.id
