"""
Copyright 2009-2010 Joshua Roesslein
"""

from .utils import parse_iso8601


class ResultSet(list):
    """
    A list of like object that holds results from the WordPress API query.
    """

    def __init__(self):
        super(ResultSet, self).__init__()

    def ids(self):
        return [item.id for item in self if hasattr(item, 'id')]


class Model(object):

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)

        try:
            del pickle['_api']  # do not pickle the API reference
        except KeyError:
            pass

        return pickle

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        """
        Prase a list of JSON objects into a result set of model instances.
        """
        results = ResultSet()

        for obj in json_list:
            if obj:
                results.append(cls.parse(api, obj))

        return results

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))


class Post(Model):
    """
    A WordPress post object.

    Arguments
    ---------

    date : datetime
        The date the object was published, in the site’s timezone.
    date_gmt : datetime
        The date the object was published, as GMT.
    guid : dict
        The globally unique identifier for the object.
    id : int
        Unique identifier for the object.
    link : str
        URL to the object.
    modified : datetime
        The date the object was last modified, in the site’s timezone.
    modified_gmt : datetime
        The date the object was last modified, as GMT.
    slug : str
        An alphanumeric identifier for the object unique to its type.
    status : str
        A named status for the object.
    type : str
        Type of Post for the object.
    password : str
        A password to protect access to the content and excerpt.
    title : dict
        The title for the object.
    content : dict
        The content for the object.
    author : int
        The ID for the author of the object.
    excerpt : dict
        The excerpt for the object.
    featured_media : int
        The ID of the featured media for the object.
    comment_status : str
        Whether or not comments are open on the object.
    ping_status : str
        Whether or not the object can be pinged.
    format : str
        The format for the object.
    meta : list
        Meta fields.
    sticky : bool
        Whether or not the object should be treated as sticky.
    template : str
        The theme file to use to display the object.
    categories : list
        The terms assigned to the object in the category taxonomy.
    tags : list
        The terms assigned to the object in the post_tag taxonomy.
    liveblog_likes : int
        The number of Liveblog Likes the post has.
    """

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        post = cls(api)
        setattr(post, '_json', json)

        for k, v in json.items():
            if k in ['date', 'date_gmt', 'modified', 'modified_gmt']:
                setattr(post, k, parse_iso8601(v))

            elif k == 'categories':
                category_list = ResultSet()

                for category in v:
                    category_list.append(api.get_category(category))

                setattr(post, k, category_list)

            elif k == 'tags':
                tag_list = ResultSet()

                for tag in v:
                    tag_list.append(api.get_tag(tag))

                setattr(post, k, tag_list)

            else:
                setattr(post, k, v)

        return post

    def update(self, **kwargs):
        """Update the post."""
        return self._api.update_post(self.id)

    def delete(self, **kwargs):
        """Delete the post."""
        return self._api.delete_post(self.id)

    def revisions(self, **kwargs):
        """Lookup revisions of the post."""
        return self._api.list_post_revisions(self.id)

    def revision(self, pk, **kwargs):
        """Get a revision of the post."""
        return self._api.get_post_revision(self.id, pk)

    def __eq__(self, compare):
        """Compare two Posts."""
        if isinstance(compare, Post):
            return self.id == compare.id

        raise NotImplementedError


class PostRevision(Model):
    """
    A WordPress post object.

    Arguments
    ---------

    author : int
        The id for the author of the revision.

        Context: view
    date : datetime
        The date the object was published.

        Context: view
    date_gmt : datetime
        The date the object was published, as GMT.

        Context: view
    guid : dict
        GUID for the object, as it exists in the database.

        Context: view
    id : int
        Unique identifier for the object.

        Context: view
    modified : datetime
        The date the object was last modified.

        Context: view
    modified_gmt : datetime
        The date the object was last modified, as GMT.

        Context: view
    parent : int
        The id for the parent of the object.

        Context: view
    slug : str
        An alphanumeric identifier for the object unique to its type.

        Context: view
    title : str
        Title for the object, as it exists in the database.

        Context: view
    content : str
        Content for the object, as it exists in the database.

        Context: view
    excerpt : str
        Excerpt for the object, as it exists in the database.

        Context: view
    """

    @classmethod
    def parse(cls, api, json):
        post_revision = cls(api)
        setattr(post_revision, '_json', json)

        for k, v in json.items():
            if k in ['date', 'date_gmt', 'modified', 'modified_gmt']:
                setattr(post_revision, k, parse_iso8601(v))
            else:
                setattr(post_revision, k, v)

        return post_revision

    def destroy(self, **kwargs):
        return self._api.delete_post_revision(self.id)

    def __eq__(self, compare):
        """Compare two Posts."""
        if isinstance(compare, Post):
            return self.id == compare.id

        raise NotImplementedError


