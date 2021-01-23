from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message="Only owner can update detail."
    def has_object_permission(self,request,view,obj):
        if request.method == "DELETE":
            return obj.user == request.user
        else:
            return request.user

class IsDeliveryApplicationOwner(permissions.BasePermission):
    message="Only delivery boy can update their application."
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.delivery_boy.job_profile.user == request.user
        elif request.method == "GET":
            return request.user

class IsPermanentEmployeeApplicationOwner(permissions.BasePermission):
    message="Only permanent employee can update their application."
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.permanent_employee.job_profile.user == request.user
        elif request.method == "GET":
            return request.user

class IsFreelancerApllicationOwner(permissions.BasePermission):
    message="Only freelancer owner can update their application."
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.freelancer.job_profile.user == request.user
        elif request.method == "GET":
            return request.user



