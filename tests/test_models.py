import json
import unittest
from datetime import datetime
from os.path import dirname, join, realpath

from wordpress.models import ResultSet, Post


class TestPost(unittest.TestCase):

    def setUp(self):
        root_dir = dirname(realpath(__file__))

        with open(join(root_dir, 'fixtures/post-448.json'), 'r') as fobj:
            self.post_fixture = json.loads(fobj.read())

        self.post = Post.parse(None, self.post_fixture)

        with open(join(root_dir, 'fixtures/posts.json'), 'r') as fobj:
            self.posts_fixture = json.loads(fobj.read())

        self.posts = Post.parse_list(None, self.posts_fixture)

    def test_parse(self):
        self.assertEqual(type(self.post.date), datetime)

    def test_parse_list(self):
        self.assertEqual(type(self.posts), ResultSet)

    def test_eq(self):
        self.assertEqual(self.post, self.post)
