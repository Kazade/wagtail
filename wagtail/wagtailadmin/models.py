from __future__ import absolute_import, unicode_literals

# The edit_handlers module extends Page with some additional attributes required by
# wagtailadmin (namely, base_form_class and get_edit_handler). Importing this within
# wagtailadmin.models ensures that this happens in advance of running wagtailadmin's
# system checks.
from wagtail.wagtailadmin import edit_handlers  # NOQA
from django.db import models


class Admin(models.Model):
    """ Fake model to make sure Djangae correctly create simulated contenttype """
    pass
