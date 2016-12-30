from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.models import Collection, Site
from wagtail.wagtailcore.permission_policies import ModelPermissionPolicy

site_permission_policy = ModelPermissionPolicy(Site)
collection_permission_policy = ModelPermissionPolicy(Collection)


def get_app_permission_choices(app_label):
    """
    Return a list of permission form field choices pertaining to a given app.
    """
    import ipdb;ipdb.set_trace()
    global PERMISSIONS_LIST
    return [choice for choice in PERMISSIONS_LIST if choice[0].startswith('{}.'.format(app_label))]


def get_model_permission_choices(app_label, model_name):
    """
    Return a list of permission form field choices pertaining to a given model.
    """
    model_name = model_name.lower()
    import ipdb;ipdb.set_trace()
    global PERMISSIONS_LIST

    model_perms = []
    for choice in PERMISSIONS_LIST:
        if (choice[0].startswith('{}.{}_'.format(app_label, model_name))
                and choice[0].endswith("_{}".format(model_name))):
            model_perms.append(choice)

    return model_perms
