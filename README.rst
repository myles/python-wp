================
Python WordPress
================

.. image:: https://img.shields.io/travis/myles/python-wp.svg
        :target: https://travis-ci.org/myles/python-wp

.. image:: https://codeclimate.com/github/myles/python-wp/badges/gpa.svg
        :target: https://codeclimate.com/github/myles/python-wp
        :alt: Code Climate


.. image:: https://pyup.io/repos/github/myles/python-wp/shield.svg
        :target: https://pyup.io/repos/github/myles/python-wp/
        :alt: Updates

.. image:: https://readthedocs.org/projects/python-wordpress/badge/?version=master
        :target: http://python-wordpress.readthedocs.io/en/master/?badge=master
        :alt: Documentation Status

A Python library for interacting with WordPress REST API.

* Free software: MIT License

Features
--------

* TODO

Quick Start
-----------

    >>> from wordpress import WordPress
    >>> wp = WordPress('http://example.org/')
    >>> posts = wp.list_posts()
    >>> for p in posts:
    ...     print('{title[rendered]}: {link}'.format(**p._json))
    Hello, World: http://example.org/2017/01/30/hello-world
