from __future__ import absolute_import, unicode_literals

from djangae.contrib.gauth.datastore.permissions import get_permission_choices as init_permissions
from wagtail.wagtailcore.models import Collection, Site
from wagtail.wagtailcore.permission_policies import ModelPermissionPolicy

site_permission_policy = ModelPermissionPolicy(Site)
collection_permission_policy = ModelPermissionPolicy(Collection)


# Hook into a Djangae hack that maintains a list of permission choices for forms to keep a list of installed permissions
init_permissions()
global PERMISSIONS_LIST

# Create organised permissions dict {'app_label': {'action_model': ('codename', 'description'),}}
PERMISSIONS_DICT = {perm_choice[0].split('.')[0]: {perm_choice[0].split('.')[1]: perm_choice}
                    for perm_choice in PERMISSIONS_LIST}


def get_app_permission_choices(app_label):
    """
    Return a list of permission form field choices pertaining to a given app.
    """
    import ipdb;ipdb.set_trace()
    return PERMISSIONS_DICT[app_label].values()


def get_model_permission_choices(app_label, model_name):
    """
    Return a list of permission form field choices pertaining to a given model.
    """
    model_name = model_name.lower()
    import ipdb;ipdb.set_trace()
    return [PERMISSIONS_DICT[app_label][action_model]
            for action_model in PERMISSIONS_DICT[app_label].keys() if action_model.endswith(model_name)]


def filter_permission_choices_to_actions(permission_choices, actions):
    """
    Filter a list of permission choices to include just the specified actions.
    """
    filtered_perm_choices = []
    for choice in permission_choices:
        for action in actions:
            if choice[0].split('.')[1].startswith(action):
                filtered_perm_choices.append(choice)

    return filtered_perm_choices


def get_codenames(permission_choices):
    """
    Return just the permission codenames from a list of permission choices.
    """
    return [perm_choice[0] for perm_choice in permission_choices]


