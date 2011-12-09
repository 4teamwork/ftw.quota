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


Links
-----

- Main github project repository: https://github.com/4teamwork/ftw.quota
- Issue tracker: https://github.com/4teamwork/ftw.quota/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.quota
- Continuous integration: https://jenkins.4teamwork.ch/job/ftw.quota/


Maintainer
----------

This package is produced and maintained by `4teamwork <http://www.4teamwork.ch/>`_ company.
