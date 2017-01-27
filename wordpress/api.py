from posixpath import join as urljoin

import requests

from ._meta import __version__, __project_name__, __project_link__
from .models import Post, PostRevision, Page, Category


class WordPress(object):

    def __init__(self, url, verify_ssl=True):
        """
        WordPress Library.

        Arguments
        ---------

        url : str
            The WordPress URL (ex https://example.org/).
        verify_ssl : bool
            Should we verify that the WordPress site is using a good SSL cert.
        """
        self.url = self._get_wp_api_url(url)
        self.version = 'v2'

        self.headers = {
            'User-Agent': '{0}/{1} +{2}'.format(
                __project_name__,
                __version__,
                __project_link__
            )
        }

    # Private Methods

    def _get_wp_api_url(self, url):
        """
        Private function for finding the WP-API URL.

        Arguments
        ---------

        url : str
            WordPress instance URL.
        """
        resp = requests.head(url)

        # Search the Links for rel="https://api.w.org/".
        wp_api_rel = resp.links.get('https://api.w.org/')

        if wp_api_rel:
            return wp_api_rel['url']
        else:
            # TODO: Rasie a better exception to the rel doesn't exist.
            raise Exception

    def _get(self, endpoint, params={}):
        """
        Private function for making GET requests.

        Arguments
        ---------

        endpoint : str
            WordPress endpoint.
        params : dict
            HTTP parameters when making the connection.

        Returns
        -------

        dict/list
            Returns the data from the endpoint.
        """
        url = urljoin(self.url, 'wp', self.version, endpoint)

        resp = requests.get(url, params=params, headers=self.headers)

        if not resp.status_code == 200:
            msg = ('WordPress REST API returned the status code '
                   '{0}.'.format(resp.status_code))
            raise Exception(msg)

        return resp.json()

    def _post(self, endpoint, data={}, params={}):
        """
        Private function for making POST requests.

        Arguments
        ---------

        endpoint : str
            WordPress endpoint.
        data : dict
            Data to send.
        params : dict
            HTTP parameters to use when making the connection.

        Returns
        -------

        dict/list
            Returns the data from the endpoint.
        """
        url = urljoin(self.url, 'wp', self.version, endpoint)

        resp = requests.get(url, data=data, params=params,
                            headers=self.headers)

        if not resp.status_code == 200:
            msg = ('WordPress REST API returned the status code '
                   '{0}.'.foramt(resp.status_code))
            raise Exception(msg)

        return resp.json()

    def _delete(self, endpoint, params={}):
        """
        Private function for making DELETE requests.

        Arguments
        ---------

        endpoint : str
            WordPress endpoint.
        params : dict
            HTTP parameters when making the connection.

        Returns
        -------

        dict/list
            Returns the data from the endpoint.
        """
        url = urljoin(self.url, 'wp', self.version, endpoint)

        resp = requests.delete(url, params=params, headers=self.headers)

        if not resp.status_code == 200:
            msg = ('WordPress REST API returned the status code '
                   '{0}.'.foramt(resp.status_code))
            raise Exception(msg)

        return resp.json()

    # Post Methods

    def list_posts(self, context='view', page=1, pre_page=10, search=None,
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

            One of: publish, future, draft, pending, private
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
            A list of wordpress.models.Post.
        """
        if context not in ['view', 'embed', 'edit']:
            raise ValueError('The context {0} is not allowed.'.format(context))

        if after:
            after = after.isoformat()

        if before:
            before = before.isoformat()

        if order not in ['asc', 'desc']:
            raise ValueError("You can't order {0}.".format(order))

        if orderby not in ['date', 'relevance', 'id', 'include', 'title',
                           'slug']:
            raise ValueError("You can't order by {0}.".format(orderby))

        if status not in ['publish', 'future', 'draft', 'pending', 'private']:
            raise ValueError("The status {0} is valid.".format(status))

        posts = self._get('posts', params=locals())

        return Post.parse_list(self, posts)

    def get_post(self, pk, context='view', password=None):
        """
        Retrieve a Post.

        Arguments
        ---------

        pk : in
            The post id you want to retrieve.
        context : str
            Scope under which the request is made; determines fields present in
            response.

            Default: view

            One of: view, embed, edit
        password : str
            The password for the post if it is password protected.

        Returns
        -------

        wordpress.models.Post
        """
        post = self._get('posts/{0}'.format(pk), params=locals())

        return Post.parse(self, post)

    def create_post(self, date=None, date_gmt=None, slug=None, status=None,
                    password=None, title=None, content=None, author=None,
                    excerpt=None, featured_media=None, comment_status=None,
                    ping_status=None, format=None, meta=None, sticky=None,
                    template=None, categories=None, tags=None,
                    liveblog_links=None):
        """
        Create a Post.

        Arguments
        ---------

        date : datetime
            The date the object was published, in the site’s timezone.
        date_gmt : datetime
            The date the object was published, as GMT.
        slug : str
            An alphanumeric identifier for the object unique to its type.
        status : str
            A named status for the object.

            One of: publish, future, draft, pending, private
        password : str
            A password to protect access to the content and excerpt.
        title : str
            The title for the object.
        content : str
            The content for the object.
        author : id
            The ID for the author of the object.
        excerpt : str
            The excerpt for the object.
        featured_media : int
            The ID of the featured media for the object.
        comment_status : str
            Whether or not comments are open on the object.

            One of: open, closed
        ping_status : str
            Whether or not the object can be pinged.

            One of: open, closed
        format : str
            The format for the object.

            One of: standard
        meta : dict
            Meta fields.
        sticky : bool
            Whether or not the object should be treated as sticky.
        template : str
            The theme file to use to display the object.

            One of:
        categories : str
            The terms assigned to the object in the category taxonomy.
        tags : str
            The terms assigned to the object in the post_tag taxonomy.
        liveblog_likes : str
            The number of Liveblog Likes the post has.
        """
        post = self._post('posts', data=locals())

        return Post.parse(self, post)

    def update_post(self, pk, date=None, date_gmt=None, slug=None, status=None,
                    password=None, title=None, content=None, author=None,
                    excerpt=None, featured_media=None, comment_status=None,
                    ping_status=None, format=None, meta=None, sticky=None,
                    template=None, categories=None, tags=None,
                    liveblog_links=None):
        """
        Update a Post.

        Arguments
        ---------

        pk : int
            The ID of the post you want to update.
        date : datetime
            The date the object was published, in the site’s timezone.
        date_gmt : datetime
            The date the object was published, as GMT.
        slug : str
            An alphanumeric identifier for the object unique to its type.
        status : str
            A named status for the object.

            One of: publish, future, draft, pending, private
        password : str
            A password to protect access to the content and excerpt.
        title : str
            The title for the object.
        content : str
            The content for the object.
        author : id
            The ID for the author of the object.
        excerpt : str
            The excerpt for the object.
        featured_media : int
            The ID of the featured media for the object.
        comment_status : str
            Whether or not comments are open on the object.

            One of: open, closed
        ping_status : str
            Whether or not the object can be pinged.

            One of: open, closed
        format : str
            The format for the object.

            One of: standard
        meta : dict
            Meta fields.
        sticky : bool
            Whether or not the object should be treated as sticky.
        template : str
            The theme file to use to display the object.

            One of:
        categories : str
            The terms assigned to the object in the category taxonomy.
        tags : str
            The terms assigned to the object in the post_tag taxonomy.
        liveblog_likes : str
            The number of Liveblog Likes the post has.
        """
        resp = self._post('posts/{0}'.format(pk), data=locals())

        return Post.parse(self, post)

    def delete_post(self, pk, force=False):
        """
        Delete a Post.

        Arguments
        ---------

        pk : int
            The post id you want to delete.
        force : bool
            Whether to bypass trash and force deletion.
        """
        resp = self._delete('posts/{0}'.format(pk), params=locals())

        if resp.status_code == 200:
            return True
        else:
            raise Exception(resp.json())

    # Post Reivion Methods

    def list_post_revisions(self, parent, context='view'):
        """
        List Post Revisions.

        Arguments
        ---------

        parent : int/wordpress.models.Post/wordpress.models.Page
            The id for the parent of the object.
        context : str
            Scope under which the request is made; determines fields present in
            response.

            Default: view

            One of: view

        Returns
        -------

        list
            A list of wordpress.models.PostRevision.
        """
        if type(parent) == int:
            parent_id = parent
        elif type(parent) in [Page, Post]:
            parent_id = parent.id

        resp = self._get('posts/{0}/revisions'.format(parent_id),
                         params=locals())

        return PostRevision.parse_list(self, resp.json())

    def get_post_revision(self, parent, pk, context='view'):
        """
        Get a Post Revision.

        Arguments
        ---------

        parent : int/wordpress.models.Post/wordpress.models.Page
            The id for the parent of the object.
        pk : int
            Unique identifier for the object.
        context : str
            Scope under which the request is made; determines fields present in
            response.

            Default: view

            One of: view

        Returns
        -------

        wordpress.models.PostRevision
        """
        if type(parent) == int:
            parent_id = parent
        elif type(parent) in [Page, Post]:
            parent_id = parent.id

        resp = self._get('posts/{0}/revisions/{1}'.format(parent_id, pk),
                         params=locals())

        return PostRevision.parse(self, resp.json())

    def delete_post_revision(self, parent, pk):
        """
        Delete Post Revision.

        Arguments
        ---------

        parent : int/wordpress.models.Post/wordpress.models.Page
            The id for the parent of the object.
        pk : int
            Unique identifier for the object.

        Returns
        -------

        dict
        """
        if type(parent) == int:
            parent_id = parent
        elif type(parent) in [Page, Post]:
            parent_id = parent.id

        resp = self._delete('posts/{0}/revisions/{1}'.format(parent_id, pk))

        return PostRevision.parse(self, resp.json())

    # Category Methods

    def list_categories(self, context='view', page=1, pre_page=10, search=None,
                        exclude=None, include=None, order='asc',
                        orderby='name', hide_empty=False, parent=None,
                        post=None, slug=None):
        """
        Get a list of categories.

        Arguments
        ---------

        context : str
            Scope under which the request is made; determines fields present in
            response.

            Default: view

            One of: view, embed, edit
        page : int
            Current page of the collection.

            Default: 1
        pre_page : int
            Maximum number of items to be returned in result set.

            Default: 10
        search : str
            Limit results to those matching a string.
        exclude : int
            Ensure result set excludes specific IDs.

            Default:
        include : int
            Limit result set to specific IDs.

            Default:
        order : str
            Order sort attribute ascending or descending.

            Default: asc

            One of: asc, desc
        orderby : str
            Sort collection by term attribute.

            Default: name

            One of: id, include, name, slug, term_group, description, count
        hide_empty : bool
            Whether to hide terms not assigned to any posts.
        parent : int/wordpress.models.Category
            Limit result set to terms assigned to a specific parent.
        post : int/wordpress.models.Post
            Limit result set to terms assigned to a specific post.
        slug : str
            Limit result set to terms with a specific slug.

        Returns
        -------

        list
            A list of wordpress.models.Category.
        """
        if context not in ['view', 'embed', 'edit']:
            raise ValueError('The context {0} is not allowed.'.format(context))

        if order not in ['asc', 'desc']:
            raise ValueError('The order {0} is not allowed.'.format(order))

        if orderby not in ['id', 'include', 'name', 'slug', 'term_group',
                           'description', 'count']:
            raise ValueError('The order by {0} is not '
                             'allowed.'.format(orderby))

        if type(parent) == Category:
            parent_id = Category.id
        elif type(parent) == int:
            parent_id = parent

        if type(post) == Post:
            post_id = Post.id
        elif type(post) == int:
            post_id = post

        category_list = self._get('categories', params=locals())

        return Category.parse_list(self, category_list)

    def get_category(self, pk, context='view', password=None):
        """
        Retrieve a Category.

        Arguments
        ---------

        pk : int
            The category id you want to retrieve.
        context : str
            Scope under which the request is made; determines fields present in
            response.

            Default: view

            One of: view, embed, edit

        Returns
        -------

        wordpress.models.Category
        """
        category = self._get('categories/{0}'.format(pk), params=locals())

        return Category.parse(self, category)

    # Tag Methods

    def list_tags(self, **kwargs):
        raise NotImplementedError

    def get_tag(self, **kwargs):
        raise NotImplementedError

    def create_tag(self, **kwargs):
        raise NotImplementedError

    def update_tag(self, **kwargs):
        raise NotImplementedError

    def delete_tag(self, **kwargs):
        raise NotImplementedError

    # Page Methods

    def list_pages(self, **kwargs):
        raise NotImplementedError

    def get_page(self, **kwargs):
        raise NotImplementedError

    def create_page(self, **kwargs):
        raise NotImplementedError

    def update_page(self, **kwargs):
        raise NotImplementedError

    def delete_page(self, **kwargs):
        raise NotImplementedError

    # Comment Methods

    def list_comments(self, **kwargs):
        raise NotImplementedError

    def get_comment(self, **kwargs):
        raise NotImplementedError

    def create_comment(self, **kwargs):
        raise NotImplementedError

    def update_comment(self, **kwargs):
        raise NotImplementedError

    def delete_comment(self, **kwargs):
        raise NotImplementedError

    # Taxonomy Methods

    def list_taxonomies(self, **kwargs):
        raise NotImplementedError

    def get_taxonomy(self, **kwargs):
        raise NotImplementedError

    # Media Methods

    def list_media(self, **kwargs):
        raise NotImplementedError

    def get_media(self, **kwargs):
        raise NotImplementedError

    def create_media(self, **kwargs):
        raise NotImplementedError

    def update_media(self, **kwargs):
        raise NotImplementedError

    def delete_media(self, **kwargs):
        raise NotImplementedError

    # User Methods

    def list_users(self, **kwargs):
        raise NotImplementedError

    def get_user(self, **kwargs):
        raise NotImplementedError

    def create_user(self, **kwargs):
        raise NotImplementedError

    def update_user(self, **kwargs):
        raise NotImplementedError

    def delete_user(self, **kwargs):
        raise NotImplementedError

    # Post Type Methods

    def list_post_types(self, **kwargs):
        raise NotImplementedError

    def get_post_type(self, **kwargs):
        raise NotImplementedError

    # Post Status Methods

    def list_post_statuses(self, **kwargs):
        raise NotImplementedError

    def get_post_status(self, **kwargs):
        raise NotImplementedError

    # Setting Methods

    def update_setting(self, **kwargs):
        raise NotImplementedError
