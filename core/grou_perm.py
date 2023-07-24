from django.contrib.auth.models import Group, Permission
#from django.contrib.contenttypes.models import ContentType

groups={
    'Developer':[
            "some_developer",
        ],
    'Guest':[
            "some_guest",
        ],
    }
for _name,_permissions in groups.items():
    list: _permissions
    group = Group.objects.get_or_create(name = _name)
    for _permission_codename in _permissions:
        _permission=Permission.objects.get_or_create(codename=_permission_codename)
        group.permissions.add(_permission)