class Category(Model):
    """
    A WordPress Category

    Arguments
    ---------

    id : int
        Unique identifier for the term.

        Context: view, embed, edit
    count : int
        Number of published posts for the term.

        Context: view, edit

    description : str
        HTML description of the term.

        Context: view, edit
    link : str
        URL of the term.

        Context: view, embed, edit
    name : str
        HTML title for the term.

        Context: view, embed, edit
    slug : str
        An alphanumeric identifier for the term unique to its type.

        Context: view, embed, edit
    taxonomy : str
        Type attribution for the term.

        Context: view, embed, edit

        One of: category, post_tag, nav_menu, link_category, post_format
    parent : int
        The parent term ID.

        Context: view, edit
    meta : dict
        Meta fields.

        Context: view, edit
    """

    @classmethod
    def parse(cls, api, json):
        category = cls(api)
        setattr(category, '_json', json)

        for k, v in json.items():
            setattr(category, k, v)

        return category

    def update(self, **kwargs):
        return self._api.update_category(self.id)

    def delete(self, **kwargs):
        return self._api.delete_category(self.id)

    def __eq__(self, compare):
        """Compare two Posts."""
        if isinstance(compare, Category):
            return self.id == compare.id

        raise NotImplementedError


class Tag(Model):
    """
    A WordPress post object.

    Arguments
    ---------

    id : int
        Unique identifier for the term.

        Context: view, embed, edit
    count : int
        Number of published posts for the term.

        Context: view, edit
    description : str
        HTML description of the term.

        Context: view, edit
    link : str
        URL of the term.

        Context: view, embed, edit
    name : str
        HTML title for the term.

        Context: view, embed, edit
    slug : str
        An alphanumeric identifier for the term unique to its type.

        Context: view, embed, edit
    taxonomy : str
        Type attribution for the term.

        Context: view, embed, edit

        One of: category, post_tag, nav_menu, link_category, post_format
    meta : dict
        Meta fields.

        Context: view, edit
    """

    @classmethod
    def parse(cls, api, json):
        tag = cls(api)
        setattr(tag, '_json', json)

        for k, v in json.items():
            setattr(tag, k, v)

        return tag

    def update(self, **kwargs):
        return self._api.update_tag(self.id)

    def delete(self, **kwargs):
        return self._api.delete_tag(self.id)

    def __eq__(self, compare):
        """Compare two Posts."""
        if isinstance(compare, Tag):
            return self.id == compare.id

        raise NotImplementedError


class Page(Model):
    pass


class Comment(Model):
    pass


class Taxonomy(Model):
    pass


class Media(Model):
    pass


class User(Model):
    pass


class PostType(Model):
    pass


class PostStatus(Model):
    """
    A WordPress post object.

    Arguments
    ---------

    name : str
        The title for the resource.

        Context: embed, view, edit
    private : bool
        Whether posts with this resource should be private.

        Context: edit
    protected : bool
        Whether posts with this resource should be protected.

        Context: edit
    public : bool
        Whether posts of this resource should be shown in the front end of the
        site.

        Context: view, edit
    queryable : bool
        Whether posts with this resource should be publicly-queryable.

        Context: view, edit
    show_in_list : bool
        Whether to include posts in the edit listing for their post type.

        Context: edit
    slug : str
        An alphanumeric identifier for the resource.

        Context: embed, view, edit
    """
    @classmethod
    def parse(cls, api, json):
        post_status = cls(api)
        setattr(post_status, '_json', json)

        for k, v in json.items():
            setattr(post_status, k, v)

        return post_status

    def __eq__(self, compare):
        """Compare two Posts."""
        if isinstance(compare, PostStatus):
            return self.id == compare.id

        raise NotImplementedError


class Setting(Model):
    pass
