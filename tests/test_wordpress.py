import unittest
import datetime

from wordpress import WordPress


class TestWordPress(unittest.TestCase):

    def setUp(self):
        self.wp = WordPress('http://demo.wp-api.org/')

    def test_get_404(self):
        with self.assertRaises(Exception):
            self.wp._get('404')

    def test_list_post(self):
        posts = self.wp.list_post()
        posts.ids()

    def test_list_post_after(self):
        posts = self.wp.list_post(after=datetime.datetime.now())
        self.assertFalse(posts)

    def test_list_post_before(self):
        posts = self.wp.list_post(before=datetime.datetime.now())
        self.assertTrue(posts)

    def test_list_post_context(self):
        with self.assertRaises(ValueError):
            self.wp.list_post(context='test')

    def test_list_post_order(self):
        with self.assertRaises(ValueError):
            self.wp.list_post(order='test')

    def test_list_post_orderby(self):
        with self.assertRaises(ValueError):
            self.wp.list_post(orderby='test')

    def test_list_post_status(self):
        with self.assertRaises(ValueError):
            self.wp.list_post(status='test')

    def test_get_post(self):
        post = self.wp.get_post(470)
        post.id
        self.assertTrue(post)
