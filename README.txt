ftw.quota
=========

This product adds quota support to archetypes containers.


Usage
-----

Add the marker interface ftw.quota.interfaces.IQuotaSupport to any archetypes
container that you want to have quota support.

Containers with quota support will get additional fields for quota setup.
You can setup quota limits in the edit form.

Add the marker interface ftw.quota.interfaces.IQuotaAware to any archetypes
content type that you want to count quota for.

To make all archetypes objects quota aware e.g. you can use the following
zcml directive.

>>> <five:implements
...     class="Products.Archetypes.BaseObject.BaseObject"
...     interface="ftw.quota.interfaces.IQuotaAware"
... />
