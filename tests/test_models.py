import json
import unittest
from datetime import datetime
from os.path import abspath, dirname, join, realpath

from wordpress.models import ResultSet, Tag, Category, Post

fixture_dir = abspath(join(dirname(realpath(__file__)), 'fixtures'))


class MockAPI(object):

    def list_posts(self, **kwargs):
        with open(join(fixture_dir, 'posts.json'), 'r') as fobj:
            return Post.parse_list(self, json.loads(fobj.read()))

    def get_post(self, pk, **kwargs):
        with open(join(fixture_dir, 'post-448.json'), 'r') as fobj:
            return Post.parse(self, json.loads(fobj.read()))

    def list_categories(self, **kwargs):
        with open(join(fixture_dir, 'categories.json'), 'r') as fobj:
            return Category.parse_list(self, json.loads(fobj.read()))

    def get_category(self, pk, **kwargs):
        with open(join(fixture_dir, 'category-1.json'), 'r') as fobj:
            return Category.parse(self, json.loads(fobj.read()))

    def list_tags(self, **kwargs):
        with open(join(fixture_dir, 'tags.json'), 'r') as fobj:
            return Tag.parse_list(self, json.loads(fobj.read()))

    def get_tag(self, pk, **kwargs):
        with open(join(fixture_dir, 'tag-3.json'), 'r') as fobj:
            return Tag.parse(self, json.loads(fobj.read()))


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


class TestCategory(unittest.TestCase):

    def setUp(self):
        self.api = MockAPI()
        self.category = self.api.get_category(1)
        self.category_list = self.api.list_categories()

    def test_parse(self):
        self.assertEqual(self.category.id, 1)

    def test_parse_list(self):
        self.assertEqual(type(self.category_list), ResultSet)

    def test_eq(self):
        self.assertEqual(self.category, self.category)


class TestTag(unittest.TestCase):

    def setUp(self):
        self.api = MockAPI()
        self.tag = self.api.get_tag(3)
        self.tag_list = self.api.list_tags()

    def test_parse(self):
        self.assertEqual(self.tag.id, 3)

    def test_parse_list(self):
        self.assertEqual(type(self.tag_list), ResultSet)

    def test_eq(self):
        self.assertEqual(self.tag, self.tag)
