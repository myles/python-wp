from posixpath import join as urljoin

import requests

from ._meta import __version__, __project_name__, __project_link__
from .models import Post


class WordPress(object):

    def __init__(self, uri, verify_ssl=True):
        """
        WordPress Library.

        Arguments
        ---------

        uri : str
            The WordPress REST API URL (ex https://example.org/wp-json).
        verify_ssl : bool
            Should we verify that the WordPress site is using a good SSL cert.
        """
        self.uri = uri
        self.version = 'v2'

        self.headers = {
            'User-Agent': '{0}/{1} +{2}'.format(
                __project_name__,
                __version__,
                __project_link__
            )
        }

    def _get(self, endpoint, params={}):
        """
        Private function for making GET requests.

        Arguments
        ---------

        endpoint : str
            WordPress endpoint.

        Returns
        -------

        dict/list
            Returns the data from the endpoint.
        """
        url = urljoin(self.uri, 'wp', self.version, endpoint)

        resp = requests.get(url, params=params, headers=self.headers)

        if not resp.status_code == 200:
            msg = ('WordPress REST API returned the status code '
                   '{0}.'.foramt(resp.status_code))
            raise Exception(msg)

        return resp.json()

    def list_post(self, context='view', page=1, pre_page=10, search=None,
                  after=None, author=None, author_exclude=None, before=None,
                  exclude=None, include=None, offset=None, order='desc',
                  orderby='date', slug=None, status='publish',
                  categories=None, cateogries_exclude=None, tags=None,
                  tags_exclude=None, sticky=None):
        """
        Get a list of posts.

        Arguments
        ---------

        context : str
            Scope under which the request is made; determines fields present in
            response.

            Default: view

            One of: view, embed, edit
        page : int
            Current page of the collection.
        pre_page : int
            Maximum number of items to be returned in result set.
        search : str
            Limit results to those matching a string.
        after : datetime
            Limit response to posts published after a given date.
        author : int
            Limit result set to posts assigned to specific authors.
        author_exclude : int
            Ensure result set excludes posts assigned to specific authors.
        before : datetime
            Limit response to posts published before a given date.
        exclude : int
            Ensure result set excludes specific IDs.
        include : int
            Limit result set to specific IDs.
        offset : int
            Offset the result set by a specific number of items.
        order : str
            Order sort attribute ascending or descending.

            Default: desc

            One of: asc, desc
        orderby : str
            Sort collection by object attribute.
            Default: date
            One of: date, relevance, id, include, title, slug
        slug : str
            Limit result set to posts with one or more specific slugs.
        status : str
            Limit result set to posts assigned one or more statuses.
            Default: publish
        categories : str
            Limit result set to all items that have the specified term assigned
            in the categories taxonomy.
        categories_exclude : str
            Limit result set to all items except those that have the specified
            term assigned in the categories taxonomy.
        tags : str
            Limit result set to all items that have the specified term assigned
            in the tags taxonomy.
        tags_exclude : str
            Limit result set to all items except those that have the specified
            term assigned in the tags taxonomy.
        sticky : bool
            Limit result set to items that are sticky.

        Returns
        -------

        list
            A list of Post.
        """
        if context not in ['view', 'embed', 'edit']:
            # TODO: Better exception handling.
            raise ValueError('The context {0} is not allowed.'.format(context))

        if after:
            after = after.isoformat()

        if before:
            before = before.isoformat()

        if order not in ['asc', 'desc']:
            # TODO: Better exception handling.
            raise ValueError("You can't order {0}.".format(order))

        if orderby not in ['date', 'relevance', 'id', 'include', 'title',
                           'slug']:
            # TODO: Better exception handling.
            raise ValueError("You can't order by {0}.".format(orderby))

        if status not in ['publish']:
            # TODO: Figureout what other options there are for status.
            # TODO: Better exception handling.
            raise ValueError("The status {0} is valid.".format(status))

        posts = self._get('posts', params=locals())

        return Post.parse_list(self, posts)

    def get_post(self, pk, context='view', password=None):
        """
        Retrieve a Post.

        Arguments
        ---------

        context : str
            Scope under which the request is made; determines fields present in
            response.

            Default: view

            One of: view, embed, edit
        password : str
            The password for the post if it is password protected.
        """
        post = self._get('posts/{0}'.format(pk), params=locals())

        return Post.parse(self, post)
