import datetime
import unittest

from wordpress import WordPress


class TestWordPress(unittest.TestCase):

    def setUp(self):
        self.wp = WordPress('http://demo.wp-api.org/')

    def test_get_404(self):
        with self.assertRaises(Exception):
            self.wp._get('404')

    def test_post_404(self):
        with self.assertRaises(Exception):
            self.wp._post('404')

    def test_delete_404(self):
        with self.assertRaises(Exception):
            self.wp._delete('404')

    def test_list_posts(self):
        posts = self.wp.list_posts()
        posts.ids()

    def test_list_posts_after(self):
        posts = self.wp.list_posts(after=datetime.datetime.now())
        self.assertFalse(posts)

    def test_list_posts_before(self):
        posts = self.wp.list_posts(before=datetime.datetime.now())
        self.assertTrue(posts)

    def test_list_posts_context(self):
        with self.assertRaises(ValueError):
            self.wp.list_posts(context='test')

    def test_list_posts_order(self):
        with self.assertRaises(ValueError):
            self.wp.list_posts(order='test')

    def test_list_posts_orderby(self):
        with self.assertRaises(ValueError):
            self.wp.list_posts(orderby='test')

    def test_get_post(self):
        post = self.wp.get_post(470)
        post.id
        self.assertTrue(post)

    def test_list_categories(self):
        categories = self.wp.list_categories()
        self.assertTrue(categories)
