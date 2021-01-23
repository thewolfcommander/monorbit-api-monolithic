from rest_framework import permissions

class JobProfilePermission(permissions.BasePermission):
    """
    Only job profile owner can update their profile.
    """
    message="Only job profile owner can update their profile."
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.user == request.user
        elif request.method == "GET":
            return request.user

class DeliveryBoyVehiclePermission(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.delivery_boy.job_profile.user == request.user
        elif request.method == "GET":
            return request.user

class DeliveryBoyPermanentEmployeeAndFreelancer(permissions.BasePermission):
    """
    Only Owner of Delivery Boy or Permanent Employee or Freelancer can update their details.
    """
    message="Only Owner of Delivery Boy or Permanent Employee or Freelancer can update their details."
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.job_profile.user == request.user
        elif request.method == "GET":
            return request.user

