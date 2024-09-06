from rest_framework import permissions

from authentication.models import User


class GroupPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        #ip_addr = request.META['REMOTE_ADDR']
        #blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()

        user = request.user
        parking_id = request.query_params.get('parking', None)
        print(user, parking_id)
        return User.objects.filter(pk=user.id, parking__id=parking_id).exists()
