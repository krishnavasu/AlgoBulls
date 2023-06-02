from typing import Any
from rest_framework.permissions import BasePermission
from .models import *
from rest_framework_jwt.serializers import jwt_decode_handler

class IsAuthenticated():
    # def __init__(self,token) :
    #     self.token = token

    def __call__(self, *args):
        return self

    def has_permission(self, request, view):
        token = request.headers['Authorization'].split()[1]
        if not token:
            return False
        try:
            decode = jwt_decode_handler(token)
            
            request.user = User.objects.get(id = decode['id'])
            # print("decode",decode)
            return True
        except:
            return False
        
    def has_object_permission(self, request, view, obj):
        # Add your custom object-level permission logic here
        # Return True if the user has permission, False otherwise
        return obj.owner == request.user
