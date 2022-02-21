from rest_framework import permissions
from backend.models import Provider, Station
from django.core.exceptions import ObjectDoesNotExist


class UserBelongsToProviderGroup(permissions.BasePermission):
    """
    A permission used on the API views to make sure only the users belong to the provider group have access to this
    provider's data
    eg only users on the AO group can access records for the AO stations

    This a unified permission that can be used both for the station endpoint and the other API endpoints
    The difference is that on the station one, we are getting the StationID as param in the request, on the others
    we have already the OP_ID that is the providerAbbr
    Decided to handle both cases here so the same permission class can be applied to both views and
    we avoid repeating code, but if there is a need for separate permissions this is also possible

    If the params are wrong (eg op1_ID is nonsense) then the permission returns true because the view implements
    validation of params and the 400 response code will be returned by the view
    Another approach would be to return False in the permission, but then the user will see a 403 forbidden response
    which is not as accurate
    This is a design choice and should be documented and can be changed if required
    """

    message = "Permission denied: The user doesn't belong to the correct group for this provider"

    def has_permission(self, request, view):
        user = request.user
        # Allow access to everything to superusers
        if user.is_superuser:
            return True

        # Check if there is the stationID kwarg in the url
        if 'stationID' in view.kwargs:
            stationID = view.kwargs['stationID']
            try:
                station = Station.objects.get(stationid=stationID)
            except ObjectDoesNotExist:  # return true and let the view catch the exception
                return True
            providerabbr = station.stationprovider.providerabbr
        # Check if there is the op1_ID kwarg in the url
        elif 'op1_ID' in view.kwargs and 'op2_ID' in view.kwargs:
            providerabbr1 = view.kwargs['op1_ID']
            if not Provider.objects.filter(providerabbr=providerabbr1).exists():
                # return true and let the view catch the exception
                return True
            providerabbr2 = view.kwargs['op2_ID']
            if not Provider.objects.filter(providerabbr=providerabbr2).exists():
                # return true and let the view catch the exception
                return True
            return user.groups.filter(name=providerabbr2).exists() | user.groups.filter(name=providerabbr1).exists()
        elif 'op_ID' in view.kwargs:
            providerabbr = view.kwargs['op_ID']

        if not Provider.objects.filter(providerabbr=providerabbr).exists():
            # return true and let the view catch the exception
            return True
        return user.groups.filter(name=providerabbr).exists()
