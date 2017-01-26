=====
Usage
=====

To use Python WordPress in a project::

    from wordpress import WordPress
    wp = WordPress('http://wordpress-site.dev/')

Get a list of posts::

    wp.list_post()

Retrieve a post::

    wp.get_post(443)

Delete a post::

    wp.delete_post(443)
