.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.memleak/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.memleak/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.memleak/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.memleak?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.memleak/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.memleak

.. image:: https://img.shields.io/pypi/v/collective.memleak.svg
    :target: https://pypi.python.org/pypi/collective.memleak/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.memleak.svg
    :target: https://pypi.python.org/pypi/collective.memleak
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.memleak.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.memleak.svg
    :target: https://pypi.python.org/pypi/collective.memleak/
    :alt: License


==================
collective.memleak
==================

Help locate memory leaks in a zope/plone site using objgraph

Features
--------

- Shows [most common types](https://mg.pov.lt/objgraph/objgraph.html#objgraph.most_common_types) and types growing since.
- shows objgraph [find_backref_chain](https://mg.pov.lt/objgraph/objgraph.html#objgraph.find_backref_chain) and 
  [show_backrefs](https://mg.pov.lt/objgraph/objgraph.html#objgraph.show_backrefs) to what might be holding on leaking objects


Documentation
-------------

Access via  ```/memview``` on your site with admin account.


Installation
------------

Install collective.memleak by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.memleak


and then running ``bin/buildout``


Authors
-------

Provided by awesome people ;)


Contributors
------------

- Dylan Jay (PretaGov)


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.memleak/issues
- Source Code: https://github.com/collective/collective.memleak


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
