"""
This script uses the django settings
Must be run as described in the README, eg python3 ../src/manage.py shell < group_creation.py

This is a utility script that must be run after the population of the database
It creates a group for each provider, based on the convention that the providerAbbr field is unique
The group has the name of the abbreviation eg OO
"""

from django.contrib.auth.models import Group
from backend.models import Provider

all_providers = Provider.objects.all()
for provider in all_providers:
    provider_abb = provider.providerabbr
    new_group, created = Group.objects.get_or_create(name=provider_abb)
    print(f"Successfully created group with name {provider_abb}")
