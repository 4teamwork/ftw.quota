ftw.quota
=========

This product adds quota support to archetypes containers.


Install
-------

- Add the package to the eggs in your buildout configuration:

::

    [instance]
    eggs +=
        ftw.quota

- Install the generic setup profile of the package.


Usage
-----

Add the marker interface ``ftw.quota.interfaces.IQuotaSupport`` to any
archetypes container that you want to have quota support.

Containers with quota support will get additional fields for quota setup.
You can setup quota limits in the edit form.

To make all archetypes objects quota aware e.g. you can use the following
zcml directive:

::

    >>> <class class="Products.Archetypes.BaseObject.BaseObject">
    ...     <implements interface="ftw.quota.interfaces.IQuotaAware" />
    ... </class>


The quota configuration is stored using additional fields (schema extender)
and can be accessed easily:

::

    >>> container.Schema().getField('quota').get(container)
    ... ...  # quota in bytes
    >>> container.Schema().getField('usage').get(container)
    ... ...  # usage in bytes
    >>> container.Schema().getField('enforce').get(container)
    ... True  # when True it is not possible to add content when quota is exceeded


Nested quota containers are not supported at the moment.


Links
-----

- Main github project repository: https://github.com/4teamwork/ftw.quota
- Issue tracker: https://github.com/4teamwork/ftw.quota/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.quota
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.quota


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.quota`` is licensed under GNU General Public License, version 2.
