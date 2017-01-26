import json
import unittest
from datetime import datetime
from os.path import dirname, join, realpath

from wordpress.models import ResultSet, Post, Category

root_dir = dirname(realpath(__file__))


class MockAPI(object):

    def list_posts(self, **kwargs):
        with open(join(root_dir, 'fixtures/posts.json'), 'r') as fobj:
            return Post.parse_list(self, json.loads(fobj.read()))

    def get_post(self, pk, **kwargs):
        with open(join(root_dir, 'fixtures/post-448.json'), 'r') as fobj:
            return Post.parse(self, json.loads(fobj.read()))

    def list_categories(self, **kwargs):
        with open(join(root_dir, 'fixtures/categories.json'), 'r') as fobj:
            return Category.parse_list(self, json.loads(fobj.read()))

    def get_category(self, pk, **kwargs):
        with open(join(root_dir, 'fixtures/category-1.json'), 'r') as fobj:
            return Category.parse(self, json.loads(fobj.read()))


class TestPost(unittest.TestCase):

    def setUp(self):
        self.api = MockAPI()
        self.post = self.api.get_post(448)
        self.post_list = self.api.list_posts()

    def test_parse(self):
        self.assertEqual(type(self.post.date), datetime)

    def test_parse_list(self):
        self.assertEqual(type(self.post_list), ResultSet)

    def test_eq(self):
        self.assertEqual(self.post, self.post)
